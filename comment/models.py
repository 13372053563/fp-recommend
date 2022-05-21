from ckeditor.fields import RichTextField
from django.db import models
from store.models import Product, Customer
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Comment(MPTTModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # content = models.TextField()
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.content[:20]