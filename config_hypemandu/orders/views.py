from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import OrderCreateForm
from .models import OrderItem,Order
from cart.cart_ import Cart
from .tasks import order_created
from django.http import JsonResponse
import requests


def order_create(request):
    cart=Cart(request)
    print('order_create')
    if request.method=='POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            pm=form.cleaned_data.get('payment_method')
            order=form.save()
            if pm =='Khalti':
                return redirect(reverse('orders:khalti_request')+'?o_id='+str(order.id))
            else:
            # for item in cart:
            #     OrderItem.objects.create(order=order,
            #                              product=item['product'],
            #                              price=item['price'],
            #                              quantity=item['quantity']
            #                              )
            #     cart.clear()
            #     order_created.delay(order.id)
            
                return render(request,'orders/order/created.html',{'order':order})
    else:
        form=OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})

def khaltiRequest(request):
    print(request.GET.get('o_id'))
    o_id=request.GET.get('o_id')
    order=Order.objects.get(id=o_id)
    cart=Cart(request)
    print(order)
    return render(request,'payment/payment_khalti.html',{
        "order":order,
        "cart":cart,
    })

def khaltiVerify(request):
    token=request.GET.get("token")
    amount=request.GET.get("amount")
    o_id=request.GET.get("order_id")
    print(token,amount,o_id)
    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
    'token': token,
    'amount': amount
    }

    headers = {
    'Authorization': 'Key test_secret_key_339be54f03e7454c8b66021dabb48b31'
    }
    order_obj=Order.objects.get(id=o_id)
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_dict=response.json()
    if resp_dict.get("idx"):
        success=True
        order_obj.payment_completed=True
        order_obj.save()
    else:
        success=False
    print(resp_dict)
    data={
        "success":success,
    }
    return JsonResponse(data)