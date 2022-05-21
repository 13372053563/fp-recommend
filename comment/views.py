from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse

from store.models import Product
from .forms import CommentForm
from .models import Comment


@login_required(login_url='/store/login/')
def post_comment(request, product_id, parent_comment_id=None):
    product = get_object_or_404(Product, id=product_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                # get_root() 将其父级重置为树形结构最底部的一级评论
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')
            new_comment.save()
            return redirect(reverse('store:product', kwargs={'product_id': product_id}))
        else:
            print(comment_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理GET请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'product_id': product_id,
            'parent_comment_id': parent_comment_id,
        }
        return render(request, 'comment/reply.html', context)
    # 处理其它请求
    else:
        return HttpResponse("仅接受GET/POST请求。")