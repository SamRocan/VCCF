from django.shortcuts import render

# Create your views here.
#To view logs: docker logs vccf_web_1
def index(request):
    if(request.method == "POST"):
        print(request.POST.get('search'))
    return render(request, 'main/index.html')