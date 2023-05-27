var form_fields = document.getElementsByTagName('input')
form_fields[1].placeholder = 'Имя пользователя..'
form_fields[2].placeholder = 'Почта..'
form_fields[3].placeholder = 'Пароль..'
form_fields[4].placeholder = 'Повторите пароль..'


form_fields[1].className += 'form-control'
form_fields[2].className += 'form-control'
form_fields[3].className += 'form-control'
form_fields[4].className += 'form-control'