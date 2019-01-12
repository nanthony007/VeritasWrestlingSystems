from django.shortcuts import render

def index(request):
    return render(request, 'vws_main/home.html')

def contact(request):
    return render(request, 'vws_main/contact.html', {'content':['If you would like to contact me please email me at:', 'nanthony007@gmail.com']})
