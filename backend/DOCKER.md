# 🐳 Docker Setup - Passd Backend

Este proyecto Django utiliza Docker y Docker Compose para un entorno de desarrollo consistente y fácil de configurar.

## 📋 Prerrequisitos

- Docker (v20.10+)
- Docker Compose (v2.0+)

## 🚀 Inicio Rápido

### 1. Configuración inicial

```bash
# Copiar archivo de variables de entorno
cp .env.example .env

# Editar .env con tus configuraciones (opcional para desarrollo)
nano .env
```

### 2. Levantar el proyecto

```bash
# Opción 1: Usando Make (recomendado)
make setup

# Opción 2: Usando docker-compose directamente
docker-compose up --build -d
docker-compose exec backend python manage.py migrate
```

### 3. Acceder a la aplicación

- **API Backend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **PostgreSQL**: localhost:5432

## 🛠️ Comandos Disponibles

### Usando Make (recomendado)

```bash
# Ver todos los comandos disponibles
make help

# Comandos principales
make up              # Iniciar servicios
make down            # Detener servicios
make logs            # Ver logs de todos los servicios
make logs-backend    # Ver logs solo del backend
make restart         # Reiniciar servicios

# Django commands
make migrate         # Ejecutar migraciones
make makemigrations  # Crear nuevas migraciones
make shell           # Abrir Django shell
make createsuperuser # Crear superusuario
make seed-data       # 🌱 Crear datos de prueba
make test            # Ejecutar tests

# Base de datos
make db-shell        # Abrir PostgreSQL shell
make db-backup       # Hacer backup de la base de datos
make db-restore file=backup.sql  # Restaurar base de datos

# Desarrollo
make dev             # Iniciar con logs en tiempo real
make dev-build       # Reconstruir y iniciar

# Limpieza
make clean           # Limpiar contenedores y volúmenes
make clean-all       # Limpieza profunda (incluye imágenes)
```

### Usando Docker Compose directamente

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Ejecutar comandos Django
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py shell

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose up --build -d
```

## 📦 Servicios

### Backend (Django)
- **Puerto**: 8000
- **Imagen**: Construida desde Dockerfile local
- **Comando**: Gunicorn con hot-reload en desarrollo
- **Volúmenes**: 
  - Código fuente (hot-reload)
  - Static files
  - Media files

### Database (PostgreSQL)
- **Puerto**: 5432
- **Versión**: PostgreSQL 16 Alpine
- **Volumen**: Persistente para datos

## 🔧 Configuración

### Variables de Entorno

Edita el archivo `.env` para configurar:

```bash
# Django
DJANGO_SECRET_KEY=tu-secret-key-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=passd_db
DB_USER=passd_user
DB_PASSWORD=tu-password-seguro
DB_HOST=db
DB_PORT=5432

# PostgreSQL
POSTGRES_DB=passd_db
POSTGRES_USER=passd_user
POSTGRES_PASSWORD=tu-password-seguro
```

### Crear Superusuario

```bash
# Método 1: Interactivo
make createsuperuser

# Método 2: Con docker-compose
docker-compose exec backend python manage.py createsuperuser
```

### Datos de Prueba 🌱

Para desarrollo rápido, puedes crear usuarios, carpetas e items de prueba:

```bash
# Crear datos de prueba
make seed-data
```

Esto creará:
- **3 usuarios**: superadmin, test user y demo user
- **4 carpetas**: Redes Sociales, Trabajo, Bancos, Personal
- **8 items de prueba**: 6 en carpetas + 2 sin clasificar (Netflix, Spotify)

**Credenciales creadas:**
```
Superusuario:
  Email: admin@passd.local
  Password: admin123
  Salt: admin_salt_123

Usuario de prueba:
  Email: test@passd.com
  Password: test123
  Salt: test_salt_456
```

**Recrear datos (⚠️ Elimina todo):**
```bash
make seed-data-clear
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
make test

# O directamente con docker-compose
docker-compose exec backend python manage.py test

# Tests específicos
docker-compose exec backend python manage.py test apps.users
docker-compose exec backend python manage.py test apps.keys
```

## 📊 Base de Datos

### Backup

```bash
# Crear backup
make db-backup

# Manualmente
docker-compose exec -T db pg_dump -U passd_user passd_db > backup_$(date +%Y%m%d).sql
```

### Restaurar

```bash
# Restaurar desde backup
make db-restore file=backup_20241107.sql

# Manualmente
docker-compose exec -T db psql -U passd_user -d passd_db < backup_20241107.sql
```

### Acceder a PostgreSQL

```bash
# Shell de PostgreSQL
make db-shell

# O con docker-compose
docker-compose exec db psql -U passd_user -d passd_db
```

## 🐛 Troubleshooting

### Puerto 8000 ya está en uso

```bash
# Ver qué proceso usa el puerto
lsof -i :8000

# Cambiar puerto en docker-compose.yml
# ports:
#   - "8001:8000"  # Puerto 8001 en tu máquina
```

### Puerto 5432 ya está en uso

```bash
# Cambiar puerto de PostgreSQL
# ports:
#   - "5433:5432"  # Puerto 5433 en tu máquina
```

### Permisos en Linux

```bash
# Si tienes problemas de permisos con volúmenes
sudo chown -R $USER:$USER .
```

### Reiniciar todo desde cero

```bash
# Limpiar todo
make clean-all

# Reiniciar setup
make setup
```

### Ver estado de servicios

```bash
make status
# o
docker-compose ps
```

## 🔄 Hot Reload

El código se actualiza automáticamente cuando haces cambios gracias a:
- Volumen montado del código fuente
- Gunicorn con flag `--reload`

No necesitas reiniciar el contenedor al modificar archivos Python.

## 📝 Logs

```bash
# Todos los logs
make logs

# Solo backend
make logs-backend

# Solo base de datos
make logs-db

# Seguir logs en tiempo real
docker-compose logs -f
```

## 🔐 Seguridad

### Para Producción

1. Cambia `DJANGO_SECRET_KEY` a un valor seguro y único
2. Configura `DJANGO_DEBUG=False`
3. Actualiza `DJANGO_ALLOWED_HOSTS` con tus dominios
4. Usa contraseñas seguras para PostgreSQL
5. Habilita HTTPS/SSL
6. Considera usar Docker Secrets para información sensible

## 📚 Estructura de Archivos Docker

```
backend/
├── Dockerfile              # Imagen del backend
├── docker-compose.yml      # Orquestación de servicios
├── entrypoint.sh          # Script de inicialización
├── requirements.txt        # Dependencias Python
├── .env.example           # Template de variables de entorno
├── .env                   # Variables de entorno (no commitear)
├── .dockerignore          # Archivos ignorados en build
├── Makefile              # Comandos útiles
└── DOCKER_README.md      # Esta guía
```

## 🤝 Contribuir

1. Haz cambios en tu código
2. Las migraciones se ejecutan automáticamente al iniciar
3. Los tests deben pasar: `make test`
4. Commit y push

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs: `make logs`
2. Verifica el estado: `make status`
3. Intenta reiniciar: `make restart`
4. Como último recurso: `make clean && make setup`

---

**¡Feliz desarrollo! 🚀**
