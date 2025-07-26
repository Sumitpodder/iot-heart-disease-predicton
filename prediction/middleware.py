# define auth
from django.shortcuts import redirect

def auth(function):
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect('login')
        return function(request)
    return wrapper

#define guest
def guest(function):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect('home')
        return function(request)
    return wrapper