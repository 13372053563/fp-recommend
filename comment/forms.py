#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: forms.py
@time: 2022/5/8 13:36
'''
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
