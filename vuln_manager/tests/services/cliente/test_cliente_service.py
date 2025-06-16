import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from vuln_manager.services.cliente.cliente_service import ClienteService
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.auth.usuario import Usuario

@pytest.mark.django_db
class TestClienteService:
    def test_creacion_completa_cliente_usuario_activos_analistas(self):
        # Crear analistas de prueba
        analista1 = Usuario.objects.create_user(username='analista1', password='test', rol='analista')
        analista2 = Usuario.objects.create_user(username='analista2', password='test', rol='analista')

        # Datos de usuario y cliente
        datos_usuario = {
            'username': 'cliente1',
            'email': 'cliente1@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {
            'nombre': 'Empresa Cliente 1'
        }

        # Archivo de activos (CSV simulado)
        contenido_csv = b"nombre,tipo,descripcion,palabras_clave,ip,puerto,version\nServidor,hardware,Servidor principal,servidor,192.168.1.1,22,1.0"
        archivo = SimpleUploadedFile("activos.csv", contenido_csv, content_type="text/csv")

        # Ejecutar servicio
        cliente = ClienteService().crear_cliente_con_usuario_activos_y_analistas(
            datos_usuario=datos_usuario,
            datos_cliente=datos_cliente,
            archivo_activos=archivo,
            analistas_ids=[analista1.id, analista2.id]
        )

        # Comprobaciones
        assert cliente.nombre == 'Empresa Cliente 1'
        assert cliente.analistas.count() == 2
        assert cliente.activos.count() == 1
        usuario_cliente = Usuario.objects.get(username='cliente1')
        assert usuario_cliente.rol == 'cliente'
        assert usuario_cliente.email == 'cliente1@email.com'
        assert cliente.usuario == usuario_cliente

    def test_error_usuario_username_duplicado(self):
        Usuario.objects.create_user(username='cliente1', email='otro@email.com', password='test', rol='cliente')
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        datos_usuario = {
            'username': 'cliente1',
            'email': 'nuevo@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 2'}
        archivo = None
        with pytest.raises(ValidationError, match='nombre de usuario ya existe'):
            ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                datos_usuario=datos_usuario,
                datos_cliente=datos_cliente,
                archivo_activos=archivo,
                analistas_ids=[analista.id]
            )

    def test_error_usuario_email_duplicado(self):
        Usuario.objects.create_user(username='otro', email='cliente1@email.com', password='test', rol='cliente')
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        datos_usuario = {
            'username': 'cliente2',
            'email': 'cliente1@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 3'}
        archivo = None
        with pytest.raises(ValidationError, match='email ya existe'):
            ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                datos_usuario=datos_usuario,
                datos_cliente=datos_cliente,
                archivo_activos=archivo,
                analistas_ids=[analista.id]
            )

    def test_error_analista_invalido(self):
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        no_analista = Usuario.objects.create_user(username='noanalista', password='test', rol='cliente')
        datos_usuario = {
            'username': 'cliente3',
            'email': 'cliente3@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 4'}
        archivo = None
        with pytest.raises(ValidationError, match='analistas no son válidos'):
            ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                datos_usuario=datos_usuario,
                datos_cliente=datos_cliente,
                archivo_activos=archivo,
                analistas_ids=[analista.id, no_analista.id]
            )

    def test_error_archivo_activos_invalido(self):
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        datos_usuario = {
            'username': 'cliente4',
            'email': 'cliente4@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 5'}
        # Archivo CSV mal formado (sin cabecera)
        contenido_csv = b"Servidor,hardware,Servidor principal,servidor,192.168.1.1,22,1.0"
        archivo = SimpleUploadedFile("activos.csv", contenido_csv, content_type="text/csv")
        with pytest.raises(ValidationError):
            ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                datos_usuario=datos_usuario,
                datos_cliente=datos_cliente,
                archivo_activos=archivo,
                analistas_ids=[analista.id]
            )
        # Comprobar que no se creó el usuario ni el cliente
        assert not Usuario.objects.filter(username='cliente4').exists()
        assert not Cliente.objects.filter(nombre='Empresa Cliente 5').exists()

    def test_error_datos_incompletos(self):
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        datos_usuario = {
            'username': '',  # Falta username
            'email': 'cliente5@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 6'}
        archivo = None
        with pytest.raises(ValidationError):
            ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                datos_usuario=datos_usuario,
                datos_cliente=datos_cliente,
                archivo_activos=archivo,
                analistas_ids=[analista.id]
            )
        assert not Usuario.objects.filter(email='cliente5@email.com').exists()
        assert not Cliente.objects.filter(nombre='Empresa Cliente 6').exists()

    def test_transaccionalidad_si_falla_activos(self):
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        datos_usuario = {
            'username': 'cliente6',
            'email': 'cliente6@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 7'}
        # Archivo con columna obligatoria faltante
        contenido_csv = b"nombre,tipo\nServidor,hardware"
        archivo = SimpleUploadedFile("activos.csv", contenido_csv, content_type="text/csv")
        with pytest.raises(ValidationError):
            ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                datos_usuario=datos_usuario,
                datos_cliente=datos_cliente,
                archivo_activos=archivo,
                analistas_ids=[analista.id]
            )
        assert not Usuario.objects.filter(username='cliente6').exists()
        assert not Cliente.objects.filter(nombre='Empresa Cliente 7').exists()

    def test_creacion_sin_activos(self):
        analista = Usuario.objects.create_user(username='analista', password='test', rol='analista')
        datos_usuario = {
            'username': 'cliente7',
            'email': 'cliente7@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 8'}
        archivo = None
        cliente = ClienteService().crear_cliente_con_usuario_activos_y_analistas(
            datos_usuario=datos_usuario,
            datos_cliente=datos_cliente,
            archivo_activos=archivo,
            analistas_ids=[analista.id]
        )
        assert cliente.nombre == 'Empresa Cliente 8'
        assert cliente.activos.count() == 0
        assert cliente.usuario.username == 'cliente7'

    def test_creacion_sin_analistas(self):
        datos_usuario = {
            'username': 'cliente8',
            'email': 'cliente8@email.com',
            'password': 'seguro123'
        }
        datos_cliente = {'nombre': 'Empresa Cliente 9'}
        archivo = None
        cliente = ClienteService().crear_cliente_con_usuario_activos_y_analistas(
            datos_usuario=datos_usuario,
            datos_cliente=datos_cliente,
            archivo_activos=archivo,
            analistas_ids=[]
        )
        assert cliente.nombre == 'Empresa Cliente 9'
        assert cliente.analistas.count() == 0
        assert cliente.usuario.username == 'cliente8' 