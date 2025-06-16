# Estado del Proyecto Vuln-Asset-Manager

## 🚨 REGLAS MUY IMPORTANTES 🚨

### Estructura y Organización
1. **Una clase, un archivo**: Cada clase debe estar en su propio archivo. Para grupos relacionados (como formularios), crear una carpeta específica.
2. **Organización jerárquica**: Seguir las convenciones de Django para la estructura de carpetas.
3. **Carpeta raíz limpia**: Mantener solo los archivos estrictamente necesarios en la raíz del proyecto.
4. **Crecimiento controlado**: No añadir nueva funcionalidad hasta que la existente esté completamente probada y funcionando.
5. **Consistencia en nombres**: 
   - Mantener consistencia en el nombrado de archivos y modelos
   - Para modelos de relación, usar el formato `entidad1_entidad2.py` (ej: `activo_vulnerabilidad.py`, `analista_cliente.py`)
   - Para clases de modelos de relación, usar el formato `Entidad1Entidad2` (ej: `ActivoVulnerabilidad`, `AnalistaCliente`)

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

## 📝 Registro de Cambios

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