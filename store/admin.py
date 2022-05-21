from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

from .resource import ProductResource


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'age', 'email', 'is_active', 'is_superuser', 'last_login')
    ordering = ('id',)

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

    def last_login(self, obj):
        return obj.user.last_login

    def is_superuser(self, obj):
        return obj.user.is_superuser

    last_login.short_description = '上次登录时间'
    is_active.short_description = '激活状态'
    is_superuser.short_description = '管理员'
    username.short_description = '用户名'
    email.short_description = '邮箱'


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'p_name', 'p_department', 'p_aisle', 'p_price', 'p_url', 'p_total_views')
    resource_class = ProductResource
    search_fields = ('p_name', 'p_department', 'p_aisle')
    list_filter = ("p_department", )
    list_per_page = 20


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)

