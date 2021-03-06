# Generated by Django 3.2.5 on 2022-05-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20220519_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_aisle',
            field=models.CharField(max_length=256, verbose_name='商品子类'),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_department',
            field=models.CharField(max_length=256, verbose_name='商品种类'),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_name',
            field=models.CharField(max_length=256, verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_price',
            field=models.IntegerField(default=10, verbose_name='商品价格'),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_url',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='商品图片'),
        ),
    ]
