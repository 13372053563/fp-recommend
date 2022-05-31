#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: resource.py
@time: 2022/5/7 18:48
'''

from import_export import resources
from import_export.fields import Field

from store.models import Product


class ProductResource(resources.ModelResource):
    id = Field(attribute='id')
    p_name = Field(attribute='p_name', column_name='商品名称')
    p_department = Field(attribute='p_department', column_name='商品种类')
    p_aisle = Field(attribute='p_aisle', column_name='商品子类')
    p_price = Field(attribute='p_price', column_name='商品价格')
    p_url = Field(attribute='p_url', column_name='商品图片')
    p_total_views = Field(attribute='p_total_views', column_name='浏览量')

    class Meta:
        model = Product
        fields = ('id', 'p_name', 'p_department', 'p_aisle')
        export_order = ('id', 'p_name', 'p_department', 'p_aisle', 'p_price', 'p_url', 'p_total_views')
