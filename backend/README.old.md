# Passd Backend

Passd Backend es la API para un gestor de contraseñas open source, diseñado para ejecutarse en Docker localmente. El objetivo principal es ofrecer transparencia y seguridad: el código es público para que cualquier usuario pueda verificar que sus datos no son utilizados indebidamente.

## Tecnologías principales
- **Django**: Framework principal para el backend.
- **Django REST Framework**: Para la creación de APIs RESTful.
- **SimpleJWT**: Autenticación basada en JSON Web Tokens.

## Arquitectura y buenas prácticas
- **Clean Code & Clean Architecture**: El proyecto sigue principios de código limpio y arquitectura modular, priorizando la escalabilidad y mantenibilidad.
- **Business Objects (BO)**: Las acciones principales (crear, actualizar, eliminar, etc.) se implementan en clases BO, separando la lógica de negocio de los serializers y views.
- **Serializers**: Se usan exclusivamente para validación y transformación de datos entre la API y los modelos.
- **Inyección de dependencias**: Se implementa donde sea necesario para mantener el código desacoplado y fácil de testear, pero siempre priorizando la simplicidad y claridad.

## Funcionalidad principal
- **Gestión de contraseñas**: El backend almacena los datos encriptados que recibe del frontend. Cada ítem representa una contraseña asociada a una URL y un nombre de usuario. Además, cada ítem puede tener:
  - Nota
  - Tags
  - Root (puede renombrarse a "folder" o similar para mayor claridad): permite agrupar ítems como si fueran carpetas.
- **Relación usuario-ítem**: Cada ítem está vinculado a un usuario.
- **Usuarios**: El registro de usuarios se realiza con username, contraseña y salt, todos enviados por el frontend. Los usuarios heredan del modelo nativo de Django, pero se personalizan para funcionar diferente al panel de administración.

## Seguridad y privacidad
- **Open Source**: El código está disponible para que cualquier usuario pueda auditarlo.
- **Datos encriptados**: El backend nunca tiene acceso a las contraseñas en texto plano; solo almacena los datos encriptados enviados por el frontend.

## Desarrollo y despliegue
- **Docker**: El proyecto está pensado para ejecutarse en contenedores Docker en local.
- **Modularidad**: La estructura del proyecto permite agregar nuevas funcionalidades de forma sencilla y escalable.

## Estructura recomendada
- `apps/`
  - `users/`: Gestión de usuarios.
  - `keys/`: Gestión de ítems (contraseñas, notas, tags, root/folder).
- `backend/`: Configuración principal de Django.

## Contribución
Este proyecto está abierto a contribuciones. Se recomienda seguir las buenas prácticas descritas aquí para mantener la calidad y coherencia del código.

