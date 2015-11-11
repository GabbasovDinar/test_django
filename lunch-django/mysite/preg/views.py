
from django.contrib.auth.models import User, UserManager
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'preg/index.html')

def order_list(request):
    latest_order_list = Order.objects.order_by('-DateOrder')[:5]
    context = {'latest_order_list': latest_order_list}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    return render(request, 'preg/order_list.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    return render(request, 'preg/order_detail.html', {'order': order})

def my_profile(request):
    if request.user.is_authenticated():
        WhoUser=request.user
        order_list = Order.objects.filter(UserID__user__username=WhoUser).order_by('-DateOrder')
        cash_list = CashMove.objects.filter(UserCash__user__username=WhoUser).order_by('-DateCashMove')
        context = {'order_list': order_list, 'cash_list':cash_list}
        return render(request, 'preg/profile.html', context)
    else:
        return HttpResponseRedirect('/preg/login/')  
    
def user_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/') 
    return render(request, 'preg/user_order_detail.html', {'order': order})

def order_new(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/') 
    if request.method == "POST":
        oform = OrderForm(request.POST)
        pform = ProductForm(request.POST)
        if oform.is_valid() and pform.is_valid():
            order = oform.save(commit=False)
            order.DateOrder = timezone.now()
            order.save()
            product = pform.save(commit=False)
            product.OrderID = order
            product.save()
            return redirect('preg:order_detail',  order_id=order.id)
    else:
        oform = OrderForm()
        pform = ProductForm()
        
    user_list = User.objects.order_by('username')
    user_list = len(user_list)
    WhoUser=request.user
    #num_product = 
    
    return render(request, 'preg/order_new.html', {'oform': oform, 'pform': pform})

def edit_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    if request.method == "POST":
        form = ProfilEditForm(request.POST)
        if form.is_valid():
            request.user.save()
            return HttpResponseRedirect('/preg/order/profile/')
    else:
        form = ProfilEditForm()   
    return render(request, 'preg/edit.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponseRedirect('/preg/order/')
    else:
        form = LoginForm()
    return render(request, 'preg/login.html', {'form': form})

def register(request):
    user=User()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('/preg/order/')
    else:
        form = RegistrationForm()
    return render(request, 'preg/register.html', {'form': form})
                   
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/preg/')