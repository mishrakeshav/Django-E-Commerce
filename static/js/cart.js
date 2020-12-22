const updateItems = document.getElementsByClassName('update-cart');

for(var i = 0 ; i < updateItems.length; i++){
    updateItems[i].addEventListener('click', function(){
        const product = this.dataset.product;
        const action = this.dataset.action;
        console.log(product,action);
        if(user == 'AnonymousUser'){
            addCookieItem(product, action)
        }else{
            updateUserOrder(product,action);
        }
    });
}

function updateUserOrder(productId,action){
    url = '/update-cart/';
    fetch(url,{
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action}),
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        location.reload()
    })
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}
