from datetime import datetime, timedelta
from urllib import response
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import PasswordInput, ValidationError
from django.shortcuts import render
from .models import *
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import auth
from shop.forms import SignupForm, LoginForm
import time
# Create your views here.

class BaseView(View):
    views = {}
    views['category'] = Category.objects.filter(status='active')
    views['brands'] = Brand.objects.filter(status='active')
    views['hots'] = Item.objects.filter(status = 'active',label = 'hot')


class HomeView(BaseView):
    def get(self,request):
        self.views['category'] = Category.objects.filter(status = 'active')
        self.views['sliders'] = Slider.objects.filter(status = 'active')
        self.views['ads'] = Ad.objects.filter(status = 'active')
        self.views['news'] = Item.objects.filter(status = 'active',label = 'new')
        self.views['reviews'] = Review.objects.filter(status = 'active')

        return render(request, 'index.html',self.views)

class CategoryView(BaseView):
    def get(self,request,slug):
        category_id = Category.objects.get(slug = slug).id
        self.views['cat_items'] = Item.objects.filter(category = category_id)

        return render(request,'category.html',self.views)

class BrandView(BaseView):
    def get(self,request,name):
        brand_id = Brand.objects.get(name = name).id
        self.views['brand_items'] = Item.objects.filter(brand = brand_id)

        return render(request,'brand.html',self.views)



class ItemSearchView(BaseView):
    def get(self,request):
        search = request.GET.get('search', None)
        if search is None:
            return redirect('/')
        else:
            self.views['search_item'] = Item.objects.filter(name__icontains = search)
            return render(request,'search.html', self.views)


class ItemDetailView(BaseView):
    def get(self,request,slug):
        self.views['item_detail'] = Item.objects.filter(slug = slug)

        return render(request, 'product-detail.html', self.views)

# def signup(request):
#     if request.method == "POST":
#         # if request.methood == "POST" is_valid:
#         f_name = request.POST['first_name']
#         l_name = request.POST['last_name']
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         cpassword = request.POST['cpassword']
        
        
        # a = f_name or l_name.isNumeric()
        # if a:
        #     messages.error(request,"Tero name integer ho voosidike")


        # if f_name or l_name or email or username or password or cpassword == "":
        #     messages.error(request,"All fiend are required")
        #     return redirect('shop:signup')
        # if password == cpassword:

        #     if User.objects.filter(username = username).exists():
        #         messages.error(request,'This username is already taken')
        #         return redirect('shop:signup')

        #     elif User.objects.filter(email = email).exists():
        #         messages.error(request,'This email is already taken')
        #         return redirect('shop:signup')
        #     else:
        #         user = User.objects.create_user(
        #             username = username,
                #     email = email,
                #     password = password,
                #     first_name = f_name,
                #     last_name = l_name,
                # )
                # user.save()
                # # user = request.user.username
                # messages.success(request, f'You are successfully registered {f_name.upper()} {l_name.upper()}')
                # # alert("you are register")
                # return redirect('shop:signup')

    #     else:
    #         messages.error(request,'The password does not match')
    #         return redirect('shop:signup')

    # return render(request,'signup.html')

def login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request = request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            pw = fm.cleaned_data['password']
            user = auth.authenticate(username = username, password = pw)
            if user is not None:
                auth.login(request,user)
                return redirect('shop:profile')
            else:
                messages.error(request,"Your are not registered")
                # return redirect('shop:login')
    else:
        fm = AuthenticationForm()
    return render(request,'login.html', {'form':fm})
    # if request.method == 'POST':
    #     username = fm.request.POST['username']
    #     password = fm.request.POST['password']

    #     user = auth.authenticate(username = username,password = password)
    #     if user is not None:
    #         auth.login(request,user)
    #         return redirect('shop:profile')
    #     else:
    #         messages.error(request,'wrong username or password')
    #         return redirect('shop:login')
    # else:

    # return render(request,'login.html', {'form':fm})

def profile(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('shop:signup')
   


def setcookie(request):
    username = request.user.username
    response = render(request, 'index.html')
    response.set_cookie('name','username')
    return response


def setsessions(request):
    request.session['f_name'] = 'Sunil'
    request.session['l-name'] = 'Nepali'
    # request.session.set_expirey(600)
    return render(request,'index.html')

def delsession(request):
    request.session.flush()
    request.session.clear_expired()
    return render(request,'index.html')

def signup(request):
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            # username = fm.cleaned_data['username']
            # f_name = fm.cleaned_data['first_name']
            # l_name = fm.cleaned_data['last_name']
            # email = fm.cleaned_data['email']
            # pass1= fm.cleaned_data['password1']
            # pass2= fm.cleaned_data['password2'] 
            
            # reg = User(
            # username = username,
            # first_name = f_name, 
            # last_name = l_name,
            # email = email, 
            # password = pass1,
            # )
            # reg.save() 
            fm = SignupForm()
                # user = request.user.username
            messages.success(request, f'You are Registered Successfully ')
            return redirect('shop:login')
    
    else:
        fm = SignupForm()
    return render(request, 'signup.html',{'form':fm})

def logout(request):
    auth.logout(request)
    return redirect('/')





# ------------------------------API-----------------------------------

# from django.urls import path, include
# from django.contrib.auth.models import User
# from rest_framework import routers, serializers, viewsets
# from .models import *
# from .serializers import *
# # ViewSets define the view behavior.
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer



