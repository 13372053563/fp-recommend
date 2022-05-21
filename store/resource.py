#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: resource.py
@time: 2022/5/7 18:48
'''
from import_export import resources
from store.models import Product

class ProductResource(resources.ModelResource):

    class Meta:
        model = Product