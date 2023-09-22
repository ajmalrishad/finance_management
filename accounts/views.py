from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists...')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'Success! Signup Completed...')
        return redirect('login')
    
    return render(request, 'signup.html')

@csrf_exempt
def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if username and password are correct
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
    
    return render(request, 'login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


