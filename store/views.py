from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cart_data, cookie_cart,guest_order


def store(request):
    data = cart_data(request)
    items = data['items']
    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    
    data = cart_data(request)
    items = data['items']
    cartItems = data['cartItems']
    order = data['order']

    context = {'items':items, 'order':order, 'cartItems' : cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cart_data(request)
    items = data['items']
    cartItems = data['cartItems']
    order = data['order']

    context = {'items':items, 'order':order, 'cartItems' : cartItems}
    return render(request, 'store/checkout.html', context)

def update_cart(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user.customer 
    product = get_object_or_404(Product,pk=product_id)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    order_item,created = OrderItem.objects.get_or_create(order=order,product=product)
    
    if action == 'add':
        order_item.quantity += 1 
    elif action == 'remove':
        order_item.quantity -= 1 
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse({'response': 'Item was added'})

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guest_order(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)