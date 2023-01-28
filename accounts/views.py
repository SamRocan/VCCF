from django.shortcuts import render

# Create your views here.
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from main.models import Favourite

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request, template_name="registration/register.html", context={"register_form":form})

def profile(request):
    favourites = Favourite.objects.filter(user=request.user)
    context = {
        'favourites':favourites
    }
    return render(request, "accounts/profile.html", context)