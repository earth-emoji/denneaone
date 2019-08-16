import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Vendor, Customer
from catalog.models import Product
from users.models import User

from .extras import generate_order_id
from .models import Order, OrderItem

def get_user_pending_order(request):
    # get order for the correct user
    customer = get_object_or_404(Customer, user=request.user)
    order = Order.objects.filter(customer=customer, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

def get_vendor_pending_orders(request, pk, template_name='orders/vendor_pending_orders.html'):
    vendor = get_object_or_404(Vendor, user=request.user, pk=pk)
    orders = OrderItem.object.filter(vendor=vendor, is_ordered=False)
    data = {}
    data['orders'] = orders
    return render(request, template_name, data)

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    customer = get_object_or_404(Customer, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    # if product in request.user.profile.ebooks.all():
    #     messages.info(request, 'You already own this ebook')
    #     return redirect(reverse('products:product-list')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product, vendor=product.vendor)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(customer=customer, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect('products:product-list')

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('shopping_cart:order_summary')


@login_required()
def order_details(request, template_name='shopping_cart/order_summary.html', **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, template_name, context)

def purchase_success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})