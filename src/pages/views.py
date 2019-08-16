from django.shortcuts import render, redirect

# Create your views here.
def home(request, template_name='pages/home.html'):
    if request.user.is_authenticated:
        if request.user.is_vendor:
            return redirect('vendors:dashboard', request.user.vendor.slug)
        else:
            return redirect('products:product-list')
    return render(request, template_name)