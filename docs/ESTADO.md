# Estado del Proyecto

## Notas Importantes
- La versión de docker-compose está fijada en 3.11 y NO debe cambiarse a 3.8 u otra versión para evitar problemas de compatibilidad.
- **Estructura del Proyecto y Buenas Prácticas de Django:**
  - **Plantillas (Templates):**
    - **A nivel de Proyecto (`/templates/`):** Contiene plantillas globales como `base.html`, `home.html` y plantillas de autenticación (`/templates/registration/`).
    - **Específicas de la Aplicación (`/vuln_manager/templates/vuln_manager/`):** Cada aplicación tiene su propio directorio `templates` con un subdirectorio que coincide con el nombre de la aplicación.
  - **Archivos Estáticos (Static Files):**
    - **Específicos de la Aplicación (`/vuln_manager/static/`):** Todos los archivos estáticos (CSS, JS, imágenes) relacionados con una aplicación residen aquí.
  - **Configuración de URLs:**
    - `config/urls.py` delega las URLs específicas de la aplicación (`vuln_manager.urls`).
    - `vuln_manager/urls.py` define las rutas con `app_name` para usar namespaces.
  - **Vistas (`views.py`):**
    - Las vistas se separan en archivos por modelo.
    - `vuln_manager/views/__init__.py` expone las vistas necesarias.
  - **Consistencia de Contexto:** Se asegura que `context_object_name` en las vistas coincida con las variables usadas en las plantillas.
  - **Filtros de Plantilla:** Ubicados en `app_name/templatetags/` y cargados explícitamente.

## Última Actualización: 12/06/2025

### Cambios Realizados
1. **Sistema de Roles y Permisos:**
   - Implementado modelo de Usuario personalizado con roles jerárquicos (Admin, Analista, Cliente)
   - Añadida relación ManyToMany entre analistas y clientes
   - Implementados mixins para control de acceso basado en roles
   - Definidos permisos específicos para cada rol

2. **Estructura de Roles:**
   - **Administrador:**
     - Gestión completa de la aplicación
     - Creación de cuentas de analistas y clientes
     - Asignación de clientes a analistas
   - **Analista:**
     - Gestión de activos de sus clientes asignados
     - Gestión de vulnerabilidades de sus clientes
   - **Cliente:**
     - Visualización de sus propios activos
     - Visualización de vulnerabilidades de sus activos

3. **Mejoras en la Seguridad:**
   - Implementado sistema de permisos basado en roles
   - Añadidos mixins para control de acceso
   - Validaciones de acceso a nivel de vista y modelo

### Estado Actual
- **Modelos implementados y registrados en Admin:**
  - [x] Usuario (con sistema de roles)
  - [x] Cliente
  - [x] Activo
  - [x] Vulnerabilidad
  - [x] ActivoVulnerabilidad
  - [x] Alerta
  - [x] Tarea
  - [x] EjecucionTarea

- **Sistema de Roles:**
  - [x] Modelo de Usuario personalizado
  - [x] Relaciones analista-cliente
  - [x] Permisos específicos por rol
  - [x] Mixins de control de acceso

### Próximos Pasos
1. Implementar vistas específicas para cada rol
2. Desarrollar interfaz de gestión de usuarios
3. Implementar sistema de asignación de clientes a analistas
4. Desarrollar la interfaz para la gestión de Tareas y Alertas
5. Implementar la lógica de interacción con APIs externas
6. Desarrollar la generación de informes
7. Añadir pruebas unitarias para el sistema de roles

### URLs Actuales
- Inicio: `/`
- Panel de Administración: `/admin/`
- Login: `/config/login/`
- Logout: `/config/logout/`

## Notas de Desarrollo
- Usar Docker para todas las operaciones
- Seguir las convenciones de código establecidas
- Actualizar la documentación con cada cambio significativo
- Mantener la estructura de vistas separadas
- Seguir el patrón de diseño actual para nuevas funcionalidades

### Problemas Conocidos
1. El atributo `version` en docker-compose.yml está obsoleto (warning)
2. Pendiente de implementar vistas específicas para cada rol
3. Pendiente de implementar interfaz de gestión de usuarios

### Notas para la Próxima Sesión
1. Implementar vistas específicas para cada rol
2. Desarrollar interfaz de gestión de usuarios
3. Implementar sistema de asignación de clientes a analistas
4. Considerar la implementación de paginación en las listas

## Tests unitarios
- Pendiente de actualizar los tests para incluir el nuevo sistema de roles
- Añadir tests para los mixins de control de acceso
- Implementar tests para las relaciones analista-cliente

### ¿Qué cubren los tests?
- **Modelos:**
  - Cliente, Activo, Vulnerabilidad, Tarea, Alerta, ActivoVulnerabilidad, EjecucionTarea.
  - Se comprueba la creación de instancias, relaciones básicas y el método `__str__` de cada modelo.
- **Vistas:**
  - Listado y detalle de Cliente, Activo y Vulnerabilidad.
  - Se comprueba el acceso a las URLs, el uso de la plantilla correcta, la presencia de los objetos esperados en el contexto y la visualización de datos clave.

### ¿Cómo ejecutar los tests?

Los tests deben ejecutarse dentro del contenedor Docker para asegurar el mismo entorno que en producción/desarrollo. Utiliza el siguiente comando desde la raíz del proyecto:

```sh
docker compose exec vuln-manager-web python manage.py test vuln_manager
```

Esto:
- Crea una base de datos temporal para testing.
- Ejecuta todos los tests de la app `vuln_manager`.
- Muestra un resumen de los resultados.

### Recomendaciones para ampliar la cobertura
- Añadir tests para los filtros de plantilla personalizados y utilidades.
- Incluir tests para vistas adicionales o futuras funcionalidades (por ejemplo, formularios, permisos, etc.).
- Considerar el uso de fixtures para poblar la base de datos de test con más variedad de datos.

**Última ejecución:**
- Todos los tests pasan correctamente (18 tests, 0 fallos). 