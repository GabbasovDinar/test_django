from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import OrderForm

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
        if form.is_valid():
            order = form.save(commit=False)
            order.DateOrder = timezone.now()
            order.save()
            return redirect('lunch:order_list')
    else:
        form = OrderForm()
    return render(request, 'lunch/order_new.html', {'form': form})