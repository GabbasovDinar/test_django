from django.contrib.auth.models import User, UserManager
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse, render_to_response
from django.utils import timezone
from .models import *
from .forms import *
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import modelformset_factory
from django.template import RequestContext

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
            for e in OrderConfirmation.objects.filter(id=order.id):
                confirmat = e.Confirmation
                processing = e.OrderProcessing
            confirmatFalse = True
            processingTrue = True
            if confirmat == confirmatFalse and processing==processingTrue:
                WhoUser=request.user #this user
                product_list = []
                price_list = []
                numproduct_list = []
                for e in Product.objects.filter(orderproductline__Confirmation=True, orderproductline__OrderID__orderconfirmation__id=order.id):
                    product_list.append(e.NameProduct)
                    price_list.append(e.Price)
                product_list = [str(x) for x in product_list]
                
                k=0
                for i in product_list:
                    for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=order.id, ProductID__NameProduct=product_list[k]):
                        numproduct_list.append(e.NumProduct)
                    k=k+1
                k=0                 
                user_balance = 0
                for i in product_list:
                    user_balance = user_balance + price_list[k]*numproduct_list[k]
                    k=k+1
                    
                other_user_balance = float((-1)*user_balance)
                #_____________other user CashMove_______________
                user_this_order = []
                for e in User.objects.filter(userprofile__order__orderconfirmation__id=order.id):
                    user_this_order.append(e.username)
                    user_this_id = e.id
                cashmove = CashMove(AmountMoney=other_user_balance, DateCashMove=timezone.now(), UserCash_id=user_this_id )
                cashmove.save()
                 
                #_____________others user balance____________                
                for e in UserProfile.objects.filter(user__id=user_this_id):
                    this_balance_users=e.balance   
                
                new_balance = other_user_balance + this_balance_users
                
                Balance = UserProfile.objects.get(user__id=user_this_id)
                Balance.balance = new_balance
                Balance.save()
                    
                #_____________this user CashMove__________________    
                cashmove = CashMove(AmountMoney=user_balance, DateCashMove=timezone.now(), UserCash=request.user.userprofile )           
                cashmove.save() 
                #________________________________________
                
                #_____________this user balance____________
                for e in UserProfile.objects.filter(user__username=WhoUser):
                    this_balance = e.balance              
                new_user_balance = this_balance + user_balance
                Balance = UserProfile.objects.get(user__username=WhoUser)
                Balance.balance = new_user_balance
                Balance.save()
                #__________________________________________              
            return HttpResponseRedirect('/preg/order/')
        else:
            form = ConfirmationEditForm()  
    return render(request, 'preg/order_detail3.html', {'order': order})

def confirmation_order(request, confirmation_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')     
    order = get_object_or_404(Order, pk=confirmation_id)
    product_list = []
    price_list = []
    numproduct_list = []
    for e in Product.objects.filter(orderproductline__OrderID__id=order.id):
        product_list.append(e.NameProduct)
        price_list.append(e.Price)
    product_list = [str(x) for x in product_list]
    k=0
    for i in product_list:
        for e in OrderProductLine.objects.filter(OrderID__id=order.id, ProductID__NameProduct=product_list[k]):
            numproduct_list.append(e.NumProduct)
        k=k+1
    
    k=0                 
    user_balance = 0
    for i in product_list:
        user_balance = user_balance + price_list[k]*numproduct_list[k]
        k=k+1       
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
    return render(request, 'preg/confirmation_order.html', {'order': order, 'form': form, 'user_balance': user_balance})

def del_this_order(request, confirmation_id):
    Order.objects.filter(id=confirmation_id).delete()
    return render(request, 'preg/del_this_order.html')

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
    product_list = []
    price_list = []
    numproduct_list = []
    for e in Product.objects.filter(orderproductline__OrderID__orderconfirmation__id=order.id):
        product_list.append(e.NameProduct)
        price_list.append(e.Price)
    product_list = [str(x) for x in product_list]
    k=0
    for i in product_list:
        for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=order.id, ProductID__NameProduct=product_list[k]):
            numproduct_list.append(e.NumProduct)
        k=k+1
    k=0                 
    user_balance = 0
    for i in product_list:
        user_balance = user_balance + price_list[k]*numproduct_list[k]
        k=k+1    
    return render(request, 'preg/user_order_detail.html', {'order': order, 'user_balance': user_balance})

@login_required
def order_new(request):
    user = request.user
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False  
    TodoItemFormSet = formset_factory(ProductForm, max_num=10, formset=RequiredFormSet)
    if request.method == "POST":
        todo_list_form = OrderForm(request.POST)
        sform = SimpleForm(request.POST)
        todo_item_formset = TodoItemFormSet(request.POST, request.FILES)
        if todo_list_form.is_valid() and todo_item_formset.is_valid() and sform.is_valid():   
            todo_list = todo_list_form.save(commit=False)
            todo_list.DateOrder = timezone.now()
            todo_list.UserID = request.user.userprofile
            todo_list.save()  
            
            #-----------------this is random order-----------------------
            
            random_user_product_id = sform.cleaned_data['Random_order']
            if random_user_product_id!=None:
                product_category_id = random_user_product_id #for example
                random_product_id = []
                k=0
                import random
                for i in product_category_id:
                    random_product_list_id = []
                    for e in Product.objects.filter(ProductCategoryID__id=product_category_id[k]):
                        random_product_list_id.append(e.id)
                    random_product_id.append(random.choice(random_product_list_id))
                    k=k+1
                    
                random_num_product = 1 #num product for random order
                k=0  
                for i in random_product_id:  
                    product = OrderProductLine(NumProduct=random_num_product, Confirmation=True, OrderID_id=todo_list.id, ProductID_id=random_product_id[k])
                    product.save()  
                    k=k+1
                
            #------------------------------------------------------------
            
            
            for form in todo_item_formset.forms:
                todo_item = form.save(commit=False)
                todo_item.OrderID = todo_list
                todo_item.Confirmation = True
                todo_item.NumProduct = form.cleaned_data['NumProduct']
                todo_item.save()            
            return redirect('preg:confirmation_order',  confirmation_id=todo_list.id)
    else:
        sform = SimpleForm()
        todo_list_form = OrderForm()
        todo_item_formset = TodoItemFormSet() 
    c = {'todo_list_form': todo_list_form, 'todo_item_formset': todo_item_formset, 'sform': sform}
    c.update(csrf(request)) 
    return render_to_response('preg/order_new.html', c)

def all_order(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    user_price_list2 = []  
    user_id_list = []
    all_order_list = OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=False).order_by('-DateConfirmation')
    for e in OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=False):
        user_id_list.append(e.id)
        
    kk=0
    for i in user_id_list:
        order = get_object_or_404(OrderConfirmation, pk=user_id_list[kk])
        if request.method == "POST":
            form = ConfirmationEditForm(request.POST or None)
            if form.is_valid():
                order.OrderProcessing = True
                order.DateProcessing= timezone.now()
                order.save()
            else:
                form = ConfirmationEditForm()
        product_list2 = []
        price_list2 = []
        numproduct_list2 = []
        for e in Product.objects.filter(orderproductline__OrderID__orderconfirmation__id=order.id):
            product_list2.append(e.NameProduct)
            price_list2.append(e.Price)
        product_list2 = [str(x) for x in product_list2]
        k=0
        for i in product_list2:
            for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=order.id, ProductID__NameProduct=product_list2[k]):
                numproduct_list2.append(e.NumProduct)
            k=k+1
    
        k=0                 
        user_balance2 = 0
        for i in product_list2:
            user_balance2 = user_balance2 + price_list2[k]*numproduct_list2[k]
            k=k+1                
        user_price_list2.append(user_balance2)        
        kk=kk+1
    k=0
    user_price_list_sum = 0
    for i in user_price_list2:
        user_price_list_sum = user_price_list_sum + user_price_list2[k]
        k=k+1   
    context = {'all_order_list': all_order_list, 'user_price_list_sum': user_price_list_sum}  
    return render(request, 'preg/all_order.html', context)

def all_confirmation(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')
    
    all_confirmation_list = OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=True).order_by('-DateConfirmation')
    user_price_list2 = [] 
    user_id_confirmation = []
    for e in OrderConfirmation.objects.filter(Confirmation=False, OrderProcessing=True):
        user_id_confirmation.append(e.id)
    #_________________________________________________________    
    WhoUser=request.user
    list_user = []
    id_list = []
    k=0
    for i in user_id_confirmation:
        for e in User.objects.filter(userprofile__order__orderconfirmation__id=user_id_confirmation[k]):
            list_user.append(e.username)
            id_list.append(e.id)
        k=k+1
    list_user = [str(x) for x in list_user]
    
    all_order_for_user = []
    product_list = []
    price_list = []
    numproduct_list = []  
    user_product_list = []
    user_price_list = []
    k1=0
    
    for i in list_user:
        for e in Product.objects.filter(orderproductline__Confirmation=True, orderproductline__OrderID__orderconfirmation__id=user_id_confirmation[k1]):
            product_list.append(e.NameProduct)
            price_list.append(e.Price)
        product_list = [str(x) for x in product_list]       
        user_product_list.append(product_list)
        user_price_list.append(price_list)
        product_list = []
        price_list = [] 
        k1=k1+1
    #up corrected 
    #error the end massiv is not correct
    #2 errors when name of products odinakovie
    #_________________________________________________
    d = 0
    k = 0
    user_numproduct_list = []

    for i in user_id_confirmation:
        for j in user_product_list[d]:
            for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=user_id_confirmation[d], ProductID__NameProduct=user_product_list[d][k]):
                numproduct_list.append(e.NumProduct)
            k=k+1
        user_numproduct_list.append(numproduct_list)
        numproduct_list = []
        d=d+1
        k=0
        
    user_sum_list = []
    sum_list = []
    k=0
    d=0
    for i in user_numproduct_list:
        for j in user_numproduct_list[d]:
            sum_list.append(user_numproduct_list[d][k]*user_price_list[d][k])
            k=k+1
        user_sum_list.append(sum_list)
        sum_list = []
        d=d+1
        k=0
        
    user_sum_order_list = []
    sum_element = 0
    d=0
    k=0
    for j in user_sum_list:
        for i in user_sum_list[d]:
            sum_element = sum_element + user_sum_list[d][k]
            k=k+1
        user_sum_order_list.append(sum_element)
        d=d+1
        k=0
        sum_element = 0
    #_________________________________________
    check = False
    #_________________________________________
    kk=0
    for i in user_id_confirmation:
        order = get_object_or_404(OrderConfirmation, pk=user_id_confirmation[kk])
        if request.method == "POST":
            form = ConfirmationEditForm(request.POST or None)
            if form.is_valid():
                order.Confirmation = True
                order.DateConfirmation = timezone.now()
                order.save() 
                check = True
            else:
                form = ConfirmationEditForm() 
        product_list = []
        price_list = []
        numproduct_list = []
        for e in Product.objects.filter(orderproductline__OrderID__orderconfirmation__id=order.id, orderproductline__Confirmation=True):
            product_list.append(e.NameProduct)
            price_list.append(e.Price)
        product_list = [str(x) for x in product_list]
        k=0
        for i in product_list:
            for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=order.id, ProductID__NameProduct=product_list[k]):
                numproduct_list.append(e.NumProduct)
            k=k+1
    
        k=0                 
        user_balance = 0
        for i in product_list:
            user_balance = user_balance + price_list[k]*numproduct_list[k]
            k=k+1                
        user_price_list2.append(user_balance)  
        kk=kk+1 
    if check==True:
        #CashMove all Users
        new_sum = []
        k=0
        for i in user_sum_order_list:
            new_sum.append(float(user_sum_order_list[k]*(-1)))
            k=k+1
        k=0
        for i in list_user:
            cashmove = CashMove(AmountMoney=new_sum[k], DateCashMove=timezone.now(), UserCash_id=id_list[k] )
            cashmove.save()
            k=k+1
            
        #Save balans all users
        k=0
        this_balance_users = []
        this_cashmove_users = []
        for i in list_user:    
            for e in UserProfile.objects.filter(user__username=list_user[k]):
                this_balance_users.append(e.balance)
            for e in CashMove.objects.filter(UserCash__user__username=list_user[k]):
                this_cashmove = e.AmountMoney
            this_cashmove_users.append(this_cashmove) 
            k=k+1
        k=0   
        this_new_balance_user = []
        for i in this_cashmove_users:
            this_new_balance_user.append(this_cashmove_users[k]+this_balance_users[k])
            k=k+1
            
        k=0   
        for i in list_user: 
            Balance = UserProfile.objects.get(user__username=list_user[k])
            Balance.balance = this_new_balance_user[k]
            Balance.save()
            k=k+1
     
        #CashMove this User
        cash_sum_this_user = 0
        k=0
        for i in user_sum_order_list:
            cash_sum_this_user=cash_sum_this_user+user_sum_order_list[k]
            k=k+1
        cashmove = CashMove(AmountMoney=cash_sum_this_user, DateCashMove=timezone.now(), UserCash=request.user.userprofile )           
        cashmove.save()    
            
        #this user balance 
        for e in UserProfile.objects.filter(user__username=WhoUser):
            this_balance = e.balance 
        # save balance this user
        for e in CashMove.objects.filter(UserCash__user__username=WhoUser):
            this_cashmove = e.AmountMoney 
            
        new_user_balance = this_balance + this_cashmove 
        
        Balance = UserProfile.objects.get(user__username=WhoUser)
        Balance.balance = new_user_balance
        Balance.save()  
    k=0
    user_price_list_sum = 0
    for i in user_price_list:
        user_price_list_sum = user_price_list_sum + user_price_list2[k]
        k=k+1     
    context = {'all_confirmation_list': all_confirmation_list, 'user_price_list_sum': user_price_list_sum}  
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

def edit_confirmation_this_product(request, order_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/preg/login/')       
    order = get_object_or_404(OrderProductLine, pk=order_id)
    if request.method == "POST":
        form = ConfirmationEditForm(request.POST or None)
        if form.is_valid():
            order.Confirmation = form.cleaned_data['Confirmation']
            order.save()          
            return HttpResponseRedirect('/preg/order/')
    else:
        form = ConfirmationEditForm()
    return render(request, 'preg/edit_confirmation_this_product.html', {'form': form})

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