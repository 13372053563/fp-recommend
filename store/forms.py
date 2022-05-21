#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: forms.py
@time: 2022/5/5 11:56
'''
from django import forms
from django.contrib.auth import authenticate

from store.models import Customer
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="密码")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        labels = {
            "username": "用户名",
            "email": "邮箱",
            "first_name": "名字",
            "last_name": "姓氏",
            "password": "密码"
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('confirm_password', 'age')
        labels = {
            "confirm_password": "确认密码",
            "age": "年龄"
        }
        widgets = {
            'confirm_password': forms.PasswordInput()
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入用户名",
            }
        ),
        label="用户名")

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码",
            }
        ),
        label="密码")

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("账号或密码错误")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data