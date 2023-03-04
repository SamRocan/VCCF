from django.shortcuts import render

# Create your views here.
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from main.models import Favourite

def register(request):
    error_list = []
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('index')
        else:
            users = get_user_model().objects.values_list('username', flat=True).distinct()
            if request.POST.get('username', False) in users:
                error_list.append("Username aleady taken")
            emails = get_user_model().objects.values_list('email', flat=True).distinct()
            if request.POST.get('email', False).lower() in emails:
                error_list.append("email aleady taken")
            if(request.POST.get('password1', False)) != request.POST.get('password2', False):
                error_list.append("passwords must match")
            else:
                error_list.append("passwords does not meet requirement, please ....")
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    print(error_list)
    return render (request, template_name="registration/register.html", context={"register_form":form, "error_list":error_list})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            login(request, user)
            return redirect('profile')
        users = get_user_model().objects.values_list('username', flat=True).distinct()
        if(username in users):
            error_message=  'Username or password incorrect. Please try again'
        else:
            error_message = 'Account not found, please check your credentials'
        context = {'error': error_message}    
        return render (request, template_name="registration/login.html", context=context)
    context = {'error':None}
    return render (request, template_name="registration/login.html", context=context)


def profile(request):
    favourites = Favourite.objects.filter(user=request.user)
    context = {
        'favourites':favourites
    }
    return render(request, "accounts/profile.html", context)