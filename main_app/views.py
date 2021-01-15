from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Cat, CatToy

# Create your views here.
# NOTE TO SELF THESE ARE CONTROLLERS

############# USERS ################
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})

def login_view(request):
    #if post then auhtenticate user
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid(): 
            u = form.cleaned_data['username']
            p = form.cleaned_data['password'] #.get('key') also works
            user = authenticate(username=u, password=p)
            # check if user in db and if active
            if user is not None:
                if user.is_active: 
                    login(request, user)
                    return HttpResponseRedirect('/user/' + u)
                else: return HttpResponseRedirect('/login')
            else: return HttpResponseRedirect('/login')
    else: # not a post request
        form = AuthenticationForm()
        return render(request, 'login.html', { 'form': form })


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
    fields = ['name', 'breed', 'description', 'age', 'cattoys']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(form.instance.cattoys)
        # self.object.cattoys.appen(form.instance.cattoy)
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
