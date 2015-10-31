from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.generic.base import View

def index(request):
    return render(request, 'lunch/index.html')

def order_list(request):
    latest_order_list = Order.objects.order_by('-DateOrder')[:5]
    context = {'latest_order_list': latest_order_list}     
    return render(request, 'lunch/order_list.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'lunch/order_detail.html', {'order': order})

def order_new(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        #pform = OrderProductLineForm(request.POST)
        if form.is_valid():
            #orderproductline = pform.save(commit=False)
            order = form.save(commit=False)
            order.DateOrder = timezone.now()
            order.save()
            #orderproductline.save()
            return redirect('lunch:order_detail',  order_id=order.id)
    else:
        form = OrderForm()
        #pform = OrderProductLineForm
    return render(request, 'lunch/order_new.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponseRedirect('/lunch/order/')
    else:
        form = LoginForm()
    return render(request, 'lunch/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # TODO:
            # 1. create user,
            # 2. input pass
            # 3. log in your name
            return HttpResponseRedirect('/lunch/order/')

    else:
        form = RegistrationForm()
    return render(request, 'lunch/register.html', {'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/lunch/')