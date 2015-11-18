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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    latest_order_list_true = OrderConfirmation.objects.filter(Confirmation=True).order_by('-DateConfirmation')[:5]
    latest_order_list_false = OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=True).order_by('DateConfirmation')
    latest_order_list_processing_false = OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=False).order_by('-DateConfirmation')
    context = {'latest_order_list_true': latest_order_list_true, 'latest_order_list_false': latest_order_list_false, 'latest_order_list_processing_false': latest_order_list_processing_false}
    return render(request, 'preg/order_list.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(OrderConfirmation, pk=order_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    return render(request, 'preg/order_detail.html', {'order': order})

def order_detail2(request, order_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    order = get_object_or_404(OrderConfirmation, pk=order_id)
    if request.method == "POST":
        form = ConfirmationEditForm(request.POST or None)
        if form.is_valid():
            order.OrderProcessing = True
            order.DateProcessing= timezone.now()
            order.save()            
            return HttpResponseRedirect('/preg/order/')
        else:
            form = ConfirmationEditForm()    
    return render(request, 'preg/order_detail2.html', {'order': order})

def order_detail3(request, order_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')    
    order = get_object_or_404(OrderConfirmation, pk=order_id)
    if request.method == "POST":
        form = ConfirmationEditForm(request.POST or None)
        if form.is_valid():
            order.Confirmation = True
            order.DateConfirmation = timezone.now()
            order.save()            
            return HttpResponseRedirect('/preg/order/')
        else:
            form = ConfirmationEditForm()  
    return render(request, 'preg/order_detail3.html', {'order': order})

def confirmation_order(request, confirmation_id):
    order = get_object_or_404(Order, pk=confirmation_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/') 
    if request.method == "POST":
        form = OrderConfirmationForm(request.POST)
        if form.is_valid():
            confirmation = form.save(commit=False)
            confirmation.Confirmation = False
            confirmation.DateConfirmation = timezone.now()
            confirmation.ConfirmationOrderID = order
            confirmation.save()
            return HttpResponseRedirect('/preg/order/') 
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
            product.Confirmation = False
            product.save()
            return redirect('preg:confirmation_order',  confirmation_id=order.id)
    else:
        oform = OrderForm()
        pform = ProductForm()
        #pform = ProductFormSet()
    return render(request, 'preg/order_new.html', {'pform': pform})

def all_order(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    all_order_list = OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=False).order_by('-DateConfirmation')
    context = {'all_order_list': all_order_list}    
    user_id = []
    for e in OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=False):
        user_id.append(e.id)
    k=0
    for i in user_id:
        order = get_object_or_404(OrderConfirmation, pk=user_id[k])
        if request.method == "POST":
            form = ConfirmationEditForm(request.POST or None)
            if form.is_valid():
                order.OrderProcessing = True
                order.DateProcessing= timezone.now()
                order.save()            
            else:
                form = ConfirmationEditForm()  
        k=k+1
    return render(request, 'preg/all_order.html', context)

def all_confirmation(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    all_confirmation_list = OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=True).order_by('-DateConfirmation')    
    context = {'all_confirmation_list': all_confirmation_list}  
    user_id_confirmation = []
    for e in OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=True):
        user_id_confirmation.append(e.id)
    #_________________________________________________________    
    WhoUser=request.user
    list_user = []
    for e in User.objects.filter(userprofile__order__orderconfirmation__OrderProcessing=True, userprofile__order__orderconfirmation__Confirmation=False):
        list_user.append(e.username)
    list_user = [str(x) for x in list_user]
    
    product_list = []
    price_list = []
    numproduct_list = []  
    user_product_list = []
    user_price_list = []
    k=0
    
    for i in list_user:
        for e in Product.objects.filter(orderproductline__OrderID__orderconfirmation__Confirmation=False, orderproductline__OrderID__orderconfirmation__OrderProcessing = True, orderproductline__OrderID__UserID__user__username=list_user[k]):
            product_list.append(e.NameProduct)
            price_list.append(e.Price)
        product_list = [str(x) for x in product_list]       
        user_product_list.append(product_list)
        user_price_list.append(price_list)
        product_list = []
        price_list = [] 
        k=k+1
        
    d = 0
    k = 0
    user_numproduct_list = []
    for i in list_user:
        for j in user_product_list[d]:
            for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__OrderProcessing=True, OrderID__orderconfirmation__Confirmation=False, ProductID__NameProduct=user_product_list[d][k], OrderID__UserID__user__username=list_user[d]):
                numproduct_list.append(e.NumProduct)
            k=k+1
        user_numproduct_list.append(numproduct_list)
        numproduct_list = []
        d=d+1
        k=0
        
    user_sum_list = []
    k=0
    for i in user_numproduct_list:
        for j in user_numproduct_list[k]:
            sum_user = user_numproduct_list[k]*user_price_list[k] #ISPRAVIT OSHIBKA
            user_sum_list.append(sum_user) 
        k=k+1
        
    


    #_________________________________
    k=0
    for i in user_id_confirmation:
        order = get_object_or_404(OrderConfirmation, pk=user_id_confirmation[k])
        if request.method == "POST":
            form = ConfirmationEditForm(request.POST or None)
            if form.is_valid():
                order.Confirmation = True
                order.DateConfirmation = timezone.now()
                order.save()            
            else:
                form = ConfirmationEditForm()  
        k=k+1      
    return render(request, 'preg/all_confirmation.html', context)
    
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