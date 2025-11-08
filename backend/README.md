# 🔐 Passd Backend# Passd Backend



**API REST para gestor de contraseñas open source**Passd Backend es la API para un gestor de contraseñas open source, diseñado para ejecutarse en Docker localmente. El objetivo principal es ofrecer transparencia y seguridad: el código es público para que cualquier usuario pueda verificar que sus datos no son utilizados indebidamente.



Passd Backend es una API segura y transparente para gestión de contraseñas, diseñada para ejecutarse localmente con Docker. El código es completamente open source para que cualquier usuario pueda auditar y verificar que sus datos nunca son expuestos.## Tecnologías principales

- **Django**: Framework principal para el backend.

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)- **Django REST Framework**: Para la creación de APIs RESTful.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)- **SimpleJWT**: Autenticación basada en JSON Web Tokens.

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)## Arquitectura y buenas prácticas

- **Clean Code & Clean Architecture**: El proyecto sigue principios de código limpio y arquitectura modular, priorizando la escalabilidad y mantenibilidad.

---- **Business Objects (BO)**: Las acciones principales (crear, actualizar, eliminar, etc.) se implementan en clases BO, separando la lógica de negocio de los serializers y views.

- **Serializers**: Se usan exclusivamente para validación y transformación de datos entre la API y los modelos.

## 🚀 Inicio Rápido- **Inyección de dependencias**: Se implementa donde sea necesario para mantener el código desacoplado y fácil de testear, pero siempre priorizando la simplicidad y claridad.



### Prerrequisitos## Funcionalidad principal

- Docker y Docker Compose instalados- **Gestión de contraseñas**: El backend almacena los datos encriptados que recibe del frontend. Cada ítem representa una contraseña asociada a una URL y un nombre de usuario. Además, cada ítem puede tener:

- Git  - Nota

  - Tags

### Instalación en 3 pasos  - Root (puede renombrarse a "folder" o similar para mayor claridad): permite agrupar ítems como si fueran carpetas.

- **Relación usuario-ítem**: Cada ítem está vinculado a un usuario.

```bash- **Usuarios**: El registro de usuarios se realiza con username, contraseña y salt, todos enviados por el frontend. Los usuarios heredan del modelo nativo de Django, pero se personalizan para funcionar diferente al panel de administración.

# 1. Clonar el repositorio

git clone https://github.com/MguevaraJ/passd.git## Seguridad y privacidad

cd passd/backend- **Open Source**: El código está disponible para que cualquier usuario pueda auditarlo.

- **Datos encriptados**: El backend nunca tiene acceso a las contraseñas en texto plano; solo almacena los datos encriptados enviados por el frontend.

# 2. Iniciar el proyecto

./start.sh## Desarrollo y despliegue

- **Docker**: El proyecto está pensado para ejecutarse en contenedores Docker en local.

# 3. Crear superusuario (opcional)- **Modularidad**: La estructura del proyecto permite agregar nuevas funcionalidades de forma sencilla y escalable.

make createsuperuser

```## Estructura recomendada

- `apps/`

**¡Listo!** Tu API está corriendo en:  - `users/`: Gestión de usuarios.

- 🌐 **API**: http://localhost:8000  - `keys/`: Gestión de ítems (contraseñas, notas, tags, root/folder).

- 📊 **Admin**: http://localhost:8000/admin/- `backend/`: Configuración principal de Django.

- 🗄️ **PostgreSQL**: localhost:5432

## Contribución

---Este proyecto está abierto a contribuciones. Se recomienda seguir las buenas prácticas descritas aquí para mantener la calidad y coherencia del código.



## 📋 Documentación

- **[DOCKER.md](DOCKER.md)** - Guía completa de Docker y comandos
- **[API Endpoints](#-endpoints-de-la-api)** - Documentación de la API REST
- **[Arquitectura](#-arquitectura)** - Estructura y buenas prácticas del proyecto

---

## 🛠️ Tecnologías

### Stack Principal
- **Django 5.2** - Framework web Python
- **Django REST Framework** - API RESTful
- **PostgreSQL 16** - Base de datos
- **JWT (SimpleJWT)** - Autenticación
- **Gunicorn** - Servidor WSGI
- **Docker** - Containerización

### Seguridad
- Encriptación end-to-end (cliente)
- Tokens JWT para autenticación
- PostgreSQL con credenciales configurables
- Usuario no-root en contenedores
- Variables de entorno para secrets

---

## 📁 Estructura del Proyecto

```
backend/
├── apps/
│   ├── users/          # Autenticación y usuarios
│   │   ├── models.py   # Modelo User personalizado
│   │   ├── views.py    # Login, Register
│   │   ├── serializers.py
│   │   └── bo/         # Business Objects
│   └── keys/           # Gestión de passwords
│       ├── models.py   # KeyItem, Folder
│       ├── v1/
│       │   ├── views.py
│       │   └── serializers.py
│       └── bo/         # Business Objects
├── backend/
│   ├── settings.py     # Configuración Django
│   └── urls.py         # Rutas principales
├── utils/
│   └── models.py       # BaseModel con Soft Delete
├── docker-compose.yml  # Orquestación Docker
├── Dockerfile          # Imagen del backend
├── requirements.txt    # Dependencias Python
├── Makefile           # Comandos útiles
└── entrypoint.sh      # Script de inicialización
```

---

## 🎯 Arquitectura

### Principios de Diseño

#### **Clean Architecture**
- Separación de responsabilidades
- Lógica de negocio independiente del framework
- Fácil de testear y mantener

#### **Business Objects (BO)**
```python
# Lógica de negocio centralizada
class ItemsBO:
    @staticmethod
    def create_item(user, **data):
        return KeyItem.objects.create(user=user, **data)
    
    @staticmethod
    def list_items(user):
        return KeyItem.objects.filter(user=user)
```

#### **Serializers para Validación**
```python
# Solo validación y transformación
class KeyItemSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['request'].user
        return ItemsBO.create_item(user=user, **validated_data)
```

#### **Soft Delete**
- Los registros nunca se eliminan físicamente
- Campo `deleted_at` para eliminación lógica
- Restauración de datos posible

### Modelos Principales

#### **User**
- Email como username
- Password hasheado por Django
- Salt personalizado del cliente
- Hereda de AbstractBaseUser

#### **KeyItem**
- URL, username, encrypted_pass (encriptado por cliente)
- Notas y tags opcionales
- Asociado a usuario y carpeta opcional
- Timestamps automáticos

#### **Folder**
- Organización de items
- Asociado a usuario
- Relación con KeyItems

---

## 🔌 Endpoints de la API

### Autenticación

#### Registro
```bash
POST /v1/users/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "hashed_password",
  "salt": "user_salt"
}
```

#### Login
```bash
POST /v1/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "hashed_password"
}

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Carpetas

```bash
GET    /v1/keys/folders/                 # Listar carpetas
POST   /v1/keys/folders/                 # Crear carpeta
GET    /v1/keys/folders/{id}/            # Ver carpeta
PUT    /v1/keys/folders/{id}/            # Actualizar carpeta
DELETE /v1/keys/folders/{id}/            # Eliminar carpeta
POST   /v1/keys/folders/{id}/add-item/   # Agregar item a carpeta
```

### Items (Passwords)

```bash
GET    /v1/keys/items/                   # Listar items
POST   /v1/keys/items/                   # Crear item
GET    /v1/keys/items/{id}/              # Ver item
PUT    /v1/keys/items/{id}/              # Actualizar item completo
PATCH  /v1/keys/items/{id}/              # Actualizar parcial
DELETE /v1/keys/items/{id}/              # Eliminar item
PATCH  /v1/keys/items/{id}/tags/         # Actualizar solo tags
```

**Nota:** Todos los endpoints (excepto register/login) requieren header:
```
Authorization: Bearer {access_token}
```

---

## 💻 Comandos de Desarrollo

### Usando Make (recomendado)

```bash
make help              # Ver todos los comandos
make up                # Iniciar servicios
make down              # Detener servicios
make logs              # Ver logs
make logs-backend      # Ver logs del backend
make shell             # Django shell
make migrate           # Ejecutar migraciones
make makemigrations    # Crear migraciones
make createsuperuser   # Crear admin
make seed-data         # 🌱 Crear datos de prueba
make test              # Ejecutar tests
make db-backup         # Backup de PostgreSQL
make clean             # Limpiar contenedores
```

### Usando Docker Compose directamente

```bash
docker-compose up -d                                    # Iniciar
docker-compose logs -f backend                          # Logs
docker-compose exec backend python manage.py migrate   # Migraciones
docker-compose exec backend python manage.py shell     # Shell
docker-compose down                                     # Detener
```

---

## 🔐 Seguridad y Privacidad

### Principios de Seguridad

1. **Encriptación Client-Side**
   - Las contraseñas se encriptan en el cliente
   - El backend solo almacena datos encriptados
   - Nunca tenemos acceso a contraseñas en texto plano

2. **Autenticación JWT**
   - Tokens de corta duración (5 minutos)
   - Refresh tokens para renovación
   - Sin sesiones en servidor (stateless)

3. **Open Source Audit**
   - Código completamente público
   - Cualquiera puede verificar seguridad
   - Transparencia total

4. **Aislamiento Docker**
   - Red privada entre servicios
   - PostgreSQL no expuesto externamente
   - Contenedores con usuarios no-root

5. **Variables de Entorno**
   - Secrets en `.env` (no commiteados)
   - Configuración separada del código
   - Diferente config para dev/prod

---

## 🧪 Testing

```bash
# Todos los tests
make test

# Tests específicos
docker-compose exec backend python manage.py test apps.users
docker-compose exec backend python manage.py test apps.keys

# Con coverage
docker-compose exec backend python manage.py test --with-coverage
```

---

## 🔧 Configuración

### Variables de Entorno

Edita `.env` para personalizar:

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=passd_db
DB_USER=passd_user
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432

# PostgreSQL
POSTGRES_DB=passd_db
POSTGRES_USER=passd_user
POSTGRES_PASSWORD=your-secure-password
```

Ver `.env.example` para todas las opciones.

---

## 🐛 Troubleshooting

### Puerto 8000 en uso
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"
```

### Problemas con migraciones
```bash
make down
make clean
make setup
```

### Ver logs de errores
```bash
make logs-backend
```

### PostgreSQL no inicia
```bash
docker-compose down -v  # Elimina volúmenes
docker-compose up -d
```

---

## 📚 Más Documentación

- **[DOCKER.md](DOCKER.md)** - Guía completa de Docker
- **[Makefile](Makefile)** - Ver comandos disponibles
- **Bruno Collection** - Colección de requests en `/bruno-collection`

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Seguir principios de Clean Code
- Usar Business Objects para lógica de negocio
- Escribir tests para nuevas features
- Documentar endpoints nuevos
- Mantener consistencia con arquitectura existente

---

## 🌱 Datos de Prueba

### Crear Datos de Prueba Automáticamente

El proyecto incluye un comando para crear usuarios, carpetas e items de prueba:

```bash
make seed-data
```

Esto creará:
- **3 usuarios**: superadmin, test user y demo user
- **4 carpetas**: Redes Sociales, Trabajo, Bancos, Personal
- **8 items de prueba**: 6 en carpetas + 2 sin clasificar (Netflix, Spotify)

### Credenciales de Prueba

```
Superusuario (acceso al admin):
  Email: admin@passd.local
  Password: admin123
  Salt: admin_salt_123

Usuario de prueba (con datos):
  Email: test@passd.com
  Password: test123
  Salt: test_salt_456

Usuario demo (sin datos):
  Email: demo@passd.com
  Password: demo123
  Salt: demo_salt_789
```

### Recrear Datos (⚠️ Elimina todo)

```bash
make seed-data-clear
```

Este comando elimina TODOS los datos existentes y crea datos frescos de prueba.

---

## 📝 Licencia

Este proyecto es de código abierto. Ver el archivo LICENSE para más detalles.

---

## 👤 Autor

**Antonio Guevara**
- GitHub: [@MguevaraJ](https://github.com/MguevaraJ)

---

## ⭐ Agradecimientos

Este proyecto fue diseñado con:
- Transparencia y seguridad como prioridades
- Clean Architecture y SOLID principles
- Docker para desarrollo consistente
- Open Source para auditabilidad completa

---

**¿Necesitas ayuda?** Abre un issue en GitHub o revisa la [documentación de Docker](DOCKER.md).
