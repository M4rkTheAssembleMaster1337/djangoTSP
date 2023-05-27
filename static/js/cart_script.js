 document.getElementById('make-payment').addEventListener('click', function(e){
        submitData()

    })

    function submitData(){
        console.log('Оплата пошла')

        var user_id = '{{ request.user }}'


        var url = '/process_order/'
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type' : 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'userId': user_id})
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Выполнено: ', data);
            alert('Заказ отправлен');
            window.location.href = "{% url 'home' %}"
        })

    }