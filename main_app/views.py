from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Cat, CatToy

# Create your views here.
# NOTE TO SELF THESE ARE CONTROLLERS

############# CATS ################

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = '/cats'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect("/cats")

class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect("/cats/" + str(self.object.pk))

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats })

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/show.html', {'cat': cat })

############# CATTOYS ################
def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', { 'toys': cattoys} )

def cattoys_show(request, cattoy_id):
    toy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', {'toy': toy })

class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'

class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']
    success_url = '/cattoys'

class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'



############# USERS ################
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})