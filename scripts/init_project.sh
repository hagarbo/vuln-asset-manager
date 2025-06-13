#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Iniciando configuración del proyecto...${NC}"

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo -e "${GREEN}Creando archivo .env...${NC}"
    cp .env.example .env
fi

# Construir y levantar contenedores
echo -e "${GREEN}Construyendo contenedores Docker...${NC}"
docker-compose build

echo -e "${GREEN}Levantando contenedores...${NC}"
docker-compose up -d

# Esperar a que la base de datos esté lista
echo -e "${GREEN}Esperando a que la base de datos esté lista...${NC}"
sleep 10

# Aplicar migraciones
echo -e "${GREEN}Aplicando migraciones...${NC}"
docker-compose exec web python manage.py migrate

# Crear superusuario
echo -e "${GREEN}Creando superusuario...${NC}"
docker-compose exec web python manage.py createsuperuser

echo -e "${BLUE}¡Configuración completada!${NC}"
echo -e "Puedes acceder a la aplicación en: http://localhost:8000"
echo -e "Panel de administración: http://localhost:8000/admin" 