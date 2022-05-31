#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: urls.py
@time: 2022/5/5 11:53
'''
from django.urls import path
from store import views

urlpatterns = [
    path('index/', views.index, name='index'),  # 主页
    path('categories/', views.categoryList, name='categories'),  # 大类列表
    path('subcategoryList/<str:cat_name>', views.subcategoryList, name='subcategoryList'),  # 子类列表
    path('product_list/<str:subcat_name>', views.product_list, name='product_list'),  # 商品列表
    path('product/<int:product_id>', views.product, name='product'),  # 商品详情
    path('product/<int:product_id>/<str:username>', views.addToCart, name='addToCart'),  # 添加购物车
    path('remove/<int:product_id>/<str:username>', views.deleteFromCart, name='delete'),  # 删除购物车商品
    path('cart/<str:username>', views.shoppingcart, name='shoppingcart'),  # 购物车页面
    path('orders/<str:username>', views.orders, name='orders'),  # 订单页面
    path('remove_order/<int:order_id>/<str:username>', views.remove_order, name='remove_order'),  # 删除订单
    path('delinfo/<int:cart_id>', views.deliveryInfo, name='checkout'),  # 支付
    path('confirm/<int:cart_id>/<str:username>', views.confirmOrder, name='confirm'),  # 填写订单信息
    path('login/', views.user_login, name='login'),  # 登录
    path('logout/', views.user_logout, name='logout'),  # 登出
    path('register/', views.register, name='register'),  # 注册
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
]
