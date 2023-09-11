from django.shortcuts import render
import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

API_KEY = 'bab03115888a4c3f906e61c1ee52ac07'

def home(request):
    context={}
    sorting=request.GET.get('sort') if request.GET.get('sort') else "relevancy"
    category = request.GET.get('category')
    searchkeyword=request.GET.get('searchkeyword')
    if searchkeyword :
        request.session['searchkeyword']=searchkeyword
        url = "https://newsapi.org/v2/everything?q="+request.session['searchkeyword']+"&sortBy="+sorting+"&apiKey="+API_KEY+""
        context['searchkeyword']=request.session['searchkeyword']
    elif category:
        url = "https://newsapi.org/v2/top-headlines?category="+category+"&language=en&sortBy="+sorting+"&apiKey="+API_KEY+""
    else:
        url = "https://newsapi.org/v2/everything?q='technology'&sortBy="+sorting+"&apiKey="+API_KEY+""
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context['articles']=articles
    context['sorting']=sorting
    if searchkeyword:
        context['searchkeyword']= searchkeyword
    if request.user.is_authenticated:
        if searchkeyword :
            usersearch.objects.update_or_create(search=request.user,keywords=searchkeyword,article=articles)
    return render(request, 'news_api/home.html', context)

def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('adminarea')
            else:
                return redirect('home')
        else:
            return render(request, 'news_api/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        return render(request, 'news_api/login.html')
    
@user_passes_test(lambda u: u.is_superuser)
def adminuser(request):
    template = 'news_api/admin.html'
    context={}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                context['usercreatedmessage'] = "User created successfully"
                context['form']=form
                return render(request, 'news_api/admin.html',context)
            
    else:
        form = RegisterForm()
    return render(request, 'news_api/admin.html',{'form': form})

def recentsearch(request):
    context={}
    if request.user.is_authenticated:
        obj=usersearch.objects.filter(search=request.user).values_list('keywords',flat=True)
        context['keyword']=obj
    return render(request, 'news_api/recentsearch.html',context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')

