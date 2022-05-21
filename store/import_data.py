#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: import_data.py
@time: 2022/4/23 7:43
'''
import os
import django
import csv
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTING_MODULE', 'django_fptree_recommend.settings')
django.setup()

from store.models import Product

with open("E:/Desktop/bishe/data/products_departments.csv") as csvfile:
    product_data = csv.reader(csvfile)
    next(product_data)
    for row in tqdm(product_data, desc='data_to_sql', ncols=80):
        product = Product(p_name=row[1], p_department=row[2], p_aisle=row[3])
        product.save()
