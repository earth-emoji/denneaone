import decimal

import simplejson as json
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from accounts.models import Vendor
from photos.forms import PhotoForm
from photos.models import Album, Photo
from shopping_cart.models import Order
from users.decorators import vendor_required, customer_required
from users.models import Acl

from .forms import ProductForm, ReservationForm, ServiceForm
from .models import Category, Product, Reservation


# Create your views here.
@login_required
@customer_required
def product_list(request, template_name='products/product_list.html'):
    # acl_obj = Acl.objects.get(name=acl)
    
    qs1 = Product.objects.filter(product_type='PRODUCT', acl__name=request.user.acl.name)
    qs2 = Product.objects.filter(product_type='PRODUCT', is_aux=True)
    
    object_list = qs1 | qs2
    
    filtered_orders = Order.objects.filter(
        customer=request.user.customer, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [
            product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, template_name, context)


@login_required
@customer_required
def service_list(request, template_name='products/service_list.html'):
    services = Product.objects.filter(product_type='SERVICE')
    data = {}
    data["services"] = services
    return render(request, template_name, data)


@login_required
@vendor_required
def product_create(request, template_name='products/product_form.html'):
    vendor = Vendor.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            c = form.save(commit=False)
            c.product_type = 'PRODUCT'
            c.vendor = vendor
            album = Album.objects.create(name=c.name, owner=request.user)
            c.album = album
            c.save()
            return redirect('products:edit-product', c.slug)
    else:
        form = ProductForm()

    return render(request, template_name, {'form': form})


@login_required
@vendor_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_form = ProductForm(instance=product)
    image = Photo.objects.filter(album=product.album).first()

    return render(request, 'products/product_edit.html', {
        'product': product,
        'product_form': product_form,
        'image': image
    })


@login_required
@vendor_required
def product_photos(request, slug):
    album = get_object_or_404(Album, slug=slug)

    if request.method == 'POST':
        form = PhotoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            c = form.save(commit=False)
            c.album = album
            c.save()
            redirect('products:product-photos', slug)
    else:
        form = PhotoForm()

    return render(request, 'products/product_photos.html', {
        'form': form,
        'album': album
    })


@login_required
@vendor_required
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if not product.vendor.id == request.user.vendor.id:
        return JsonResponse("It is not yours ! You are not permitted !", status=403)
    if request.POST:
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            c = form.save(commit=False)
            data = {
                'success': True,
                'name': c.name,
                'description': c.description,
                'price': c.price,
                'stock': c.stock_quantity
            }
            c.save()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': form.errors})
    return JsonResponse({})


def service_create(request, template_name='products/service_form.html'):
    form = ServiceForm(request.POST or None)
    if form.is_valid():
        c = form.save(commit=False)
        c.product_type = 'SERVICE'
        c.vendor = request.user.vendor
        c.save()
        return redirect('vendors:vendor-products', request.user.vendor.slug)
    return render(request, template_name, {'form': form})


@login_required
def reserve_service(request, pk, template_name='products/reserve_service.html'):
    service = Product.objects.get(pk=pk)

    if not(service.product_type == 'SERVICE'):
        return redirect('products:product-list')
    data = {}

    form = ReservationForm(request.POST or None, product=service)
    if request.method == "POST":
        if form.is_valid():
            c = form.save(commit=False)
            c.product = service
            c.client = request.user.customer
            c.save()
            return redirect('thanks')

    data['form'] = form
    data['service'] = service

    return render(request, template_name, data)


@login_required
def thank_you(request, template_name='products/thank_you.html'):
    return render(request, template_name)
