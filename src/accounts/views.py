from django.contrib.auth import logout, login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from accounts.forms import CustomerSignUpForm
from accounts.models import Customer, Vendor
from catalog.models import Product, Reservation
from users.models import User


class UserSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'User'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


def dashboard(request, slug, template_name='vendors/dashboard.html'):
    vendor = Vendor.objects.get(slug=slug)
    data = {
        'vendor': vendor
    }
    return render(request, template_name, data)


def vendor_products(request, slug, template_name='vendors/vendor_products.html'):
    data = {}
    vendor = Vendor.objects.get(slug=slug)
    if not (vendor.user == request.user):
        return HttpResponse("It is not yours ! You are not permitted !", content_type="application/json", status=403)
    products = Product.objects.filter(vendor=vendor)
    data['products'] = products
    return render(request, template_name, data)


def vendor_reservations(request, slug, template_name='vendors/vendor_reservations.html'):
    vendor = Vendor.objects.get(slug=slug)
    reservations = Reservation.objects.filter(product__vendor__id=vendor.id)
    data = {
        'reservations': reservations
    }
    return render(request, template_name, data)