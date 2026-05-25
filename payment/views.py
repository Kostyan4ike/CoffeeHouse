from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from orders.models import Order

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.paid = True
        order.save()
        
        return redirect('payment:yoomoney_redirect', order_id=order.id)
    
    return render(request, 'payment/process.html', {'order': order})

def yoomoney_redirect(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total = order.get_total_cost()
    
    # Создаём форму для отправки на ЮMoney
    context = {
        'order': order,
        'total': total,
        'wallet': settings.YOOMONEY_WALLET,
        'success_url': request.build_absolute_uri(reverse('payment:completed')),
        'cancel_url': request.build_absolute_uri(reverse('payment:canceled')),
    }
    return render(request, 'payment/yoomoney_form.html', context)

def payment_completed(request):
    order_id = request.session.get('order_id', None)
    print(f"DEBUG: order_id from session = {order_id}")  # ← добавить
    
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        print(f"DEBUG: order found, paid before = {order.paid}")  # ← добавить
        order.paid = True
        order.save()
        print(f"DEBUG: paid after = {order.paid}")  # ← добавить
    else:
        print("DEBUG: No order_id in session!")
    
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')