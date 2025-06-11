# Estado del Proyecto

## Notas Importantes
- La versión de docker-compose está fijada en 3.11 y NO debe cambiarse a 3.8 u otra versión para evitar problemas de compatibilidad.
- Antes de crear nuevas carpetas o archivos, es crucial revisar y seguir las buenas prácticas y estándares de Django. La refactorización posterior de la estructura del proyecto es compleja y puede causar problemas de compatibilidad.

## Última Actualización: 11/06/2025

### Cambios Realizados
1. Reorganización de la estructura del proyecto:
   - Renombrado `core` a `config` para seguir las mejores prácticas de Django
   - Renombrado `core_app` a `vuln_manager` para mejor claridad
   - Actualizadas todas las referencias en el código

2. Reorganización de las vistas en archivos separados:
   - Creado directorio `vuln_manager/views/`
   - Separadas las vistas en archivos específicos:
     - `cliente_views.py`
     - `activo_views.py`
     - `vulnerabilidad_views.py`
   - Creado `__init__.py` para exportar las vistas

3. Corrección de nombres de campos en vistas y plantillas:
   - Actualizado `fecha_creacion` a `created_at`
   - Actualizado `fecha_actualizacion` a `updated_at`
   - Corregido `activo_set` a `activos`
   - Corregido `vulnerabilidad_set` a `vulnerabilidades`

4. Mejoras en las plantillas:
   - Mejorado el diseño y estructura HTML
   - Añadidos mensajes informativos cuando no hay datos
   - Mejorado el formato de la información mostrada
   - Añadidos badges para mostrar severidad de vulnerabilidades

### Cambios Recientes (11/06/2025)
- Corregidas las importaciones en las vistas para usar rutas absolutas (`vuln_manager.models`) en lugar de relativas
- Movidas las plantillas de `templates/core_app/` a `templates/vuln_manager/` para mantener consistencia con el nombre de la aplicación
- Eliminada temporalmente la restricción de login en las vistas para facilitar el desarrollo
- Corregida la configuración de URLs para incluir las rutas de autenticación
- Añadida plantilla de login en `templates/registration/login.html`
- Eliminado el directorio redundante `staticfiles/` y ajustada la configuración para usar solo `static/` como raíz de archivos estáticos.
- Añadida la estructura básica de carpetas en `static/` (`css`, `js`, `img`).
- Actualizado `settings.py` para reflejar estos cambios y mejorar la seguridad (CORS, CSRF, Whitenoise).
- Actualizado `requirements.txt` e instalado dependencias de testing y seguridad en el contenedor.
- Ejecutado `collectstatic` para recopilar archivos estáticos correctamente.

### Próximos Pasos
1. Implementar formularios para crear/editar entidades
2. Añadir autenticación y autorización
3. Implementar búsqueda y filtrado
4. Añadir validaciones de datos
5. Implementar pruebas unitarias

### Problemas Conocidos
1. No se puede acceder por HTTPS en desarrollo (configurado para usar HTTP)
2. Pendiente de implementar la gestión de sesiones de usuarios
3. El atributo `version` en docker-compose.yml está obsoleto (warning)
4. Necesidad de implementar la autenticación de usuarios
5. Pendiente de implementar formularios para crear/editar registros

### Notas
- El proyecto está funcionando correctamente en desarrollo con HTTP
- Las vistas están correctamente organizadas y son mantenibles
- Las plantillas están optimizadas y son responsivas

### Notas para la Próxima Sesión
1. Pendiente de implementar:
   - Formularios para crear/editar entidades
   - Sistema de autenticación
   - Búsqueda y filtrado
   - Validaciones de datos

2. Consideraciones técnicas:
   - Mantener la estructura actual de vistas separadas
   - Seguir el patrón de diseño actual para nuevas funcionalidades
   - Considerar la implementación de Class-Based Views para formularios

3. Puntos de atención:
   - Revisar la necesidad de HTTPS en desarrollo
   - Evaluar la implementación de un sistema de caché
   - Considerar la implementación de paginación en las listas

4. URLs actuales:
   - Lista de clientes: `/clientes/`
   - Detalle de cliente: `/clientes/<id>/`
   - Lista de activos: `/activos/`
   - Detalle de activo: `/activos/<id>/`
   - Lista de vulnerabilidades: `/vulnerabilidades/`
   - Detalle de vulnerabilidad: `/vulnerabilidades/<id>/`

## Última Sesión
- **Fecha**: [Fecha actual]
- **Objetivo**: Implementación del modelo de Vulnerabilidades
- **Cambios realizados**:
  - Añadido soporte para CVSS v2/v3
  - Implementado sistema de referencias
  - Añadido campo de estado para vulnerabilidades

## Estado Actual
- **Modelos implementados**:
  - [x] Cliente
  - [x] Activo
  - [x] Vulnerabilidad
  - [x] ActivoVulnerabilidad
  - [x] Alerta
  - [x] Tarea

- **Funcionalidades en desarrollo**:
  - Sistema de actualización automática de CVEs
  - Sistema de alertas
  - Generación de informes

## Próximas Tareas
1. Completar la implementación del modelo ActivoVulnerabilidad
2. Implementar el sistema de alertas
3. Desarrollar la generación de informes

## Notas de Desarrollo
- Usar Docker para todas las operaciones
- Seguir las convenciones de código establecidas
- Actualizar la documentación con cada cambio significativo 