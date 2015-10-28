from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .forms import UserForm
from .models import *

def index(request):
    latest_order_list = Order.objects.order_by('-DateOrder')[:5]
    context = {'latest_order_list': latest_order_list}  
    return render(request, 'lunch/index.html', context)


def detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'lunch/detail.html', {'order': order})

def neworder(request):
    latest_user_list = User.objects.order_by('NameUser')
    latest_product_list = Product.objects.order_by('NameProduct')
    latest_delivery_list = DeliveryService.objects.order_by('NameServis')
    context = {'latest_user_list': latest_user_list, 'latest_product_list': latest_product_list, 'latest_delivery_list': latest_delivery_list} 
    return render(request, 'lunch/neworder.html', context)

def newuser(request):
    form = UserForm
    return render(request, 'lunch/newuser.html', form)

def results(request, order_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % order_id)


#def index(request):
    #latest_user_list = User.objects.order_by('-RegistrationDate')[:5]
    #template = loader.get_template('lunch/index.html')
    #context = RequestContext(request, {'latest_user_list': latest_user_list,})   
    #return HttpResponse(template.render(context))

#def detail(request, user_id):
    #user = get_object_or_404(User, pk=user_id)
    #return render(request, 'lunch/detail.html', {'user': user})

#def results(request, user_id):
    #response = "You're looking at the results of order %s."
    #return HttpResponse(response % user_id)

#def order(request, user_id):
    #return HttpResponse("You're voting on order %s." % user_id)

