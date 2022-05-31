import re

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from time import sleep
from django.urls import reverse

from store.models import Product, Cart


class ProductPostViewTests(TestCase):
    def setUp(self) -> None:
        self.username = 'test'
        self.password = 'test'
        self.customer = User(username=self.username, password=self.password)
        self.customer.save()
        # self.client.login(username=self.username, password=self.password)

    def test_increase_views(self):
        # 请求详情视图时，浏览量+1
        product = Product(p_name='test1', p_department='test', p_aisle='test', p_total_views=0)
        product.save()
        self.assertIs(product.p_total_views, 0)  # 浏览量
        self.assertIs(self.check_product_img(product), 0)  # 商品图片

        url = reverse('store:product', args=(product.id,))
        response = self.client.get(url)

        viewed_product = Product.objects.get(id=product.id)
        self.assertIs(viewed_product.p_total_views, 1)
        self.assertIs(self.check_product_img(viewed_product), 1)

    def check_product_img(self, product):
        re_s = 'http'
        if re.match(re_s, str(product.p_url)) is None:
            return 0
        else:
            return 1

    def test_add_to_cart(self):
        # 测试 添加购物车
        # print(self.customer.id)
        cart = Cart.objects.filter(cart_Customer_id=self.customer.id)
        if len(cart) == 0:
            cart = None
        self.assertIs(cart, None)

        url = reverse('store:login')
        response = self.client.post(url, {'username': self.username, 'password': self.password})

        cart = Cart.objects.filter(cart_Customer_id=self.customer.id)
        print(cart)
        if len(cart) != 0:
            cart = 1
        self.assertIs(cart, 1)

class SendViewsTestCase(TestCase):
    # 测试注册页面
    def test_user_register(self):
        url = reverse('store:register')
        rep = self.client.get(url)
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'content')