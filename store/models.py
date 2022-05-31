from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirm_password = models.CharField(null=False, max_length=50, default='')
    age = models.IntegerField(default=1, verbose_name="年龄")
    address = models.CharField(null=False, default='', max_length=200)
    region = models.CharField(null=False, default='', max_length=200)
    city = models.CharField(null=False, default='', max_length=50)
    province = models.CharField(null=False, default='', max_length=50)
    zipcode = models.CharField(null=False, default='', max_length=5)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "用户表"


class Product(models.Model):
    p_name = models.CharField(max_length=256, verbose_name='商品名称')
    p_department = models.CharField(max_length=256, verbose_name='商品种类')
    p_aisle = models.CharField(max_length=256, verbose_name='商品子类')
    p_price = models.IntegerField(default=10, verbose_name='商品价格')
    p_url = models.CharField(max_length=512, verbose_name='商品图片', blank=True, null=True)
    p_total_views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    def __str__(self):
        return self.p_name

    class Meta:
        verbose_name_plural = "商品表"


class Order(models.Model):
    order_Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_Product = models.ManyToManyField(Product, through="OrderProducts")
    order_Date = models.DateField(default=date.today)
    order_Total = models.FloatField(default=0)


class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    cart_Customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    cart_Products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.id.__str__()
