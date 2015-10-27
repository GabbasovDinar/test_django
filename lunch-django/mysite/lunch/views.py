from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import *


def index(request):
    latest_user_list = User.objects.order_by('-RegistrationDate')[:5]
    template = loader.get_template('lunch/index.html')
    context = RequestContext(request, {'latest_user_list': latest_user_list,})   
    return HttpResponse(template.render(context))

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'lunch/detail.html', {'user': user})

def results(request, user_id):
    response = "You're looking at the results of order %s."
    return HttpResponse(response % user_id)

def order(request, user_id):
    return HttpResponse("You're voting on order %s." % user_id)

#def reguser(request, user_id):
    #response = "You're looking at the results of user %s."
    #return HttpResponse(response % user_id)    
#def regprocessing(request, user_id)
#def login(request, user_id) 
# Create your views here.
