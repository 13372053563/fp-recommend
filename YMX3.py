#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: zhangshihao
@file: YMX3.py
@time: 2022/5/8 21:53
'''
import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'django_fptree_recommend.settings')  # mysite用的是自己的project
import django

django.setup()
from store.models import Product

def create_chrome():
    # 声明一个谷歌驱动器，并设置不加载图片，间接加快访问速度
    with open('static/stealth.min.js') as f:
        js = f.read()
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("headless")  # 不显示浏览器
    browser = webdriver.Chrome(options=chrome_options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    return browser


def get_product_url(product_url_dict):
    number = 0
    browser = create_chrome()
    for product_name in tqdm(list(product_url_dict.keys()), desc="get_product_url", ncols=80):
        product_url = product_url_dict[product_name]
        img_list = []
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
        number += 1
        update_product(img_list[0], product_name)
        if number % 100 == 0:
            print(datetime.datetime.now())
            print("等待10分钟！")
            sleep(600)
            if number == 500:
                print(datetime.datetime.now())
                print("多休息一会儿！")
                sleep(600)
            if number == number_end:
                print("爬虫结束！！！")
                browser.close()
                return None
        if number == number_end:
            sleep(300)
            print("爬虫结束！！！")
            browser.close()


def get_search_url(number_start, number):
    products = Product.objects.all()
    results = []
    for product in products:
        results.append(product.p_name)
    results = results[number_start:number_start + number]
    amazon_search = "https://www.amazon.cn/s?k="
    product_url_dict = {}
    for i in tqdm(results, desc="获取搜索页面", ncols=100):
        product_name = i
        product_url = amazon_search + product_name
        product_url_dict[product_name] = product_url
    return product_url_dict  # 产品名称：对应的亚马逊连接


def update_product(p_url, p_name):  # 数据写入mysql
    products = Product.objects.filter(p_name=p_name)
    for i in products:
        i.p_url = p_url
        i.save(update_fields=['p_url'])


if __name__ == "__main__":
    number_start = 49500
    number_end = 189
    product_url_dict = get_search_url(number_start, number_end)
    get_product_url(product_url_dict)
