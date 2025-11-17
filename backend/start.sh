#!/bin/bash

echo "🐳 ================================================"
echo "   Passd Backend - Docker Quick Start"
echo "================================================ 🐳"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

echo "✅ Docker está corriendo"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo "⚠️  Revisa el archivo .env y ajusta las configuraciones si es necesario"
    echo ""
fi

# Build images
echo "🔨 Construyendo imágenes Docker..."
docker compose build

echo ""
echo "🚀 Iniciando servicios..."
docker compose up -d

echo ""
echo "⏳ Esperando que los servicios estén listos..."
sleep 15

echo ""
echo "📦 Ejecutando migraciones..."
docker compose exec backend python manage.py migrate

echo ""
echo "================================================"
echo "✅ ¡Configuración completa!"
echo "================================================"
echo ""
echo "🌐 Backend API: http://localhost:8000"
echo "📊 Admin Panel: http://localhost:8000/admin/"
echo "🗄️  PostgreSQL: localhost:5432"
echo ""
echo "📋 Comandos útiles:"
echo "   make logs          - Ver logs"
echo "   make shell         - Django shell"
echo "   make createsuperuser - Crear superusuario"
echo "   make down          - Detener servicios"
echo "   make help          - Ver todos los comandos"
echo ""
echo "🎉 ¡Listo para desarrollar!"
echo ""
