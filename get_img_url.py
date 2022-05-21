#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: get_img_url.py
@time: 2022/5/10 21:10
'''
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'django_fptree_recommend.settings')  # mysite用的是自己的project
import django

django.setup()
from store.models import Product


def get_product_url(number, key_words):
    # 声明一个谷歌驱动器，并设置不加载图片，间接加快访问速度
    count = 0
    with open('static/stealth.min.js') as f:
        js = f.read()
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("headless")  # 不显示浏览器
    browser = webdriver.Chrome(options=chrome_options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    for key in key_words:
        img_list = []
        amazon_search = "https://www.amazon.cn/s?k="
        product_url = amazon_search + str(key)
        browser.get(product_url)
        try:
            lis = browser.find_elements(By.XPATH, '//a[@class="a-link-normal s-no-outline"]//img')
            for li in lis:
                img_list.append(li.get_attribute('src'))
            browser.find_element(By.ID, 'twotabsearchtextbox').clear()
            if len(img_list) == 0:
                img_list.append("http://via.placeholder.com/200x250/FAEBD7")
        except Exception as e:
            img_list.append("http://via.placeholder.com/200x250/FAEBD7")
        save_to_model(key, img_list[0])  # 保存到数据库
        print(count, key, img_list[0])
        count += 1
        if count % 100 == 0:
            if count == number:
                print("结束!")
                browser.close()
                break
            else:
                sleep(300)
        if count == number:
            print("结束!")
            browser.close()
            return img_list[0]



def save_to_model(p_name, url):
    products = Product.objects.filter(p_name=p_name)
    for product in products:
        product.p_url = url
        product.save()
