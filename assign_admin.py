import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vuln_manager.models import Usuario

def assign_admin_role():
    try:
        # Buscar el superusuario por username
        admin_user = Usuario.objects.get(username='admin')
        
        # Asignar el rol de administrador
        admin_user.rol = Usuario.Rol.ADMIN
        admin_user.save()
        
        print(f"Rol de administrador asignado correctamente a {admin_user.username}")
    except Usuario.DoesNotExist:
        print("No se encontró el usuario 'admin'")
    except Exception as e:
        print(f"Error al asignar el rol: {str(e)}")

if __name__ == '__main__':
    assign_admin_role() 