from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from get_img_url import get_product_url
from comment.forms import CommentForm
from comment.models import Comment
from predict import predict
from store.forms import UserForm, CustomerForm, LoginForm
from store.models import *


def index(request):
    # 本质上返回HttpResponse  它帮我们把模板和context数据渲染成字符串
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        customer_form = CustomerForm(data=request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            if user_form.cleaned_data['password'] == customer_form.cleaned_data['confirm_password'] and \
                    customer_form.cleaned_data['age'] > 0:
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                customer = customer_form.save(commit=False)
                customer.confirm_password = customer_form.cleaned_data['confirm_password']
                customer.user = user
                customer.save()

                cart = Cart()
                cart.cart_Customer_id = customer.id
                cart.save()

                login(request, user)
                return redirect(reverse('store:index'))
            if user_form.cleaned_data['password'] != customer_form.cleaned_data['confirm_password'] and \
                    customer_form.cleaned_data['age'] > 0:
                customer_form.add_error("confirm_password", "两次输入的密码不相等")
            else:
                customer_form.add_error("age", "年龄不能为0")
    # GET 请求
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    context = {
        'user_form': user_form,
        'customer_form': customer_form,
    }
    return render(request, 'signup.html', context=context)


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(reverse('index'))
    # GET请求
    else:
        login_form = LoginForm()
    context = {
        "login_form": login_form,
    }
    return render(request, "login.html", context=context)


def categoryList(request):
    product_list = Product.objects.all().order_by('p_department')
    cat = []
    for product in product_list:
        if product.p_department == 'other':
            continue
        else:
            cat.append(product.p_department)
    cat = set(cat)
    cat_list = list(cat)
    cat_list.append('other')  # other放在最后显示
    context = {
        'cat_list': cat_list,
    }
    return render(request, 'categorylist.html', context=context)


def subcategoryList(request, cat_name):
    product = Product.objects.all().filter(p_department=cat_name).values()
    subcat = []
    for i in product:
        subcat.append(i.get("p_aisle"))
    subcat_set = list(set(subcat))
    # 每页显示 10 个
    paginator = Paginator(subcat_set, 10)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 subcat_sets
    subcat_sets = paginator.get_page(page)
    context = {
        "subcat_sets": subcat_sets,
        "cat_name": cat_name,
    }
    return render(request, 'subcategorylist.html', context=context)


def product_list(request, subcat_name):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'p_total_views':
        product_list = Product.objects.all().filter(p_aisle=subcat_name).order_by('-p_total_views')
        order = 'p_total_views'
    else:
        product_list = Product.objects.all().filter(p_aisle=subcat_name).order_by('-id')
        order = 'normal'
    # product_list = Product.objects.all().filter(p_aisle=subcat_name).order_by('p_total_views')
    # 每页显示 20 个商品
    paginator = Paginator(product_list, 20)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 products
    products = paginator.get_page(page)
    context = {
        "products": products,
        "order": order,  # 顺序
        "subcat_name": subcat_name,
    }
    return render(request, 'productlist.html', context=context)


def product(request, product_id):
    # 展示商品的详细信息
    # pro = Product.objects.all().filter(id=product_id).values()
    # print(pro)
    # <QuerySet [{'id': 219, 'p_name': 'Totz Toothbrush Extra Soft 18+ Months', 'p_department': 'babies', 'p_aisle': 'baby accessories', 'p_price': 10}]>

    pro = Product.objects.get(id=product_id)
    # 商品图片
    if pro.p_url.startswith('http'):
        url = pro.p_url
        pass
    else:
        name_list = []
        name_list.append(pro.p_name)
        url = get_product_url(1, name_list)
        # print(url)
    # 推荐
    max_len = 8
    result = predict(str(product_id), max_len)
    recItems = []
    for res in result:
        p = Product.objects.all().get(id=int(res))
        recItems.append(p)
    comments = Comment.objects.filter(product=product_id)
    # 浏览量 +1
    pro.p_total_views += 1
    pro.save(update_fields=['p_total_views'])
    # update_fields=[]指定了数据库只更新total_views字段，优化执行效率
    # 评论富文本
    comment_form = CommentForm()
    context = {
        "pro": pro,
        "comments": comments,
        "recItems": recItems,
        'comment_form': comment_form,
        'url': url,
    }
    return render(request, 'product.html', context=context)


def addToCart(request, product_id, username):
    product = Product.objects.get(id=product_id)  # 获取待添加的商品
    cart = Cart.objects.get(cart_Customer__user__username=username)  # 获取当前用户的购物车
    cart.cart_Products.add(product)  # 将商品添加到当前用户的购物车
    return HttpResponse(status=204)


def deleteFromCart(request, product_id, username):
    product = Product.objects.get(id=product_id)  # 获取待添加的商品
    cart = Cart.objects.get(cart_Customer__user__username=username)  # 获取当前用户的购物车
    cart.cart_Products.remove(product)  # 将商品从当前用户的购物车删除
    return HttpResponseRedirect(reverse('store:shoppingcart', kwargs={'username': username}))


def shoppingcart(request, username):
    cart = Cart.objects.all().get(cart_Customer__user__username=username)
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context=context)


def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    return render(request, 'contactus.html')


def deliveryInfo(request, cart_id):
    # 发起订单
    # 获取购物车中的所有商品
    cart = Cart.objects.all().get(id=cart_id)
    c = cart.cart_Products.all()
    data = request.POST
    convertedData = dict(data)
    # {'quantity': ['1', '0'], 'AddToCart': [''], 'csrfmiddlewaretoken': ['QiTFETOervm3VEhzIr22sbwGjvopgcGlxjGhU8jXBMJeTXS9IUVPrybLOWEKbmNw']}
    # 获取购物车中每个商品的购买数量
    quantity = convertedData['quantity']
    # print(quantity)

    toKeep = []
    finalCart = []
    ids = []
    total = 0

    for i in range(0, len(quantity)):
        if int(quantity[i]) != 0:  # 将购买数量不为0的商品加入finalcart
            # 获取每个商品的数量
            toKeep.append(quantity[i])
            # 获取支付的商品的名称
            finalCart.append(c[i])
            # 获取支付的商品的id
            ids.append(c[i].id)
            # 获取购物车中商品的总价格
            total += (c[i].p_price * int(quantity[i]))

    if len(finalCart):  # 如果有商品
        # session中的aaa值为对应的商品id
        request.session['aaa'] = ids
        global PRDS  # 声明全局变量PRDS, products
        PRDS = finalCart

    else:
        return HttpResponse(status=204)
    toKeep.reverse()  # 倒序
    context = {
        "products": finalCart,  # 购买的商品
        "total": total,  # 总价格
        "cartId": cart_id,  # 购物车id
        "quantity": toKeep,  # 已购买的商品的数量
    }
    return render(request, 'checkout.html', context=context)


def confirmOrder(request, cart_id, username):
    # 填写订单信息
    # 获取deliveryInfo中设置的session值，为购买的商品的id
    ids = request.session.get('aaa')
    cart = Cart.objects.all().get(id=cart_id)
    order = Order()
    order.order_Customer = cart.cart_Customer

    # 从前端的POST请求中，获取对应的地址信息
    data = request.POST
    # 信息转为字典
    convertedData = dict(data)
    print(convertedData)
    # {'quantity': ['01'], 'products': ['[<Product: Penne Rigate With Spinach>]'], 'total': ['10'], 'address1': ['caoji'], 'address2': ['16hao'], 'city': ['suqian'], 'state': ['Perak'], 'zipcode': ['12345']}

    total = request.POST.get('total')
    address1 = request.POST.get('address1')
    address2 = request.POST.get('address2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zipcode = request.POST.get('zipcode')

    global PRDS
    products = PRDS
    # 删除购物车中已经购买的商品
    for product in products:
        cart.cart_Products.remove(product.id)

    # 订单的总价钱
    order.order_Total = total
    order.save()

    # 购买商品的数量，列表
    tempQuantity = convertedData['quantity']
    # print(tempQuantity)  # ['01']

    # 将地址信息保存到用户的信息表
    cart.cart_Customer.address = address1
    cart.cart_Customer.address2 = address2
    cart.cart_Customer.city = city
    cart.cart_Customer.state = state
    cart.cart_Customer.zipcode = zipcode
    cart.cart_Customer.save()


    p = Product.objects.all()
    products = []
    for z in range(0, ids.__len__()):
        products.append(p.filter(id=ids[z]))

    for j in range(0, products.__len__()):
        orderproducts = OrderProducts()
        orderproducts.product = products[j][0]
        orderproducts.quantity = tempQuantity[0][j]
        orderproducts.order = order
        orderproducts.save()
    PRDS = []

    # 支付完成后跳转到订单页面
    return redirect(reverse("store:orders", kwargs={'username': username}))



def orders(request, username):
    products = []
    orders = list(Order.objects.filter(order_Customer__user__username=username))
    o = OrderProducts.objects.filter(order__order_Customer__user__username=username)
    for order in orders:
        products.append(list(o.filter(order_id=order.id)))
    context = {
        "products": products,
    }
    # print(products)
    return render(request, 'order.html', context=context)


def remove_order(request, order_id, username):
    orders = list(Order.objects.filter(order_Customer__user__username=username))
    order_obj = orders[order_id]  # 获取待删除订单的对象
    order_obj.delete()
    return redirect(reverse("store:orders", kwargs={'username': username}))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:index'))


