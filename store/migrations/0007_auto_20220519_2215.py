# Generated by Django 3.2.5 on 2022-05-19 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_customer_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='state',
            new_name='province',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='address2',
            new_name='region',
        ),
    ]
