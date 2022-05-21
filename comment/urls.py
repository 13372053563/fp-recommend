#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: urls.py
@time: 2022/5/8 15:10
'''
from django.urls import path
from . import views

urlpatterns = [
    # 发表评论
    path('post-comment/<int:product_id>/', views.post_comment, name='post_comment'),
    # 处理二级回复
    path('post-comment/<int:product_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]