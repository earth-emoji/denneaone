from django.urls import include, path

from . import views

urlpatterns = [
    path('thanks/', views.thank_you, name='thanks'),
    path('products/', include(([
        path('', views.product_list, name='product-list'),
        path('add/', views.product_create, name='new-product'),
        path('<uuid:slug>/edit/', views.product_edit, name='edit-product'),
        path('<uuid:slug>/update/', views.product_update, name='update-product'),
        path('album/<uuid:slug>/', views.product_photos, name='product-photos'),
    ], 'products'))),
    path('services/', include(([
        path('', views.service_list, name='service-list'),
        path('add/', views.service_create, name='new-service'),
        path('<int:pk>/reserve/', views.reserve_service, name='reserve'),
    ], 'services'))),
]