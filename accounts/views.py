from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render
from .form import UserLoginForm ,UserRegisterForm


# Create your views here.
def login_view(request):
    print(request.user)
    title="Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        #print(request.user.is_authenticated())
    return render(request, "form.html", {"form":form, "title": title})

def register_view(request):
    title= " Regiter"
    form= UserRegisterForm(request.POST or None)

    context = {
        "form":form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    return render(request, "form.html", {})
