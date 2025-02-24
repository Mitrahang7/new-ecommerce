from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
  products=Product.objects.all()
  categories = Category.objects.all()
  return render(request, 'home.html', {'products':products, 'categories': categories})

def category(request, cat):
   cat= cat.replace('-', ' ').lower()

   try:
      category=Category.objects.get(name__iexact=cat)
      products=Product.objects.filter(category=category)
      categories = Category.objects.all()
      return render(request, 'category.html', {
         'category':category,
         'products': products,
         'categories': categories
      })
  
   except:
       messages.error(request, 'No such category..')
       return redirect('home')
      


def about(request):
  return render(request, 'about.html')


def login_user(request):
  if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request, username=username, password=password)

    if user is not None:
      login(request,user)
      messages.success(request, 'You are successfully logged in.')
      return redirect('home')

    else:
      messages.error(request, 'Sorry, validate again.')

  else:

    return render(request, 'login.html')
  
  

def logout_user(request):
  logout(request)
  messages.success(request, 'You are logged out...')
  return redirect('home')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('register')

      
        user = User.objects.create_user(username=username, password=password1, email=email,
                                        first_name=first_name, last_name=last_name)
        user.save()

        
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')

    return render(request, 'register.html') 


def product_detail(request, pk):
   product=Product.objects.get(id=pk)

   return render(request, 'product_detail.html', {'product':product})

@login_required
def update_info(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get("phone", "")
        profile.address1 = request.POST.get("address1", "")
        profile.address2 = request.POST.get("address2", "")
        profile.disrtict = request.POST.get("city", "")  
        profile.province = request.POST.get("state", "") 
        profile.save()

        messages.success(request, "Your Info Has Been Updated!!")
        
        

    return render(request, "update_info.html", {"profile": profile})