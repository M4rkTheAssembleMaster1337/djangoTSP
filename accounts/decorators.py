from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Недостаточно прав для перехода на страницу')

    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('products')
    return wrapper_func
