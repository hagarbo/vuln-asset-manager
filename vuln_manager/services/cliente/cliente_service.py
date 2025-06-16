from django.db import transaction
from django.core.exceptions import ValidationError
import csv
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ClienteService:
    def crear_cliente_con_usuario_activos_y_analistas(
        self,
        datos_usuario: dict,
        datos_cliente: dict,
        archivo_activos,
        analistas_ids: list,
    ):
        """
        Crea un usuario (rol cliente), el cliente asociado, sus activos y asigna analistas.
        - datos_usuario: dict con username, email, password, etc.
        - datos_cliente: dict con nombre, etc.
        - archivo_activos: archivo Excel/CSV subido.
        - analistas_ids: lista de IDs de usuarios analistas a asignar.
        Devuelve el objeto Cliente creado.
        Lanza excepción si algo falla (transacción atómica).
        """
        usuario_repo = UsuarioRepository()
        cliente_repo = ClienteRepository()
        activo_repo = ActivoRepository()
        with transaction.atomic():
            # Validar y crear usuario
            if not datos_usuario.get('username') or not datos_usuario.get('email') or not datos_usuario.get('password'):
                raise ValidationError('Faltan datos obligatorios del usuario')
            if usuario_repo.model.objects.filter(username=datos_usuario['username']).exists():
                raise ValidationError('El nombre de usuario ya existe')
            if usuario_repo.model.objects.filter(email=datos_usuario['email']).exists():
                raise ValidationError('El email ya existe')
            usuario_cliente = usuario_repo.model.objects.create_user(
                username=datos_usuario['username'],
                email=datos_usuario['email'],
                password=datos_usuario['password'],
                rol='cliente'
            )
            # Crear cliente
            cliente = cliente_repo.create_cliente(nombre=datos_cliente['nombre'], usuario=usuario_cliente)
            # Asignar analistas
            cliente_repo.asignar_analistas(cliente, analistas_ids)
            # Crear activos desde archivo CSV (si se sube archivo)
            if archivo_activos:
                archivo_activos.seek(0)
                decoded = archivo_activos.read().decode('utf-8')
                reader = csv.DictReader(decoded.splitlines())
                columnas_obligatorias = ['nombre', 'tipo', 'descripcion', 'palabras_clave', 'ip', 'puerto', 'version']
                if not all(col in reader.fieldnames for col in columnas_obligatorias):
                    raise ValidationError('El archivo de activos no tiene todas las columnas obligatorias')
                for row in reader:
                    activo_repo.model.objects.create(
                        cliente=cliente,
                        nombre=row.get('nombre', ''),
                        tipo=row.get('tipo', ''),
                        descripcion=row.get('descripcion', ''),
                        palabras_clave=row.get('palabras_clave', ''),
                        ip=row.get('ip') or None,
                        puerto=row.get('puerto') or None,
                        version=row.get('version', '')
                    )
            return cliente 