# Generated by Django 4.2.14 on 2024-12-05 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_role_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verfied',
            field=models.BooleanField(default=False),
        ),
    ]
