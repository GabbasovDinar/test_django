from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import *

def index(request):
    latest_order_list = Order.objects.order_by('-DateOrder')[:5]
    context = {'latest_order_list': latest_order_list}  
    return render(request, 'lunch/index.html', context)


def detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'lunch/detail.html', {'order': order})

def results(request, order_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % order_id)

def userorder(request, order_id):
    return HttpResponse("You're voting on question %s." % order_id)



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

