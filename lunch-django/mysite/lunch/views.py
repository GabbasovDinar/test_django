#from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
#from .models import OrderProductLine
from .models import User, Order, OrderProductLine

def index(request):
    latest_user_list = User.objects.order_by('-RegistrationDate')[:5]
    template = loader.get_template('lunch/index.html')
    context = RequestContext(request, {'latest_user_list': latest_user_list,})   
    return HttpResponse(template.render(context))
def cash(request, cash_id):
    
def orders(request, OrderProductLine_id):
    try:
        orderr = Order.objects.get(pk=OrderProductLine_id)
    except 
    return HttpResponse("You're looking at order %s." % OrderProductLine_id)

def results(request, OrderProductLine_id):
    response = "You're looking at the results of order %s."
    return HttpResponse(response % OrderProductLine_id)

def processing(request, OrderProductLine_id):
    return HttpResponse("You're voting on order %s." % OrderProductLine_id)

def reguser(request, user_id):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % user_id)    
#def regprocessing(request, user_id)
#def login(request, user_id) 
# Create your views here.
