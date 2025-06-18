# Scripts de Inicialización y Mantenimiento

Este directorio contiene scripts para la inicialización y mantenimiento de la base de datos del proyecto Vuln-Asset-Manager.

## 📋 Scripts Disponibles

### 🚀 `init_project.sh`
**Propósito:** Script principal de inicialización para producción.
**Uso:** Se ejecuta automáticamente al arrancar el contenedor.

**Funciones:**
- Aplica migraciones
- Crea superusuario admin
- **Ejecuta `init_production.py` solo si la BD está vacía**
- Carga fixtures adicionales
- Arranca gunicorn

**Control de ejecución:**
- **Automático:** Solo se ejecuta si no hay datos existentes
- **Manual:** Usar `FORCE_INIT=true` para forzar la inicialización

### 🎯 `init_production.py`
**Propósito:** Inicialización completa de la base de datos para producción.
**Uso:** `python manage.py shell -c "exec(open('scripts/init_production.py').read())"`

**Funciones:**
- Limpia TODOS los datos existentes
- Crea tipos de tarea (cve_collector, cve_asset_correlation)
- Crea usuarios de demo (analistas y clientes)
- Crea activos de ejemplo
- **Asigna analistas a clientes de forma aleatoria**
- Muestra credenciales de acceso

### 🔄 `reset_production.py`
**Propósito:** Reset completo de la base de datos (solo para emergencias).
**Uso:** `python manage.py shell -c "exec(open('scripts/reset_production.py').read())"`

**Funciones:**
- **⚠️ ELIMINA TODOS LOS DATOS EXISTENTES**
- Requiere confirmación manual (escribir 'SI')
- Recrea toda la estructura desde cero
- Ideal para emergencias o cambios estructurales

### 🧹 `clean_database.py`
**Propósito:** Limpieza selectiva de datos de correlación.
**Uso:** `python manage.py shell -c "exec(open('scripts/clean_database.py').read())"`

**Funciones:**
- Elimina correlaciones y alertas
- Elimina ejecuciones de tareas de correlación
- Mantiene ejecuciones del colector
- Mantiene usuarios, clientes, activos y vulnerabilidades

### ⚡ `quick_clean.py`
**Propósito:** Limpieza rápida para desarrollo.
**Uso:** `python manage.py shell -c "exec(open('scripts/quick_clean.py').read())"`

**Funciones:**
- Solo elimina correlaciones y alertas
- Mantiene todo lo demás intacto
- Ideal para pruebas rápidas

### 📊 `populate_demo_data.py`
**Propósito:** Población de datos de demo (versión completa).
**Uso:** `python manage.py shell -c "exec(open('scripts/populate_demo_data.py').read())"`

**Funciones:**
- Crea tipos de tarea
- Crea muchos usuarios de demo
- Crea muchos activos de ejemplo
- **Asigna analistas a clientes de forma aleatoria**
- Ideal para desarrollo con datos realistas

## 🔧 Comandos de Uso

### Para Producción (primera vez):
```bash
# Se ejecuta automáticamente al arrancar el contenedor
docker compose up
```

### Para Limpieza Rápida (desarrollo):
```bash
docker compose exec vuln-manager-web python manage.py shell -c "exec(open('scripts/quick_clean.py').read())"
```

### Para Limpieza Selectiva:
```bash
docker compose exec vuln-manager-web python manage.py shell -c "exec(open('scripts/clean_database.py').read())"
```

### Para Reinicialización Completa:
```bash
docker compose exec vuln-manager-web python manage.py shell -c "exec(open('scripts/init_production.py').read())"
```

### Para Forzar Inicialización (ignorar datos existentes):
```bash
FORCE_INIT=true docker compose exec vuln-manager-web python manage.py shell -c "exec(open('scripts/init_production.py').read())"
```

### Para Datos de Demo Extensos:
```bash
docker compose exec vuln-manager-web python manage.py shell -c "exec(open('scripts/populate_demo_data.py').read())"
```

## 🔑 Credenciales por Defecto

### Admin:
- **Usuario:** `admin`
- **Contraseña:** `Admin123!`
- **Rol:** `admin`

### Analistas de Demo:
- **Usuarios:** `marta.garcia`, `juan.perez`, `ana.rodriguez`
- **Contraseña:** `renaido.`
- **Rol:** `analista`

### Clientes de Demo:
- **Usuarios:** `contacto_iberdrola`, `it_santander`, `admin_endesa`
- **Contraseña:** `renaido.`
- **Rol:** `cliente`

## 👥 Asignaciones de Analistas a Clientes

Los scripts `init_production.py` y `populate_demo_data.py` asignan automáticamente analistas a clientes:

### Lógica de Asignación:
- Cada cliente recibe entre 1 y 2 analistas aleatoriamente
- Un analista puede estar asignado a múltiples clientes
- Las asignaciones se crean usando la relación many-to-many del modelo

### Ejemplo de Asignaciones:
```
Iberdrola: ['juan.perez', 'marta.garcia']
Banco Santander: ['ana.rodriguez', 'marta.garcia']
Endesa: ['ana.rodriguez', 'marta.garcia']
```

### Verificar Asignaciones:
```bash
# Desde clientes
docker compose exec vuln-manager-web python manage.py shell -c "from vuln_manager.models import Cliente; clientes = Cliente.objects.all(); [print(f'{c.nombre}: {[a.username for a in c.analistas.all()]}') for c in clientes]"

# Desde analistas
docker compose exec vuln-manager-web python manage.py shell -c "from vuln_manager.models import Cliente, Usuario; analistas = Usuario.objects.filter(rol='analista'); [print(f'{a.username}: {[c.nombre for c in Cliente.objects.filter(analistas=a)]}') for a in analistas]"
```

## ⚠️ Notas Importantes

1. **`init_project.sh`** ahora solo inicializa si la BD está vacía
2. **`init_production.py`** elimina TODOS los datos existentes
3. **`reset_production.py`** requiere confirmación manual
4. **`clean_database.py`** mantiene usuarios, clientes, activos y vulnerabilidades
5. **`quick_clean.py`** es la opción más segura para desarrollo
6. Los scripts se ejecutan dentro del contenedor Docker
7. Siempre haz backup antes de ejecutar scripts de limpieza en producción

## 🎯 Flujo Recomendado

### Desarrollo:
1. Usar `quick_clean.py` para limpiar correlaciones
2. Usar `populate_demo_data.py` para datos extensos
3. Probar funcionalidad

### Producción:
1. Usar `init_project.sh` (automático, solo primera vez)
2. Configurar credenciales reales
3. Crear tareas programadas
4. Para cambios estructurales, usar `reset_production.py` con precaución