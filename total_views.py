#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: total_views.py
@time: 2022/5/14 16:19
'''

import os

from tqdm import tqdm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'django_fptree_recommend.settings')  # mysite用的是自己的project
import django
django.setup()
from store.models import Product

import pandas as pd
data = pd.read_csv("dataset/transaction_data.csv")
total_views = {}
for i in tqdm(data["product_id"].to_list(), desc="统计各元素出现次数", ncols=120):
    if i not in total_views:
        total_views[i] = 1
    else:
        total_views[i] += 1

for product_id, p_total_views in tqdm(total_views.items(), desc="写入数据库", ncols=120):
    product = Product.objects.get(id=product_id)
    product.p_total_views = p_total_views
    product.save(update_fields=['p_total_views'])