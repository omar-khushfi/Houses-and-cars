# Generated by Django 5.1.2 on 2024-12-19 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_seller_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='code',
            old_name='user',
            new_name='seller',
        ),
    ]
