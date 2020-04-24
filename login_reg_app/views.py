from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt


# Create your views here.

def register_login(request):
    return render(request, 'register_login.html')

def render_success(request):
    if 'loggedinId' not in request.session:
        return redirect('/')
    
    context = {
        "loggedinUser": User.objects.get(id = request.session['loggedinId'])
    }
    return render(request, "success.html", context)

def register_user(request):
    request.POST
    errorsFromValidator = User.objects.userValidator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value, extra_tags= "register")
        return redirect("/")

    password = request.POST['reg_pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print("password hash below")
    print(pw_hash)
    newUser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['reg_email'], birthday = request.POST['bday'], password = pw_hash, confirm_password = pw_hash)
    print(request.POST)
    print(newUser)
    request.session['loggedinId'] = newUser.id
    messages.success(request,"Successfully registered!")
    return redirect('/success')


def user_login(request):
    request.POST
    errorsFromValidator = User.objects.loginValidator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value, extra_tags= "login")
        return redirect("/")

    user = User.objects.get(email = request.POST['login_email'])
    request.session['loggedinId'] = user.id
    print('Login Successful')
    messages.success(request, "Successfully logged in!")
    return redirect ('/success')


def logout(request):
    request.session.clear()
    return redirect('/')