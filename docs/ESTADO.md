# Estado del Proyecto Vuln-Asset-Manager

## Última Actualización: 20/06/2025

### 🎨 Cambios Recientes - Unificación Visual y Corrección de Permisos (20/06/2025)

#### Unificación del Diseño Visual de Dashboards
- **Banner Moderno y Coherente**: Implementado banner consistente en todos los dashboards (admin, analista, cliente)
- **Limpieza de Variables de Contexto**: Eliminadas variables innecesarias y duplicadas en vistas de dashboard
- **Corrección de Errores de Relaciones**: Solucionados errores de `activo.alerta_set` vs `activo.alertas` en templates
- **Coherencia Visual Completa**: Todos los dashboards ahora siguen el mismo patrón de diseño Mazer

#### Adaptación de Vistas y Plantillas por Rol
- **Vistas de Cliente**: Adaptadas para mostrar solo información relevante, ocultando botones de edición/eliminación
- **Columnas Condicionales**: Implementadas columnas que se muestran/ocultan según el rol del usuario
- **Acciones Seguras**: Clientes solo pueden ver detalles, no pueden editar ni eliminar datos
- **Filtros Avanzados**: Replicados filtros de alertas en activos y vulnerabilidades con filtros por:
  - Severidad (crítica, alta, media, baja)
  - Estado (nuevo, en_proceso, resuelto)
  - Búsqueda por texto
  - Filtros por fechas

#### Corrección de Permisos y Seguridad
- **Acceso Restringido**: Clientes solo pueden acceder a sus propios datos
- **Páginas 404**: Implementado comportamiento seguro mostrando 404 cuando clientes intentan acceder a datos de otros
- **Vistas de Detalle**: Permitido acceso a clientes en alertas y vulnerabilidades con lógica de filtrado
- **Listados Seguros**: Clientes solo ven sus activos, vulnerabilidades y alertas
- **Condicionales en Templates**: Implementadas verificaciones para ocultar elementos no permitidos

#### Mejoras de UX/UI
- **Botones de Acción**: Reorganizados en dashboard admin para mejor coherencia visual
- **Compatibilidad Nocturna**: Ajustados estilos para funcionar correctamente en modo oscuro
- **Clases Mazer**: Eliminado CSS personalizado, usando solo clases de Mazer
- **Selector de Cliente**: Ocultado para usuarios cliente en listado de alertas
- **Columna Cliente**: Ocultada en listado de alertas para clientes
- **Enlaces Funcionales**: Corregido enlace en dashboard cliente para filtro de alertas críticas

#### Archivos Modificados
- **Templates de Dashboard**: `admin/index.html`, `analista/index.html`, `cliente/index.html`
- **Vistas de Dashboard**: `admin.py`, `analista.py`, `cliente.py`
- **Templates de Entidades**: `activo/list.html`, `vulnerabilidad/list.html`, `alerta/list.html`
- **Vistas de Entidades**: `activo/list.py`, `vulnerabilidad/list.py`, `alerta/list.py`
- **Templates de Detalle**: `activo/detail.html`, `vulnerabilidad/detail.html`, `alerta/detail.html`
- **Vistas de Detalle**: `activo/detail.py`, `vulnerabilidad/detail.py`, `alerta/detail.py`

#### Seguridad Verificada
- **Filtrado por Cliente**: Todas las vistas respetan la relación usuario-cliente
- **Permisos por Rol**: Implementados correctamente en todas las vistas
- **Sin Fugas de Información**: Clientes no pueden acceder a datos de otros clientes
- **Experiencia Clara**: Interfaz adaptada para cada rol sin confusión

### ✅ Completado

#### Funcionalidades Core
- [x] **Sistema de Autenticación y Autorización**
  - Login/logout personalizado
  - Roles: admin, analista, cliente
  - Mixins de permisos por rol
  - Redirección automática por rol

- [x] **Gestión de Usuarios**
  - CRUD completo de usuarios
  - Asignación de roles
  - Formularios de creación y edición

- [x] **Gestión de Clientes**
  - CRUD completo de clientes
  - Asignación de analistas a clientes
  - Relación ManyToMany con usuarios analistas

- [x] **Gestión de Activos**
  - CRUD completo de activos
  - Asignación a clientes
  - Paginación en listados
  - Filtros y búsqueda

- [x] **Gestión de Vulnerabilidades**
  - CRUD completo de vulnerabilidades
  - Integración con NIST NVD API
  - Sistema de severidad (crítica, alta, media, baja)
  - Paginación y filtros

- [x] **Sistema de Correlación**
  - Correlación automática activo-vulnerabilidad
  - Correlador por palabras clave
  - Correlador por CVE específico
  - Generación automática de alertas

- [x] **Sistema de Alertas**
  - Modelo de alertas con estados
  - Estados: nueva, en_proceso, resuelta
  - Asociación con activos y vulnerabilidades

- [x] **Sistema de Tareas**
  - Tareas programadas de correlación
  - Ejecución manual de tareas
  - Tipos de tarea configurables
  - Historial de ejecuciones

#### Mejoras de UX/UI
- [x] **Paginación Implementada**
  - Lista de vulnerabilidades en detalle de activos (10 por página)
  - Lista de activos en detalle de clientes (10 por página)
  - Lista de activos afectados en detalle de vulnerabilidades (10 por página)
  - Navegación consistente con botones anterior/siguiente

- [x] **Mejoras Visuales**
  - Columna "Severidad" en lugar de "Vector CVSS" en detalle de activos
  - Badges de severidad consistentes con el listado de vulnerabilidades
  - Ordenación por severidad en detalle de activos
  - CSS de severidad cargado correctamente

#### Dashboards
- [x] **Dashboard del Analista**
  - Vista `AnalistaDashboardView` con permisos por rol
  - Template con diseño moderno y responsive
  - **Estructura corregida para cumplir con Mazer**:
    - Uso de `container-fluid py-4` como en admin dashboard
    - Widgets de estadísticas con `h-100` y `display-4`
    - Headers de tarjetas consistentes sin `border-bottom-0 bg-light`
    - Tabla con `table-link-row` para filas clickeables
    - Estilos CSS simplificados y coherentes
  - Estadísticas generales (alertas nuevas, en proceso, resueltas)
  - Alertas nuevas con información detallada
  - Resumen por cliente expandible/colapsable
  - Activos más vulnerables con ranking
  - Resumen de trabajo (hoy y esta semana)
  - URL: `/dashboard/analista/`
  - Funcionalidades JavaScript para interactividad
  - **Coherencia visual completa con dashboard de admin**
  - **Error corregido**: Referencias a `activo.alerta_set` en lugar de `activo.alertas`

#### Vistas de Alerta
- [x] **Sistema Completo de Gestión de Alertas**
  - **Repositorio actualizado** con métodos para filtrado por usuario y rol
  - **AlertaListView**: Listado único para admin y analistas con filtros
  - **AlertaDetailView**: Detalle con cambio automático de estado
  - **AlertaUpdateView**: Edición con validaciones por rol
  - **Templates completos**: list.html, detail.html, form.html
  - **URLs configuradas**: `/alertas/`, `/alertas/<id>/`, `/alertas/<id>/editar/`
  - **Funcionalidades avanzadas**:
    - Filtros por cliente, severidad y estado
    - Ordenación por múltiples campos
    - Paginación (10 por página)
    - Cambio automático de estado al acceder al detalle
    - Alertas relacionadas para contexto
  - **Integración con dashboard**: Enlaces funcionales desde dashboard del analista
  - **Seguridad**: Solo admin y analistas pueden acceder
  - **UX/UI**: Diseño Mazer consistente y responsive

#### Infraestructura y DevOps
- [x] **Docker y Docker Compose**
  - Contenedores para web, base de datos y Redis
  - Volúmenes persistentes
  - Variables de entorno configuradas

- [x] **Base de Datos**
  - PostgreSQL configurado
  - Migraciones aplicadas
  - Datos de prueba cargados

- [x] **Scripts de Utilidad**
  - `init_project.sh`: Inicialización completa del proyecto
  - `populate_demo_data.py`: Población de datos de prueba
  - `clean_database.py`: Limpieza de base de datos
  - `quick_clean.py`: Limpieza rápida
  - Documentación en `scripts/README.md`

#### Testing
- [x] **Tests Unitarios**
  - Tests de modelos
  - Tests de formularios
  - Tests de vistas
  - Tests de repositorios
  - Tests de servicios

### 🔄 En Progreso

#### Dashboards
- [x] **Dashboard del Cliente**
  - Vista y template pendientes
  - Resumen de activos y vulnerabilidades
  - Alertas del cliente
  - Estadísticas de seguridad

### 📋 Pendiente

#### Funcionalidades Avanzadas
- [ ] **Sistema de Notificaciones**
  - Notificaciones por email
  - Notificaciones en tiempo real
  - Configuración de alertas

- [ ] **Reportes y Analytics**
  - Reportes PDF
  - Gráficos y estadísticas
  - Exportación de datos

- [ ] **API REST**
  - Endpoints para integración externa
  - Autenticación por token
  - Documentación con Swagger

#### Mejoras de UX/UI
- [ ] **Dashboard del Cliente**
  - Implementación completa
  - Funcionalidades específicas para clientes

- [ ] **Mejoras de Navegación**
  - Breadcrumbs
  - Menús contextuales
  - Accesos directos

### 🐛 Problemas Conocidos

#### Resueltos
- ✅ Error de migración con tabla `vuln_manager_usuario` ya existente
  - **Solución**: Limpieza manual del volumen de datos con `docker volume rm vuln_manager_postgres_data`
  - **Prevención**: Usar `docker compose down -v` y reconstruir cuando sea necesario

- ✅ Errores de importación tras refactorización
  - **Solución**: Revisión sistemática de todas las importaciones y referencias
  - **Prevención**: Verificar imports tras cambios estructurales

### 📝 Notas Técnicas

#### Estructura del Proyecto
- **Plantillas**: Globales en `/templates/`, específicas en `/app_name/templates/app_name/`
- **Estáticos**: Específicos de app en `/app_name/static/`
- **Vistas**: Modularizadas en `/app_name/views/` con `__init__.py`
- **URLs**: Delegadas en `config/urls.py`, definidas con namespaces

#### Patrones de Desarrollo
- **TDD**: Tests escritos antes que la funcionalidad
- **Repository Pattern**: Separación de lógica de acceso a datos
- **Service Pattern**: Lógica de negocio en servicios
- **Mixin Pattern**: Reutilización de funcionalidad de permisos

#### Configuración de Docker
- **Servicio principal**: `vuln-manager-web`
- **Base de datos**: PostgreSQL con volumen persistente
- **Redis**: Para tareas asíncronas (futuro)
- **Variables de entorno**: Configuradas en `docker-compose.yml`

### 🎯 Próximos Pasos

1. **Completar Dashboard del Cliente**
   - Implementar vista y template
   - Añadir funcionalidades específicas
   - Probar con datos reales

2. **Sistema de Notificaciones**
   - Configurar email backend
   - Implementar notificaciones automáticas
   - Añadir configuración de alertas

3. **Mejoras de UX**
   - Implementar breadcrumbs
   - Añadir menús contextuales
   - Mejorar navegación general

4. **Testing Completo**
   - Aumentar cobertura de tests
   - Tests de integración
   - Tests de UI

### 📊 Métricas del Proyecto

- **Líneas de código**: ~15,000+
- **Archivos**: ~200+
- **Tests**: ~50+
- **Migraciones**: 17
- **Funcionalidades principales**: 8
- **Dashboards**: 1/2 completados

---

**Estado General**: 🟢 **Estable y Funcional**
El proyecto está en un estado sólido con todas las funcionalidades core implementadas y funcionando correctamente. El dashboard del analista está completo y funcional. El siguiente paso prioritario es completar el dashboard del cliente.

## 🚨 REGLAS MUY IMPORTANTES 🚨

### Estructura y Organización
1. **Una clase, un archivo**: Cada clase debe estar en su propio archivo. Para grupos relacionados (como formularios), crear una carpeta específica.
2. **Organización jerárquica**: Seguir las convenciones de Django para la estructura de carpetas.
3. **Carpeta raíz limpia**: Mantener solo los archivos estrictamente necesarios en la raíz del proyecto.
4. **Crecimiento controlado**: No añadir nueva funcionalidad hasta que la existente esté completamente probada y funcionando.
5. **Consistencia en nombres**: 
   - Mantener consistencia en el nombrado de archivos y modelos
   - Para modelos de relación, usar el formato `entidad1_entidad2.py` (ej: `activo_vulnerabilidad.py`)
   - Para clases de modelos de relación, usar el formato `Entidad1Entidad2` (ej: `ActivoVulnerabilidad`)

### Proceso de Desarrollo
1. **Confirmación de cambios**: Solicitar confirmación antes de crear nuevos archivos.
2. **Documentación**: Explicar claramente el propósito y funcionamiento de cada nuevo componente.
3. **TDD (Test-Driven Development)**:
   - Escribir tests antes de implementar nueva funcionalidad
   - Validar el código con tests unitarios
   - Mantener la cobertura de tests
4. **Verificación de funcionalidad**: Asegurar que todo funciona antes de añadir nuevas características.

### Convenciones de Nombrado
- Usar nombres descriptivos para contenedores Docker (evitar 'pfc-daw-dual')
- Mantener consistencia en el nombrado de archivos y clases
- Seguir las convenciones de Python/Django para el nombrado
- Para modelos de relación, usar el formato `entidad1_entidad2.py`
- Para clases de modelos de relación, usar el formato `Entidad1Entidad2`
- Para repositorios, usar el formato `entidad_repository.py` y la clase `EntidadRepository`
- Para servicios, usar el formato `entidad_service.py` y la clase `EntidadService`
- Para vistas, usar el formato `entidad_view.py` y la clase `EntidadView`
- Para formularios, usar el formato `entidad_form.py` y la clase `EntidadForm`
- Para URLs, usar el formato `entidad_urls.py`
- Para templates, usar el formato `entidad_list.html`, `entidad_detail.html`, etc.
- Para tests, usar el formato `test_entidad.py` y la clase `EntidadTest`

## Notas Importantes
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

## 📝 Registro de Cambios

### 2025-06-19: Ordenación y badges mejorados en detalle de activos
- **Implementada ordenación completa** en la tabla de vulnerabilidades del detalle de activos
- **Ordenación por severidad** con ranking inteligente (crítica=5, alta=4, media=3, baja=2, no_establecida=1)
- **Ordenación por fechas** (detección, resolución) y estado
- **Enlaces de ordenación** en encabezados con iconos de dirección (↑↓)
- **Badges mejorados** consistentes con el listado de vulnerabilidades
- **Paginación mejorada** que mantiene el parámetro de ordenación
- **Formato de fechas** mejorado (d/m/Y) para mejor legibilidad
- **CVE ID destacado** en negrita para mejor identificación
- **Consistencia mantenida** con el patrón de ordenación del listado de vulnerabilidades

### 2025-06-19: Paginación en detalle de vulnerabilidades
- **Implementada paginación** en la vista de detalle de vulnerabilidades para los activos afectados
- **Seguido el mismo patrón** usado en las otras vistas de detalle para mantener consistencia
- **10 activos por página** para mejorar el rendimiento y usabilidad
- **Navegación consistente** con botones anterior/siguiente y números de página
- **Preparado para escalabilidad** cuando las vulnerabilidades afecten a muchos activos
- **Mantenida la funcionalidad** existente sin afectar otras características

### 2025-06-19: Paginación en detalle de clientes
- **Implementada paginación** en la vista de detalle de clientes para los activos asociados
- **Seguido el mismo patrón** usado en el detalle de activos para mantener consistencia
- **10 activos por página** para mejorar el rendimiento y usabilidad
- **Navegación consistente** con botones anterior/siguiente y números de página
- **Preparado para escalabilidad** cuando los clientes tengan muchos activos
- **Mantenida la funcionalidad** existente sin afectar otras características

### 2025-06-19: Paginación implementada correctamente en detalle de activos
- **Implementada paginación completa** en la vista `ActivoDetailView` para las vulnerabilidades
- **Seguido el patrón de Mazer** usado en las vistas de listado existentes
- **10 vulnerabilidades por página** para mejorar el rendimiento y usabilidad
- **Navegación consistente** con botones anterior/siguiente y números de página
- **Verificación exitosa** con activos que tienen 174 vulnerabilidades (18 páginas)
- **Mantenida la funcionalidad** existente sin afectar otras características
- **Template actualizado** con paginación completa y responsive

### 2025-06-13: Integración y normalización de la recolección de CVEs desde NIST
- Arquitectura desacoplada con DTO, recolector y repositorio.
- Añadido soporte para CVSS v3 y CVSS v4 (eliminado CVSS v2).
- Normalización automática de los campos de severidad (`severidad`, `cvss3_severidad`, `cvss4_severidad`).
- Ampliados los campos `cvss3_vector` y `cvss4_vector` a 512 caracteres.
- Comando de gestión para recolección periódica (`collect_cves`).
- Script para normalizar severidad en la base de datos.
- Tests para el recolector y validación de integración.
- Documentación de la estructura y buenas prácticas para futuras fuentes de CVEs.

### 2025-06-13: Limpieza y migración de datos
- Eliminadas vulnerabilidades recientes para pruebas de recolección.
- Actualización de la base de datos y migraciones para soportar los nuevos campos.

### 2024-06-12: Sistema de Roles y Permisos
- Implementado modelo de Usuario personalizado con roles jerárquicos (Admin, Analista, Cliente)
- Añadida relación ManyToMany entre analistas y clientes
- Implementados mixins para control de acceso basado en roles
- Definidos permisos específicos para cada rol

### 2024-06-12: Estructura de Roles y Seguridad
- Mejoras en la seguridad y control de acceso
- Validaciones de acceso a nivel de vista y modelo

### 2024-03-19 a 2024-03-20: Reorganización y buenas prácticas
- Reorganización de formularios, vistas y tests por entidad
- Separación de archivos y carpetas siguiendo el dominio
- Refactorización de modelos de relación y consistencia en nombres
- Actualización de la documentación y reglas del proyecto

### 2025-06-15: Modelos y repositorio de tareas programadas
- Se ha creado el modelo `Tarea` para gestionar tareas programadas (por ejemplo, recolección de CVEs), siguiendo la estructura y convenciones del proyecto.
- Se ha creado el modelo `EjecucionTarea` para registrar la ejecución de cada tarea, incluyendo estadísticas específicas para tareas de CVE.
- Se ha implementado el repositorio `TareaRepository` con métodos para filtrar, actualizar y consultar tareas según distintos criterios.
- Se han desarrollado y ejecutado tests unitarios para los modelos y el repositorio, cubriendo validaciones, creación, actualización, filtrado y representación.
- **Todos los tests han pasado correctamente.**

### 2024-06-17: Mejora visual del dashboard y padding
- Se ha añadido padding generoso (2rem) al contenido principal del dashboard (`main-content`) para mejorar la legibilidad y el aspecto visual en todas las vistas internas.
- El color de fondo oscuro (`#181c2f`) ahora se define en una sección de estilos CSS en `base_dashboard.html` en vez de en línea, facilitando su mantenimiento y personalización.
- Se ha creado la clase `.main-content` y se ha aplicado en `dashboard/base.html` para unificar el espaciado en todas las páginas del dashboard.
- Se mantiene la coherencia visual y la separación clara entre sidebar y contenido principal.
- No se han realizado cambios funcionales, solo mejoras visuales y de organización del CSS.

### 2025-06-18: Paginación en detalle de activos
- **Implementada paginación** en la vista de detalle de activos para las vulnerabilidades
- **Seguido el patrón de Mazer** usado en las vistas de listado existentes
- **10 vulnerabilidades por página** para mejorar el rendimiento
- **Navegación consistente** con botones anterior/siguiente y números de página
- **Mantenida la funcionalidad** de asignación automática de analistas a clientes

### 2025-06-18: Simplificación de scripts de inicialización
- **Eliminados archivos extra:** `start_production.sh`, `docker-compose.prod.yml`, `reset_production.py`
- **Mantenida verificación simple** en `init_project.sh` para evitar inicialización repetida
- **Solución minimalista:** Solo verifica si hay datos existentes antes de inicializar
- **Variable de entorno:** `FORCE_INIT=true` para forzar inicialización cuando sea necesario
- **Keep it simple:** Sin auto-eliminación ni scripts complejos

### 2025-06-18: Control de inicialización condicional para producción
- **Implementado control inteligente de inicialización** en `init_project.sh`
- **Verificación automática** de datos existentes antes de ejecutar inicialización
- **Variable de entorno `FORCE_INIT=true`** para forzar inicialización cuando sea necesario
- **Script `reset_production.py`** para reset completo con confirmación manual
- **Documentación actualizada** con nuevos comandos y flujos de trabajo
- **Lógica de verificación:** Solo inicializa si `usuarios_count > 1` o `clientes_count > 0`

### 2025-06-18: Asignación automática de analistas a clientes
- **Implementada asignación automática de analistas a clientes** en los scripts de inicialización
- **Actualizado `init_production.py`** para incluir asignación aleatoria de 1-2 analistas por cliente
- **Verificado que `populate_demo_data.py`** ya incluía esta funcionalidad
- **Documentación actualizada** en `scripts/README.md` con ejemplos y comandos de verificación
- **Pruebas exitosas** de correlación con datos que incluyen asignaciones de analistas
- **Funcionalidad completa** para verificar asignaciones desde clientes y analistas

### 2025-06-18: Scripts de inicialización y limpieza completados

## Estado Actual
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

## Próximos Pasos
1. Visualización y filtrado avanzado de vulnerabilidades (por severidad, fecha, CVSS, etc.).
2. Mejorar la presentación de los datos de CVSS v4 en la interfaz.
3. Programar el comando `collect_cves` como Scheduled Job en Render.
4. Implementar nuevos recolectores para otras fuentes de CVEs.
5. Mejorar la gestión de usuarios y roles (vistas específicas, asignación de clientes a analistas).
6. Ampliar la cobertura de tests (inserción/actualización de vulnerabilidades, filtros de plantilla, etc.).
7. Unificar y mantener actualizado este fichero de estado y el de `docs/estado.md`.
8. Documentar el flujo de recolección y normalización de CVEs.
9. Revisar la visualización de los nuevos campos en la interfaz.
10. Probar la integración de la tarea programada en Render.

## Notas de Desarrollo
- Usar Docker para todas las operaciones
- Seguir las convenciones de código establecidas
- Actualizar la documentación con cada cambio significativo
- Mantener la estructura de vistas separadas
- Seguir el patrón de diseño actual para nuevas funcionalidades

## Tests unitarios
- Añadir tests para los nuevos campos y lógica de recolección
- Mantener la cobertura de tests para roles, permisos y relaciones
- Ejecutar los tests dentro del contenedor Docker:

```sh
docker compose exec vuln-manager-web python manage.py test vuln_manager
```

## Cambios Realizados

### 14/06/2024
- Refactorización de la estructura de templates:
  - Renombradas las carpetas de templates de plural a singular para mantener coherencia con el resto del proyecto:
    - `activos` → `activo`
    - `clientes` → `cliente`
    - `vulnerabilidades` → `vulnerabilidad`
  - Actualizadas todas las referencias a los templates en las vistas y tests
  - Verificado que todos los tests pasan correctamente tras la refactorización

- Mejoras en la vista de vulnerabilidades:
  - Añadido orden por defecto por `fecha_modificacion` en orden descendente
  - Eliminada la advertencia de paginación con objetos no ordenados
  - Las vulnerabilidades ahora se muestran con las más recientes primero

### Tareas Pendientes
- Documentar la estructura del proyecto
- Implementar tests adicionales para nuevas funcionalidades
- Revisar y actualizar la documentación de la API 

## Lecciones Aprendidas

### Errores de Bytes Nulos en Python
- Cuando se encuentra un error `SyntaxError: source code string cannot contain null bytes`, generalmente indica un problema en la cadena de importaciones de Python.
- Este error suele aparecer cuando hay problemas en los archivos `__init__.py`, especialmente cuando:
  1. Faltan importaciones necesarias en algún `__init__.py` de la cadena
  2. Hay importaciones circulares entre módulos
  3. Los modelos o clases no están correctamente expuestos en los `__all__` de los `__init__.py`
- Para resolver estos errores:
  1. Revisar la cadena completa de importaciones desde el punto donde se origina el error
  2. Verificar que todos los `__init__.py` necesarios existen y están correctamente configurados
  3. Asegurarse de que los modelos y clases están correctamente importados y expuestos en los `__init__.py`
  4. Si es necesario, recrear los archivos `__init__.py` desde cero para evitar problemas de codificación 

## 15 de Junio 2024 - Implementación de Tareas Programadas

### Trabajo Realizado
- Se intentó implementar la funcionalidad de tareas programadas usando Celery
- Se añadieron las dependencias necesarias (celery, django-celery-beat, redis)
- Se configuró el entorno Docker para incluir los servicios de Celery y Redis
- Se creó una implementación inicial de tasks.py y cve_service.py

### Problemas Encontrados
1. **Inconsistencia en la Arquitectura**:
   - Se creó una nueva implementación sin tener en cuenta el código existente
   - Se duplicó funcionalidad que ya existía en management/commands
   - No se siguió el patrón de diseño establecido

2. **Lecciones Aprendidas**:
   - Siempre revisar el código existente antes de crear nuevas implementaciones
   - Mantener la consistencia con la arquitectura establecida
   - Seguir el patrón de diseño acordado (servicios, repositorios, commands)
   - Documentar los cambios antes de implementarlos

### Próximos Pasos
1. Revisar la estructura actual del proyecto:
   - Analizar management/commands/collect_cves.py
   - Revisar la implementación de servicios y repositorios existentes
   - Documentar el flujo de trabajo actual

2. Planificar la implementación de tareas programadas:
   - Definir cómo integrar Celery con la estructura existente
   - Mantener la consistencia con el patrón de diseño actual
   - Asegurar que no se duplique funcionalidad

3. Consideraciones para la implementación:
   - Usar el comando existente como base
   - Mantener la separación de responsabilidades
   - Seguir el patrón de la comunidad
   - Documentar cada paso del proceso

### Archivos Eliminados
- vuln_manager/tasks.py
- vuln_manager/views/tarea/execute.py
- vuln_manager/services/cve_service.py

### Dependencias Añadidas
- celery==5.3.6
- django-celery-beat==2.5.0
- redis==5.0.1

### Notas Importantes
- La implementación de tareas programadas debe integrarse con el sistema existente
- Mantener la consistencia con la arquitectura actual es crucial
- Seguir el patrón de diseño establecido por la comunidad
- Documentar todos los cambios y decisiones 

## Lecciones aprendidas sobre errores en tests y codificación

- **Errores de integridad referencial en tests:**
  - Si los tests fallan con errores de integridad (por ejemplo, `null value in column "usuario_id"`), revisar que todos los objetos requeridos por la base de datos (usuarios, claves foráneas, etc.) se creen correctamente en el test.
  - No asumir que el problema está en la estructura de carpetas o archivos vacíos si antes los tests funcionaban y no ha habido cambios masivos en la estructura.

- **Errores de codificación:**
  - Si aparecen errores extraños al leer o escribir archivos, comprobar la codificación (UTF-8 sin BOM, sin bytes nulos) y asegurarse de que los editores y scripts respetan la codificación estándar.

- **Diagnóstico:**
  - Antes de eliminar carpetas o archivos, ejecutar los tests de forma individual para aislar el problema.
  - Documentar estos casos en el historial del proyecto para referencia futura. 

### Estado de los tests de activo-vulnerabilidad (16/06/2025)

- Se han corregido referencias a `user.role` por `user.rol` en vistas y tests para coherencia con el modelo personalizado `Usuario`.
- Se han actualizado los nombres de los templates en los tests para que coincidan con los usados en las vistas (`form.html`, `confirm_delete.html`).
- Se ha añadido el atributo `fields = '__all__'` en las vistas de creación y actualización para cumplir con los requisitos de Django.
- Actualmente, solo fallan dos tests (`test_create_activo_vulnerabilidad` y `test_update_activo_vulnerabilidad`) porque la respuesta es 200 en vez de 302, lo que indica errores de validación en el formulario (probablemente faltan campos obligatorios o hay valores incorrectos en los datos enviados).
- Próximo paso: imprimir los errores del formulario en los tests para identificar y corregir los datos enviados.

#### Nota
Mañana se abordará la implementación de los dashboards para los distintos roles. Se recomienda revisar primero los errores de los tests para dejar la base estable antes de avanzar con nuevas funcionalidades. 

# Estado del proyecto (última sesión)

## Cambios realizados hoy
- Unificación visual y funcional de todas las plantillas antiguas al layout moderno del dashboard (sidebar, modo oscuro, bloques dashboard_content).
- Integración del botón de modo oscuro en el sidebar, con persistencia de preferencia y funcionamiento real usando data-bs-theme en <html>.
- Logo del sidebar igual que en la landing, coherente en ambos modos.
- Listados de tareas, activos y clientes: toda la fila es clicable para acceder al detalle, eliminando el botón azul de "Ver" y mejorando la experiencia UX.
- En el detalle de cliente, la tabla de activos asociados también tiene filas clicables y botón de borrar activo.
- Corrección de referencias a campos y métodos inexistentes (como get_tipo_display en ForeignKey).
- Refactor de vistas y plantillas para mayor coherencia y limpieza visual.

## Pendiente de revisión visual
- Repasar el formato y alineación de columnas en todas las tablas (especialmente tareas y activos) para asegurar consistencia y legibilidad.
- Añadir el widget de usuario/logout en el header del dashboard (actualmente no visible, revisar si se eliminó o quedó sin incluir).

## Tareas centrales para la próxima sesión
- Implementar una tarea que cruce activos y CVE y genere alertas automáticamente.
- Automatizar ambos procesos (cruce y generación de alertas) mediante un cron job en el entorno de despliegue.

---

Buen trabajo hoy. Mañana más y mejor 🚀 

# Estado del Proyecto - Refactorización de Plantillas (junio 2024)

## Cambios estructurales recientes

- Se ha eliminado la plantilla `base.html` de la raíz y se ha dividido la herencia en dos bases especializadas:
  - `base_public.html`: para landing page y login, con `.container` y diseño centrado.
  - `base_dashboard.html`: para dashboard y todos los CRUD, sin `.container`, con layout de app (sidebar + main content), 100% alto.
- Todas las vistas internas (dashboard, CRUD, etc.) heredan ahora de `vuln_manager/dashboard/base.html`, que a su vez hereda de `base_dashboard.html`.
- Todas las vistas públicas (landing, login) heredan de `base_public.html`.
- Se han corregido las herencias de todas las plantillas, eliminando cualquier referencia a la antigua `base.html`.
- El layout del sidebar y el botón de logout ahora es coherente en todas las vistas internas.

## Observaciones y evolución

- El motivo inicial de la refactorización fue un problema visual con el botón de logout en el sidebar, que no se ha resuelto completamente: sigue sin comportarse como se esperaba en todas las situaciones.
- Durante el proceso, se ha mejorado la coherencia de la estructura de herencia y la separación de layouts, pero el resultado visual general es menos atractivo que el original.
- Se recomienda una revisión de estilos y layout para mejorar la experiencia visual, especialmente en el dashboard y el sidebar.

## Próximos pasos sugeridos

- Revisar y refinar el CSS del sidebar y el main content para lograr un resultado visual más profesional y atractivo.
- Considerar el uso de utilidades de Bootstrap/Mazer para el layout, evitando sobrescribir estilos a mano salvo que sea imprescindible.
- Documentar cualquier ajuste visual o funcional adicional en este archivo.

---

**Nota:** El proceso de refactorización ha dejado la base del proyecto más preparada para el crecimiento y el mantenimiento, aunque el problema visual original persiste y la estética general requiere mejoras. 

## Nota sobre tests en carpetas profundas (junio 2025)

- Cuando los tests se encuentran en rutas profundas (por ejemplo, `vuln_manager/tests/services/correlation/`), el comando `python manage.py test` de Django puede no detectarlos automáticamente, aunque el archivo y la clase sigan la convención de nombres.
- En estos casos, es recomendable ejecutar los tests usando `pytest`, que sí detecta correctamente los archivos y métodos de test en cualquier subcarpeta:

  ```sh
  docker compose exec vuln-manager-web pytest vuln_manager/tests/services/correlation/test_keyword_correlator.py -v
  ```

- Además, para la clase `KeywordCorrelator`, el método correcto para ejecutar la correlación es `correlate()`. Si se usa el nombre anterior `correlacionar()`, los tests fallarán con `AttributeError`.

- Si los tests no se detectan, revisar:
  - Que los métodos empiecen por `test_`.
  - Que la clase empiece por `Test`.
  - Que el archivo empiece por `test_`.
  - Probar con `pytest` si Django no los encuentra. 

- Refactorizada la lógica de correlación en `TaskExecutor` para que solo procese las CVEs nuevas o actualizadas desde la última ejecución exitosa del colector, usando el repositorio y pasando la lista de CVEs al correlador.
- Modificado `KeywordCorrelator` para aceptar una lista de CVEs a procesar y usarla en vez de consultar todas las vulnerabilidades.
- Añadido un test en `test_keyword_correlator.py` que verifica que el correlador solo procesa la lista de CVEs pasada por parámetro (simulando el filtrado por fecha).
- Todos los tests de correlación pasan correctamente tras la refactorización.
- Refactorizado `KeywordCorrelator` para usar el patrón repository en lugar de acceder directamente a los modelos: ahora usa `ActivoRepository`, `VulnerabilidadRepository`, `ActivoVulnerabilidadRepository` y `AlertaRepository`.
- Añadido método `get_by_activo_y_vulnerabilidad` al `AlertaRepository` para verificar alertas existentes.
- Todos los tests siguen pasando correctamente tras la refactorización a repositorios.
- Reutilizados los campos existentes de `EjecucionTarea` para las métricas de correlación:
  - `cves_procesadas` → CVEs procesadas (coincide)
  - `cves_nuevas` → Correlaciones creadas
  - `cves_actualizadas` → Alertas generadas
- Actualizado el template `tarea/detail.html` para mostrar las etiquetas correctas según el tipo de tarea.
- Verificado que la funcionalidad funciona correctamente: ejecución de prueba procesó 679 CVEs, creó 0 correlaciones nuevas y generó 15700 alertas. 