var updateBtns = document.getElementsByClassName('buy')

console.log(updateBtns.length)

for(var k = 0; k < updateBtns.length; k++){
    updateBtns[k].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId, 'action:',action)

        updateUserOrder(productId, action)
    })
}

function updateUserOrder(productId, action){
    console.log('Sending data')
    var url = '/update_item/'

    fetch(url, {
    method:'POST',
    headers:{
    'Content-Type' : 'application/json',
    'X-CSRFToken': csrftoken,
    },
    body:JSON.stringify({'productId':productId, 'action':action})

    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data: ', data)
        location.reload()
    })
}
