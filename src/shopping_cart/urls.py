from django.urls import path, include

from .views import (
    add_to_cart,
    delete_from_cart,
    order_details,
    purchase_success
)

urlpatterns = [
    path('cart/', include(([
        path('add-to-cart/<int:item_id>/', add_to_cart, name="add_to_cart"),
        path('order-summary/', order_details, name="order_summary"),
        path('success/', purchase_success, name='purchase_success'),
        path('item/delete/<int:item_id>/', delete_from_cart, name='delete_item'),
    ], 'shopping_cart'), namespace='shopping_cart')),
]

