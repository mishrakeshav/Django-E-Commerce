from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 


def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        

        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order.get('get_cart_items')
        for i in cart:
            cartItems += cart[i]['quantity']
    
    context = {'items':items, 'order':order, 'cartItems' : cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}

    context = {'items':items, 'order':order}
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
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)