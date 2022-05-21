"""
WSGI config for django_fptree_recommend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_fptree_recommend.settings')

application = get_wsgi_application()

from store.models import Product
from get_img_url import get_product_url
products = Product.objects.filter(p_url=' ')
if products:
    print("存在商品没有图片，开始爬虫")
else:
    print("所有商品都有图片")
products_no_image = []
for product in products:
    products_no_image.append(product.p_name)
get_product_url(len(products_no_image), products_no_image)
