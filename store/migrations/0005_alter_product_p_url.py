# Generated by Django 3.2.5 on 2022-05-19 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_p_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_url',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='产品图片'),
        ),
    ]