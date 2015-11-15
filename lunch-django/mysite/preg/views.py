from django.contrib.auth.models import User, UserManager
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory

def index(request):
    return render(request, 'preg/index.html')

def order_list(request):
    latest_order_list_true = OrderConfirmation.objects.filter(Confirmation="True").order_by('-DateConfirmation')[:5]
    latest_order_list_false = OrderConfirmation.objects.filter(Confirmation="").order_by('-DateConfirmation')[:5]
    context = {'latest_order_list_true': latest_order_list_true, 'latest_order_list_false': latest_order_list_false}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    return render(request, 'preg/order_list.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(OrderConfirmation, pk=order_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    return render(request, 'preg/order_detail.html', {'order': order})

def order_detail2(request, order_id):
    order = get_object_or_404(OrderConfirmation, pk=order_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    return render(request, 'preg/order_detail2.html', {'order': order})


def confirmation_order(request, confirmation_id):
    order = get_object_or_404(Order, pk=confirmation_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/') 
    if request.method == "POST":
        form = OrderConfirmationForm(request.POST)
        cform = AddCashMoveForm(request.POST)
        if form.is_valid() and cform.is_valid():
            confirmation = form.save(commit=False)
            confirmation.DateConfirmation = timezone.now()
            confirmation.ConfirmationOrderID = order
            confirmation.save()
            
            for e in OrderConfirmation.objects.filter(id=confirmation.id):
                confirmat = e.Confirmation
                tru = True
            if confirmat == tru:
                user_num = len(User.objects.order_by('username'))
                WhoUser=request.user
                product_list = []
                price_list = []
                numproduct_list = []
                for e in Product.objects.filter(orderproductline__OrderID__orderconfirmation__id=confirmation.id):
                    product_list.append(e.NameProduct)
                    price_list.append(e.Price)
                product_list = [str(x) for x in product_list]
                k=0
                for i in product_list:
                    for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=confirmation.id, ProductID__NameProduct=product_list[k]):
                        numproduct_list.append(e.NumProduct)
                    k=k+1
                k=0                 
                user_balance = 0
                for i in product_list:
                    user_balance = user_balance + price_list[k]*numproduct_list[k]
                    k=k+1
                #_____________this user__________________    
                cashmove = CashMove(AmountMoney=user_balance, DateCashMove=timezone.now(), UserCash=request.user.userprofile )           
                cashmove.save() 
                #________________________________________
                
                #_____________others users_______________
                user_list = []
                for e in User.objects.exclude(username=WhoUser):
                    user_list.append(e.username)
                    
                user_list = [str(x) for x in user_list]
                new_balance = (-1)*user_balance/user_num
                
                #for i in user_list:
                    #cashmove = CashMove(AmountMoney=new_balance, DateCashMove=timezone.now(), UserCash=request.user.userprofile )
                    
                    #Balance = UserProfile.objects.get(user__username=user_list[k])
                    #Balance.balance = new_balance
                    #Balance.save()
                    #k=k+1                 
                #__________________________________________
                
                
                Balance = UserProfile.objects.get(user__username=WhoUser)
                Balance.balance = user_balance
                Balance.save()
                
                user_list = []
                for e in User.objects.exclude(username=WhoUser):
                    user_list.append(e.username)
                    
                user_list = [str(x) for x in user_list]
                new_balance = (-1)*user_balance/user_num
                
                k=0
                for i in user_list:
                    Balance = UserProfile.objects.get(user__username=user_list[k])
                    Balance.balance = new_balance
                    Balance.save()
                    k=k+1            
            return redirect('preg:user_order_detail',  confirmation_id=confirmation.id)
    else:
        form = OrderConfirmationForm()
    return render(request, 'preg/confirmation_order.html', {'order': order, 'form': form})


def my_profile(request):
    if request.user.is_authenticated():
        WhoUser=request.user
        confirmation_list = OrderConfirmation.objects.filter(ConfirmationOrderID__UserID__user__username=WhoUser).order_by('-DateConfirmation')
        cash_list = CashMove.objects.filter(UserCash__user__username=WhoUser).order_by('-DateCashMove')
        context = {'cash_list':cash_list, 'confirmation_list':confirmation_list}
        return render(request, 'preg/profile.html', context)
    else:
        return HttpResponseRedirect('/preg/login/')  
    
def user_order_detail(request, confirmation_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')     
    order = get_object_or_404(OrderConfirmation, pk=confirmation_id)     
    return render(request, 'preg/user_order_detail.html', {'order': order})

def order_new(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/') 
    #ProductFormSet = formset_factory(ProductForm, extra=3)
    if request.method == "POST":
        oform = OrderForm(request.POST)
        pform = ProductForm(request.POST)
        #pform = ProductFormSet(request.POST)
        if oform.is_valid() and pform.is_valid():
            order = oform.save(commit=False)
            order.DateOrder = timezone.now()
            order.UserID = request.user.userprofile 
            order.save()
            product = pform.save(commit=False)
            product.OrderID = order
            product.save()
            return redirect('preg:confirmation_order',  confirmation_id=order.id)
    else:
        oform = OrderForm()
        pform = ProductForm()
        #pform = ProductFormSet()
        

    return render(request, 'preg/order_new.html', {'pform': pform})


def edit_confirmation(request, confirmation_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')  
    order = get_object_or_404(OrderConfirmation, pk=confirmation_id)
    if request.method == "POST":
        form = ConfirmationEditForm(request.POST or None)
        if form.is_valid():
            order.Confirmation = form.cleaned_data['Confirmation']
            order.DateConfirmation = timezone.now()
            order.save()
            for e in OrderConfirmation.objects.filter(id=confirmation_id):
                confirmat = e.Confirmation
            tru = True
            if confirmat == tru:
                user_list = len(User.objects.order_by('username'))
                WhoUser=request.user
                #my_balance = 5
                cashmove = CashMove(AmountMoney=100, DateCashMove=timezone.now(), UserCash=request.user.userprofile )           
                cashmove.save()              
            return HttpResponseRedirect('/preg/order/profile/')
        
    else:
        form = ConfirmationEditForm()
    return render(request, 'preg/edit_confirmation.html', {'form': form})    
    
def edit_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    username = request.user.username
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = ProfilEditForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/preg/order/profile/')
    else:
        form = ProfilEditForm()   
    return render(request, 'preg/edit.html', {'form': form})

def edit_pass(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    username = request.user.username
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = PassEditForm(request.POST or None)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user = authenticate(username = username, password = form.cleaned_data['password1'])
            login(request, user)            
            return HttpResponseRedirect('/preg/order/profile/')
    else:
        form = PassEditForm()
    return render(request, 'preg/edit_pass.html', {'form': form})

    

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
        cform = CashUserForm(request.POST)
        if form.is_valid() and cform.is_valid():
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            login(request, user)
            cashmove = cform.save(commit=False)
            cashmove.DateCashMove = timezone.now()
            cashmove.AmountMoney = float('0')
            cashmove.UserCash = request.user.userprofile             
            cashmove.save()
            return HttpResponseRedirect('/preg/order/')
    else:
        form = RegistrationForm()
    return render(request, 'preg/register.html', {'form': form})
                   
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/preg/')