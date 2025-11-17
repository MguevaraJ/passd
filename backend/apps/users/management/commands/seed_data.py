"""
Comando personalizado para crear datos de prueba (seed data)
Uso: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.keys.models import Folder, KeyItem

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea datos de prueba para desarrollo: usuarios, carpetas e items'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los datos antes de crear nuevos (peligroso)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=' * 60))
        self.stdout.write(self.style.WARNING('🌱 Iniciando creación de datos de prueba...'))
        self.stdout.write(self.style.WARNING('=' * 60))
        
        # Opcional: limpiar datos existentes
        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Limpiando datos existentes...'))
            KeyItem.objects.all().delete()
            Folder.objects.all().delete()
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Datos eliminados'))
        
        # Crear superusuario
        self.stdout.write('\n📋 Creando usuarios...')
        admin, created = User.objects.get_or_create(
            email='admin@passd.local',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'salt': 'admin_salt_123',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Superusuario creado: {admin.email}'))
            self.stdout.write(self.style.SUCCESS(f'   Username: {admin.username}'))
            self.stdout.write(self.style.SUCCESS(f'   Password: admin123'))
            self.stdout.write(self.style.SUCCESS(f'   Salt: admin_salt_123'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Superusuario ya existe: {admin.email}'))
        
        # Crear usuarios de prueba
        test_users = [
            {
                'email': 'test@passd.com',
                'username': 'testuser',
                'password': 'test123',
                'salt': 'test_salt_456',
            },
            {
                'email': 'demo@passd.com',
                'username': 'demouser',
                'password': 'demo123',
                'salt': 'demo_salt_789',
            }
        ]
        
        users_created = []
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'salt': user_data['salt'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                users_created.append(user)
                self.stdout.write(self.style.SUCCESS(f'✅ Usuario creado: {user.email}'))
                self.stdout.write(self.style.SUCCESS(f'   Username: {user.username}'))
                self.stdout.write(self.style.SUCCESS(f'   Password: {user_data["password"]}'))
                self.stdout.write(self.style.SUCCESS(f'   Salt: {user_data["salt"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Usuario ya existe: {user.email}'))
        
        # Crear carpetas de prueba para el usuario test
        test_user = User.objects.get(email='test@passd.com')
        
        self.stdout.write('\n📁 Creando carpetas...')
        folders_data = [
            {'name': 'Redes Sociales', 'user': test_user},
            {'name': 'Trabajo', 'user': test_user},
            {'name': 'Bancos', 'user': test_user},
            {'name': 'Personal', 'user': test_user},
        ]
        
        folders = []
        for folder_data in folders_data:
            folder, created = Folder.objects.get_or_create(**folder_data)
            folders.append(folder)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Carpeta creada: {folder.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Carpeta ya existe: {folder.name}'))
        
        # Crear items de prueba
        self.stdout.write('\n🔐 Creando items de prueba...')
        
        items_data = [
            {
                'url': 'https://twitter.com',
                'username': 'test_user',
                'encrypted_pass': 'encrypted_twitter_pass_123',
                'note': 'Mi cuenta personal de Twitter',
                'tags': 'social,twitter,personal',
                'folder': folders[0],  # Redes Sociales
                'user': test_user,
            },
            {
                'url': 'https://facebook.com',
                'username': 'test@passd.com',
                'encrypted_pass': 'encrypted_facebook_pass_456',
                'note': 'Cuenta de Facebook',
                'tags': 'social,facebook',
                'folder': folders[0],  # Redes Sociales
                'user': test_user,
            },
            {
                'url': 'https://github.com',
                'username': 'test_developer',
                'encrypted_pass': 'encrypted_github_pass_789',
                'note': 'Cuenta de desarrollo',
                'tags': 'desarrollo,github,trabajo',
                'folder': folders[1],  # Trabajo
                'user': test_user,
            },
            {
                'url': 'https://gmail.com',
                'username': 'test@gmail.com',
                'encrypted_pass': 'encrypted_gmail_pass_abc',
                'note': 'Email personal principal',
                'tags': 'email,google,importante',
                'folder': folders[3],  # Personal
                'user': test_user,
            },
            {
                'url': 'https://bankofamerica.com',
                'username': 'test_user_boa',
                'encrypted_pass': 'encrypted_bank_pass_def',
                'note': 'Cuenta bancaria principal',
                'tags': 'banco,finanzas,importante',
                'folder': folders[2],  # Bancos
                'user': test_user,
            },
            {
                'url': 'https://linkedin.com',
                'username': 'test-professional',
                'encrypted_pass': 'encrypted_linkedin_pass_ghi',
                'note': 'Perfil profesional',
                'tags': 'profesional,linkedin,networking',
                'folder': folders[1],  # Trabajo
                'user': test_user,
            },
            # Items sin carpeta (sin clasificar)
            {
                'url': 'https://netflix.com',
                'username': 'test@passd.com',
                'encrypted_pass': 'encrypted_netflix_pass_jkl',
                'note': 'Cuenta de streaming',
                'tags': 'entretenimiento,streaming,netflix',
                'folder': None,  # Sin carpeta
                'user': test_user,
            },
            {
                'url': 'https://spotify.com',
                'username': 'test_music',
                'encrypted_pass': 'encrypted_spotify_pass_mno',
                'note': 'Música y podcasts',
                'tags': 'musica,spotify,premium',
                'folder': None,  # Sin carpeta
                'user': test_user,
            },
        ]
        
        items_created = 0
        for item_data in items_data:
            item, created = KeyItem.objects.get_or_create(
                url=item_data['url'],
                user=item_data['user'],
                defaults=item_data
            )
            if created:
                items_created += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Item creado: {item.url} ({item.username})'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Item ya existe: {item.url}'))
        
        # Resumen final
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 DATOS DE PRUEBA CREADOS EXITOSAMENTE'))
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS(f'\n📊 Resumen:'))
        self.stdout.write(self.style.SUCCESS(f'   👥 Usuarios: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   📁 Carpetas: {Folder.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   🔐 Items: {KeyItem.objects.count()}'))
        
        self.stdout.write(self.style.SUCCESS('\n🔑 Credenciales de acceso:'))
        self.stdout.write(self.style.SUCCESS('   Superusuario:'))
        self.stdout.write(self.style.SUCCESS('     Username: admin'))
        self.stdout.write(self.style.SUCCESS('     Email: admin@passd.local'))
        self.stdout.write(self.style.SUCCESS('     Password: admin123'))
        self.stdout.write(self.style.SUCCESS('     Salt: admin_salt_123'))
        
        self.stdout.write(self.style.SUCCESS('\n   Usuario de prueba:'))
        self.stdout.write(self.style.SUCCESS('     Username: testuser'))
        self.stdout.write(self.style.SUCCESS('     Email: test@passd.com'))
        self.stdout.write(self.style.SUCCESS('     Password: test123'))
        self.stdout.write(self.style.SUCCESS('     Salt: test_salt_456'))
        
        self.stdout.write(self.style.SUCCESS('\n   Usuario demo:'))
        self.stdout.write(self.style.SUCCESS('     Username: demouser'))
        self.stdout.write(self.style.SUCCESS('     Email: demo@passd.com'))
        self.stdout.write(self.style.SUCCESS('     Password: demo123'))
        self.stdout.write(self.style.SUCCESS('     Salt: demo_salt_789'))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ ¡Todo listo para probar la API!'))
        self.stdout.write('=' * 60 + '\n')
