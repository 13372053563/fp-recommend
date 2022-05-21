from django.contrib import admin
from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'product', 'user', 'created')
    ordering = ('id',)

    def user(self, obj):
        return obj.user.username

    def product(self, obj):
        return obj.product.p_name


admin.site.register(Comment, CommentAdmin)
