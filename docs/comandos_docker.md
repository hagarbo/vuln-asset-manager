# Comandos para reiniciar el proyecto desde cero

## Reinicio completo del entorno Docker

### 1. Detener y eliminar todos los contenedores y volúmenes
```sh
docker compose down -v
```

### 2. Eliminar manualmente el volumen de datos de PostgreSQL (por si acaso)
```sh
docker volume rm vuln_manager_postgres_data
```

### 3. Reconstruir las imágenes
```sh
docker compose build
```

### 4. Levantar los contenedores
```sh
docker compose up -d
```

### 5. Aplicar las migraciones
```sh
docker compose exec vuln-manager-web python manage.py migrate
```

### 6. Cargar los datos de prueba
```sh
docker compose exec vuln-manager-web python manage.py loaddata vuln_manager/fixtures/initial_data.json
```

### 7. Verificar que todo funciona
```sh
docker compose ps
```

### 8. Ver los logs si hay algún problema
```sh
docker compose logs vuln-manager-web
docker compose logs db
```

## Comandos útiles adicionales

### Acceder a la consola de PostgreSQL
```sh
docker compose exec db psql -U postgres -d postgres
```

### Comandos útiles dentro de PostgreSQL
- `\dt` - Listar todas las tablas
- `\l` - Listar todas las bases de datos
- `\q` - Salir de la consola de PostgreSQL

### Ver el estado de los contenedores
```sh
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Ver los logs en tiempo real
```sh
docker compose logs -f
```

## Notas importantes
- Si se experimentan problemas con la base de datos, es recomendable eliminar completamente los volúmenes y empezar desde cero.
- El comando `docker compose down -v` elimina todos los contenedores y volúmenes asociados.
- El comando `docker volume rm vuln_manager_postgres_data` elimina específicamente el volumen de datos de PostgreSQL.
- Siempre asegúrate de que las migraciones se apliquen antes de cargar los datos de prueba.
- El servicio de la base de datos se llama `db` en el docker-compose.yml, no `vuln-manager-db`.
- La base de datos por defecto se llama `postgres`, no `vuln_manager`. 