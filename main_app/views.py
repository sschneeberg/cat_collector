from django.shortcuts import render

# Create your views here.
# NOTE TO SELF THESE ARE CONTROLLERS

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')