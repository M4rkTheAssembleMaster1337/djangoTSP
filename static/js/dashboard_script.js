    var btns_accept = document.getElementsByClassName('accept')
    var btns_decline = document.getElementsByClassName('decline')
    console.log(btns_accept.length)
    for(var k = 0; k < btns_accept.length; k++){
        btns_accept[k].addEventListener('click', function(){
            var ord_id = this.dataset.order
            var temp = 'accept'
            updateOrder(ord_id, temp)
        })
        btns_decline[k].addEventListener('click', function(){
            var ord_id = this.dataset.order
            var temp = 'decline'
            updateOrder(ord_id, temp)
        })

    }

    function updateOrder(ord_id, res){
        console.log('Заказ обновляется')

        var url = '/update_order/'
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type' : 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'ord_id': ord_id, 'res': res})
        })
        .then((response) => response.json())
        .then((data)=>{
        console.log('data: ', data)
        location.reload()
        })

    }