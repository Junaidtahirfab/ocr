# Generated by Django 4.2.14 on 2024-12-05 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_gender_user_address_1_user_address_2_user_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Gender',
            new_name='gender',
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.company'),
        ),
    ]
