# Generated migration to populate username field

from django.db import migrations


def populate_usernames(apps, schema_editor):
    """
    Llena el campo username con el email para usuarios existentes que tengan username null
    """
    User = apps.get_model('users', 'User')
    users_without_username = User.objects.filter(username__isnull=True)
    
    for user in users_without_username:
        # Usar el email como username para usuarios existentes
        user.username = user.email.split('@')[0]
        user.save()


def reverse_populate_usernames(apps, schema_editor):
    """
    Operación reversa: establecer username a null
    """
    User = apps.get_model('users', 'User')
    User.objects.all().update(username=None)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_username'),
    ]

    operations = [
        migrations.RunPython(populate_usernames, reverse_populate_usernames),
    ]
