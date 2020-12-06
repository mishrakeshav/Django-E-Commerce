const updateItems = document.getElementsByClassName('update-cart');

for(var i = 0 ; i < updateItems.length; i++){
    updateItems[i].addEventListener('click', function(){
        const product = this.dataset.product;
        const action = this.dataset.action;
        console.log(product,action);
        if(user == 'AnonymousUser'){
            console.log('Not logged in');
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