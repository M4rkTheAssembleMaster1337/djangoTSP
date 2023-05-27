from django.db import transaction
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.http import HttpResponse
from products.models import *
from orders.models import *
from .forms import CreateUserForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from accounts.queries import DbConnectivity

activate('rus')
from django.contrib.auth.forms import UserCreationForm

from .decorators import unauthenticated_user, allowed_users, admin_only
from django.http import JsonResponse

import json

import datetime



@login_required(login_url='login')
@admin_only
def home(request):
    all_completed = Order.objects.filter(status_id=3, complete=True).count()
    all_cancelled = Order.objects.filter(status_id=2,complete=True).count()
    all_new = Order.objects.filter(status_id=1,complete=True).count()
    all_orders = Order.objects.filter(complete=True).count()
    new_orders = Order.objects.filter(status_id=1, complete=True)
    context = {'completed': all_completed, 'cancelled':all_cancelled, 'new':all_new, 'all':all_orders, 'orders': new_orders}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    all_products = ProductImage.objects.select_related('product')
    context = {'products': all_products, 'nmb_items': 0}
    check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    if not request.user.is_staff and len(check):
        ord_id = \
        list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
        items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
        print('items: ', items)
        print('nm_in_cart: ', ord_id)
        context = {'products': all_products, 'nmb_items': items}
    return render(request, 'accounts/products_.html', context)


def customer(request):
    return render(request, 'accounts/customer_.html')


@unauthenticated_user
def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Успешно был создан аккаунт с именем ' + user)
            return redirect('login')
        else:
            messages.error(request, 'Нельзя зарегистрировать')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)


def order_history_page(request):
    # context = {'products': all_products, 'nmb_items': 0}
    check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    nmb_items = 0
    if len(check):
        ord_id = list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
        nmb_items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
    pending_order = Order.objects.filter(user=request.user, complete=True, status_id=3)
    cancelled_order = Order.objects.filter(user=request.user, complete=True, status_id=2)
    done_order = Order.objects.filter(user=request.user, complete=True, status_id=1)
    all_orders = Order.objects.filter(user=request.user, complete=True)
    all_orders_ids = list(all_orders.values_list('id', flat=True))
    print('all ids: ', all_orders_ids)
    all_items_in_order = ProductInOrder.objects.filter(order_id__in=all_orders_ids).order_by('product_id')
    all_product_ids = list(all_items_in_order.values_list('product_id', flat=True))
    all_images_in_order = ProductImage.objects.filter(product_id__in=all_product_ids).order_by('product_id')
    # test = ProductInOrder.objects.filter(order_id__in=all_orders_ids).prefetch_related('productimage_set')
    # print('test', test)
    print('len1: ', len(all_items_in_order))
    print('len2: ', len(all_images_in_order))
    # items = list(zip(all_items_in_order, all_images_in_order))
    context = {'orders': all_orders, 'items': all_items_in_order, 'images': all_images_in_order, 'nmb_items': nmb_items}
    print('all orders: ', all_orders)
    # print('items: ', items)
    # print('items[0]: ', items[0])
    # print('items[1]: ', items[1])

    return render(request, 'accounts/order_history.html', context)


def cart_page(request):

    customer_ = request.user
    order, created = Order.objects.get_or_create(user=customer_, complete=False, status_id=1)
    # check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    ord_id = list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
    nmb_items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
    print('items: ', nmb_items)
    print('nm_in_cart: ', ord_id)
    order_id = order.id
    print('order id: ', order_id)
    items = ProductInOrder.objects.filter(order=order_id).order_by('product_id')
    all_ids_items = items.values_list('product_id', flat=True)
    all_ids_items = list(all_ids_items)
    print(all_ids_items)
    items2 = ProductImage.objects.filter(product_id__in=all_ids_items).order_by('product_id')
    print('items: ', items)
    res = list(zip(items, items2))
    print(res)
    prices = items.values_list('total_price', flat=True)
    prices = list(prices)
    print(prices)
    prices = [float(i) for i in prices]
    print(prices)
    total_sum = 0
    for i in prices:
        total_sum += i
    quantity = len(prices)
    context = {'items': res, 'total': total_sum, 'nmb': quantity, 'nmb_items': nmb_items}
    return render(request, 'accounts/cart.html', context)

def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action: ', action)
    print('prId: ', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=customer, complete=False, status_id=1)
    print('our order: ', order)
    # temp = Order.objects.filter(complete=False, user=customer, total_pric)
    print('temp: ', order)
    # print('len temp: ', len(order))
    if action == 'add':
        curItems = ProductInOrder.objects.filter(order_id=order.id, product_id=productId)
        if not len(curItems):

            orderItem = ProductInOrder.objects.create(
                product_id=product.id,
                nmb=1,
                order_id=order.id
            )
            print('Order item now: ', orderItem)
            order.total_price += orderItem.price_per_item
        else:

            temp_nmb = list(curItems.values_list('nmb', flat=True))[0]
            print(temp_nmb)
            curItems.delete()
            orderItem = ProductInOrder.objects.create(
                product_id=product.id,
                nmb=temp_nmb + 1,
                order_id=order.id
            )
            print('Order item now: ', orderItem)
            order.total_price += orderItem.price_per_item


    elif action == 'remove':
        curItems = ProductInOrder.objects.filter(order_id=order.id, product_id=productId)
        quant = list(curItems.values_list('nmb', flat=True))[0]
        if len(curItems) and quant > 1:
            temp_nmb = list(curItems.values_list('nmb', flat=True))[0]
            temp_total_price = list(curItems.values_list('total_price', flat=True))[0]
            temp_price_per_item = list(curItems.values_list('price_per_item', flat=True))[0]
            curItems.delete()
            order.total_price -= temp_price_per_item
            orderItem = ProductInOrder.objects.create(
                product_id=product.id,
                nmb=temp_nmb - 1,
                order_id=order.id
            )
        if len(curItems) and quant == 1:
            temp_price_per_item = list(curItems.values_list('price_per_item', flat=True))[0]
            curItems.delete()
            order.total_price -= temp_price_per_item

    order.save()
    print('total price now: ', order.total_price)

    # if len(temp) != 0:
    #    temp.delete()
    #    print('temp: ', temp)
    #    print('len temp: ', len(temp))
    #    temp = Order.

    return JsonResponse('Item was added', safe=False)


def kapas(request):
    all_products = list(Product.objects.filter(category=1).values_list('id', flat=True))
    all_products = ProductImage.objects.filter(product_id__in=all_products)
    context = {'products': all_products, 'nmb_items': 0}
    check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    if not request.user.is_staff and len(check):
        ord_id = \
        list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
        items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
        print('items: ', items)
        print('nm_in_cart: ', ord_id)
        context = {'products': all_products, 'nmb_items': items}
    return render(request, 'accounts/products_.html', context)


def gloves(request):
    all_products = list(Product.objects.filter(category=3).values_list('id', flat=True))
    all_products = ProductImage.objects.filter(product_id__in=all_products)
    context = {'products': all_products, 'nmb_items': 0}
    check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    if not request.user.is_staff and len(check):
        ord_id = \
        list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
        items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
        print('items: ', items)
        print('nm_in_cart: ', ord_id)
        context = {'products': all_products, 'nmb_items': items}
    return render(request, 'accounts/products_.html', context)


def helmets(request):
    all_products = list(Product.objects.filter(category=2).values_list('id', flat=True))
    all_products = ProductImage.objects.filter(product_id__in=all_products)
    context = {'products': all_products, 'nmb_items': 0}
    check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    if not request.user.is_staff and len(check):
        ord_id = \
        list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
        items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
        print('items: ', items)
        print('nm_in_cart: ', ord_id)
        context = {'products': all_products, 'nmb_items': items}
    return render(request, 'accounts/products_.html', context)


def bandage(request):
    all_products = list(Product.objects.filter(category=4).values_list('id', flat=True))
    all_products = ProductImage.objects.filter(product_id__in=all_products)
    context = {'products': all_products, 'nmb_items': 0}
    check = Order.objects.filter(user=request.user, complete=False, status_id=1)
    if not request.user.is_staff and len(check):
        ord_id = \
        list(Order.objects.filter(user=request.user, complete=False, status_id=1).values_list('id', flat=True))[0]
        items = sum(list(ProductInOrder.objects.filter(order_id=ord_id).values_list('nmb', flat=True)))
        print('items: ', items)
        print('nm_in_cart: ', ord_id)
        context = {'products': all_products, 'nmb_items': items}
    return render(request, 'accounts/products_.html', context)


def profit_page(request):
    res = DbConnectivity.get_total_price_all()
    all_products_ids = list(res.values_list('product', flat=True))
    print(all_products_ids)
    all_images = ProductImage.objects.filter(product_id__in=all_products_ids)
    print('all_images: ', all_images)
    places = []
    for i in range(1,len(all_images)+1):
        places.append(i)
    res = list(zip(places, res))
    context = {'total': res, 'images': all_images, 'places': places}
    return render(request, 'accounts/profit.html', context)

def popularity_page(request):
    res = DbConnectivity.get_order_popularity()
    all_products_ids = list(res.values_list('product', flat=True))
    print(all_products_ids)
    all_images = ProductImage.objects.filter(product_id__in=all_products_ids)
    print('all_images: ', all_images)
    places = []
    for i in range(1, len(all_images) + 1):
        places.append(i)
    res = list(zip(places, res))
    context = {'total': res, 'images': all_images, 'places': places}
    return render(request, 'accounts/popular.html', context)

def processOrder(request):
    # transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    print('Data: ', request.body)
    print('Cur User: ', request.user)
    cur_ord, created = Order.objects.get_or_create(user=request.user, complete=False, status_id=1)
    total = float(data['total'])
    print('total from front: ', total)
    print('total back: ', cur_ord.total_price)
    # cur_ord.transaction_id = transaction_id
    #print(cur_ord)
    #print(cur_ord.values_list())
    if total == cur_ord.total_price:
        cur_ord.complete = True
    cur_ord.save()


    return JsonResponse('Заказ отправлен', safe=False)


def update_order(request):
    data = json.loads(request.body)
    print(data)
    cur_ord = Order.objects.get(id=int(data['ord_id']))
    if data['res'] == 'accept':
        print(cur_ord)
        cur_ord.status_id=3
        cur_ord.save()
    elif data['res'] == 'decline':
        print(cur_ord)
        cur_ord.status_id=2
        cur_ord.save()
    return JsonResponse('Заказ обновлен', safe=False)

