# Generated migration to make username required

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_populate_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
