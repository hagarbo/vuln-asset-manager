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

## 📝 Registro de Cambios

### 2024-03-19: Reorganización de Formularios y Tests
- **Motivo**: Mejorar la organización del código siguiendo las convenciones de Django y TDD
- **Cambios**:
  1. Reorganización de formularios:
     ```
     vuln_manager/
         forms/
             __init__.py
             usuario_creation.py
             usuario_change.py
     ```
  2. Separar cada formulario en su propio archivo:
     - `usuario_creation.py`: Formulario para crear nuevos usuarios
     - `usuario_change.py`: Formulario para modificar usuarios existentes
  3. Crear `__init__.py` para exponer los formularios
  4. Eliminar el archivo `forms.py` original
  5. Actualizar importaciones en `auth_views.py`
  6. Crear estructura de tests:
     ```
     vuln_manager/
         tests/
             forms/
                 __init__.py
                 test_usuario_creation.py
                 test_usuario_change.py
     ```
  7. Implementar tests unitarios:
     - Tests para UsuarioCreationForm:
       - Validación de datos correctos
       - Validación de email
       - Validación de contraseñas
       - Campos requeridos
       - Guardado de usuario
     - Tests para UsuarioChangeForm:
       - Validación de datos correctos
       - Validación de email
       - Campo email requerido
       - Guardado de cambios
       - Exclusión de password
  8. Correcciones realizadas:
     - Eliminar referencias a campos obsoletos en modelo Usuario
     - Mejorar la exclusión de campos de contraseña en UsuarioChangeForm
- **Resultados**:
  - ✅ 10 tests implementados
  - ✅ Todos los tests pasando
  - ✅ Cobertura completa de funcionalidad básica
- **Beneficios**:
  - Mejor organización y mantenibilidad
  - Seguimiento de convenciones Django
  - Facilita la reutilización de código
  - Mejora la legibilidad
  - Cobertura de tests para validar funcionalidad
- **Próximos pasos**:
  - Documentar la nueva estructura en el README
  - Revisar y actualizar la documentación existente
  - Considerar añadir más tests para casos edge

### 2024-03-20: Reorganización de la Estructura del Proyecto
- **Motivo**: Mejorar la organización del código siguiendo un patrón por entidad
- **Plan de Reorganización**:
  1. Estructura de Formularios:
     ```
     vuln_manager/
         forms/
             usuario/
                 __init__.py
                 creation.py
                 change.py
             activo/
                 __init__.py
                 creation.py
                 update.py
             vulnerabilidad/
                 __init__.py
             cliente/
                 __init__.py
             tarea/
                 __init__.py
             alerta/
                 __init__.py
     ```
  2. Estructura de Vistas:
     ```
     vuln_manager/
         views/
             usuario/
                 __init__.py
                 auth.py
                 profile.py
             activo/
                 __init__.py
                 list.py
                 detail.py
                 create.py
                 update.py
             vulnerabilidad/
                 __init__.py
             cliente/
                 __init__.py
             tarea/
                 __init__.py
             alerta/
                 __init__.py
     ```
  3. Estructura de Tests:
     ```
     vuln_manager/
         tests/
             forms/
                 usuario/
                     __init__.py
                     test_creation.py
                     test_change.py
                 activo/
                     __init__.py
                     test_creation.py
                     test_update.py
                 vulnerabilidad/
                     __init__.py
                 cliente/
                     __init__.py
                 tarea/
                     __init__.py
                 alerta/
                     __init__.py
             views/
                 usuario/
                     __init__.py
                     test_auth.py
                     test_profile.py
                 activo/
                     __init__.py
                     test_list.py
                     test_detail.py
                     test_create.py
                     test_update.py
                 vulnerabilidad/
                     __init__.py
                 cliente/
                     __init__.py
                 tarea/
                     __init__.py
                 alerta/
                     __init__.py
     ```
- **Beneficios**:
  - Mejor organización por dominio/entidad
  - Más fácil de mantener y escalar
  - Mejor separación de responsabilidades
  - Más fácil de encontrar el código relacionado
  - Facilita el trabajo en equipo
  - Mejora la reutilización de código
- **Plan de Implementación**:
  1. Empezar con la entidad Activo
  2. Crear la estructura de carpetas
  3. Mover y refactorizar el código existente
  4. Implementar tests unitarios
  5. Verificar que todo funciona correctamente
  6. Repetir el proceso con las demás entidades

### 2024-03-20: Implementación de Formularios de Activo
- **Cambios realizados**:
  1. Creación de la estructura de carpetas para Activo:
     - `forms/activo/`
     - `tests/forms/activo/`
  2. Implementación de formularios:
     - `ActivoCreationForm`: Para crear nuevos activos
     - `ActivoUpdateForm`: Para actualizar activos existentes
  3. Implementación de tests:
     - Tests para validación de datos
     - Tests para campos requeridos
     - Tests para campos opcionales
     - Tests para limpieza de datos
     - Tests para guardado de datos
- **Estado actual**:
  - ✅ Estructura de carpetas creada
  - ✅ Formularios implementados
  - ✅ Tests implementados
  - ⏳ Pendiente verificar funcionamiento de tests
  - ⏳ Pendiente integrar con vistas existentes

### 2024-03-20: Creación de Estructura Base para Todas las Entidades
- **Cambios realizados**:
  1. Creación de carpetas para todas las entidades:
     - Vulnerabilidad
     - Cliente
     - Tarea
     - Alerta
  2. Creación de archivos `__init__.py` en todas las carpetas
  3. Renombrado de `relacion_analista_cliente.py` a `analista_cliente.py` por consistencia
  4. Renombrado de la clase `RelacionAnalistaCliente` a `AnalistaCliente` por consistencia
- **Estado actual**:
  - ✅ Estructura base creada para todas las entidades
  - ✅ Archivos `__init__.py` creados
  - ✅ Modelo renombrado por consistencia
  - ✅ Clase renombrada por consistencia
  - ⏳ Pendiente implementar formularios y tests para cada entidad

### 2024-03-20: Actualización de la documentación
- **Motivo**: Actualizar la documentación para reflejar los cambios realizados
- **Cambios**:
  - Actualización de las reglas del proyecto
  - Documentación de la nueva estructura
  - Registro de cambios realizados
  - Plan de implementación actualizado
  - Actualización de las convenciones de nombrado
- **Beneficios**:
  - Mejorar la legibilidad y claridad de la documentación
  - Facilitar la comprensión de los resultados de los tests
- **Próximos pasos**:
  - Revisar y actualizar la documentación existente
  - Considerar añadir más tests para casos edge 

## 2024-03-19: Reorganización de modelos por dominio

### Motivación
Para mejorar la organización y mantenibilidad del código, se ha reorganizado la estructura de los modelos siguiendo un enfoque basado en dominios. Esto permite una mejor separación de responsabilidades y facilita la navegación del código.

### Cambios realizados
1. Creación de directorios por dominio:
   - `auth/`: Modelos relacionados con autenticación y usuarios
   - `clientes/`: Modelos relacionados con clientes y sus relaciones
   - `activos/`: Modelos relacionados con activos y sus vulnerabilidades
   - `vulnerabilidades/`: Modelos relacionados con vulnerabilidades
   - `tareas/`: Modelos relacionados con tareas y su ejecución
   - `alertas/`: Modelos relacionados con alertas

2. Reorganización de archivos:
   - Movimiento de modelos a sus respectivos directorios
   - Actualización de importaciones en `__init__.py`
   - Creación de `__init__.py` en cada subdirectorio

3. Beneficios:
   - Mejor organización del código
   - Separación clara de responsabilidades
   - Facilidad para encontrar y mantener modelos relacionados
   - Mejor escalabilidad para futuros modelos 

## Refactorizaciones Realizadas

### 1. Organización de Templates
- Se ha reorganizado la estructura de templates siguiendo un patrón por entidad:
  ```
  vuln_manager/templates/vuln_manager/
  ├── activos/
  │   ├── list.html
  │   └── detail.html
  ├── clientes/
  │   ├── list.html
  │   └── detail.html
  ├── vulnerabilidades/
  │   ├── list.html
  │   └── detail.html
  └── components/
      ├── navbar.html
      ├── messages.html
      ├── list_actions.html
      └── detail_actions.html
  ```

### 2. Gestión de Formularios
- Se ha reorganizado la estructura de formularios en módulos separados:
  ```
  vuln_manager/forms/
  ├── usuario/
  │   ├── __init__.py
  │   ├── creation.py (UsuarioCreationForm)
  │   └── change.py (UsuarioChangeForm)
  ```
- Se han corregido las importaciones en las vistas para usar la ruta correcta:
  ```python
  from vuln_manager.forms.usuario import UsuarioCreationForm, UsuarioChangeForm
  ```

### 3. Filtros de Template
- Se han implementado filtros personalizados en `vuln_manager/templatetags/vuln_manager_filters.py`:
  - `severity_to_css_class`: Mapea severidades a clases CSS
  - `status_to_css_class`: Mapea estados a clases Bootstrap
- **Nota**: Investigar una solución alternativa para el sistema de templatetags, ya que la implementación actual podría no ser la más óptima.

### 4. Estilos CSS
- Se ha implementado un sistema de estilos para severidades en `vuln_manager/static/css/severity.css`
- Los estilos incluyen:
  - Colores específicos para cada nivel de severidad
  - Estilos para badges
  - Estilos para filas de tabla
  - Clases para elementos clickeables

### 5. Correcciones de Base de Datos
- Se han aplicado las migraciones pendientes
- Se ha cargado el fixture inicial con datos de prueba
- Se ha actualizado la contraseña del usuario admin

### 6. Problemas Resueltos
1. Error de importación de formularios:
   - Se corrigió la ruta de importación en `auth_views.py`
   - Se comentaron temporalmente las importaciones no utilizadas

2. Error de tabla `django_session`:
   - Se aplicaron las migraciones pendientes
   - Se cargaron los datos iniciales del fixture

3. Estilos de vulnerabilidades:
   - Se implementaron los filtros necesarios
   - Se aseguró la correcta carga de archivos estáticos

### 7. Pendiente
- Implementar los formularios para las entidades principales (Cliente, Activo, Vulnerabilidad)
- Revisar y actualizar las vistas para usar los nuevos formularios
- Completar la implementación de los templates de formularios
- Investigar y proponer una solución alternativa para el sistema de templatetags

### 8. Notas Importantes
- La estructura del proyecto sigue las convenciones de Django
- Se mantiene la separación de responsabilidades
- Los archivos estáticos están correctamente organizados
- Se han seguido las buenas prácticas de desarrollo 

## 13/06/2025 - Refactorización de formularios para usar el patrón Repository

- Se refactorizaron los formularios de Activo (`ActivoCreationForm` y `ActivoUpdateForm`) para que utilicen el `ActivoRepository` en lugar de guardar directamente el modelo.
- Se refactorizaron los formularios de Usuario (`UsuarioCreationForm` y `UsuarioChangeForm`) para que utilicen el `UsuarioRepository` en lugar de guardar directamente el modelo.
- Se crearon tests para verificar que los formularios utilizan correctamente el patrón Repository.
- Se ejecutaron los tests de los formularios de Activo y Usuario, y todos pasaron correctamente.

Este avance garantiza que los formularios de Activo y Usuario están completamente alineados con el patrón Repository y listos para futuras ampliaciones o refactorizaciones. 

## 13/06/2025 - Refactorización de vistas para usar el patrón Repository

- Se refactorizaron las vistas de Activo (`ActivoListView`, `ActivoDetailView`, `ActivoCreateView`, `ActivoUpdateView`, `ActivoDeleteView`) para que utilicen el `ActivoRepository` en lugar de acceder directamente al modelo.
- Se actualizaron los métodos `get_queryset`, `form_valid` y `delete` para utilizar los métodos del repositorio correspondientes.
- Se ejecutaron los tests de las vistas de Activo, y todos pasaron correctamente.

Este avance garantiza que las vistas de Activo están completamente alineadas con el patrón Repository y listas para futuras ampliaciones o refactorizaciones. 

## Cambios Realizados

### Reorganización de ActivoVulnerabilidad

1. Se movió el modelo `ActivoVulnerabilidad` de `vuln_manager/models/activo/` a `vuln_manager/models/vulnerabilidad/` siguiendo las mejores prácticas de Django para relaciones many-to-many con modelo intermedio.

2. Se actualizaron las importaciones en:
   - `vuln_manager/models/__init__.py`
   - `vuln_manager/models/vulnerabilidad/__init__.py`
   - `vuln_manager/views/__init__.py`
   - `vuln_manager/views/activo_views.py`
   - `vuln_manager/views/vulnerabilidad_views.py`
   - `vuln_manager/views/activo_vulnerabilidad_views.py`
   - `vuln_manager/admin.py`
   - `vuln_manager/tests/test_models.py`
   - `vuln_manager/urls.py`
   - `vuln_manager/templatetags/vuln_manager_filters.py`
   - `vuln_manager/templates/vuln_manager/activos/detail.html`

3. Se unificaron los filtros de plantilla:
   - Se eliminó el filtro `estado_to_css_class`
   - Se mantuvo `status_to_css_class` como filtro único para estados
   - Se actualizaron los estados en el diccionario de clases CSS

4. Se actualizaron las URLs:
   - Se cambió el prefijo de `activovulnerabilidad` a `activo-vulnerabilidad`
   - Se añadieron las URLs para listar y ver detalles
   - Se actualizaron los nombres de las URLs para seguir el patrón de nomenclatura

5. Se actualizaron las plantillas:
   - Se simplificó la plantilla de detalle de activo
   - Se actualizaron las referencias a los filtros
   - Se mejoró la presentación de las vulnerabilidades asociadas

## Próximos Pasos

1. Revisar y actualizar las plantillas restantes que puedan estar usando el filtro antiguo.
2. Verificar que todas las funcionalidades relacionadas con `ActivoVulnerabilidad` sigan funcionando correctamente.
3. Actualizar la documentación del proyecto para reflejar la nueva estructura.
4. Considerar la reorganización de otros modelos similares siguiendo las mejores prácticas de Django. 