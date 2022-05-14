from django.shortcuts import render,redirect

# Create your views here.
#To view logs: docker logs vccf_web_1
from django.urls import reverse


def index(request):
    return render(request, 'main/index.html')

def product(request):
    print(request.GET["productSearch"])
    return redirect('productHome', productSlug=request.GET["productSearch"])

def productHome(request, productSlug):
    context = {
        'product':productSlug
    }
    return render(request, 'main/productHome.html', context)
