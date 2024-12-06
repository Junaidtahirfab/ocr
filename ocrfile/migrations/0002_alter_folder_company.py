# Generated by Django 4.2.14 on 2024-12-06 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_rename_gender_user_gender_alter_user_company'),
        ('ocrfile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='account.company'),
        ),
    ]
