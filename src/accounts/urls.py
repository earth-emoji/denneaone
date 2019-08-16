from django.urls import include, path

from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.UserSignUpView.as_view(), name='user_signup'),
    path('vendors/', include(([
        path('<uuid:slug>/', views.dashboard, name='dashboard'),
        path('<uuid:slug>/products', views.vendor_products, name='vendor-products'),
        path('<uuid:slug>/reservations', views.vendor_reservations, name='vendor-reservations'), 
    ], 'vendors'))),
]