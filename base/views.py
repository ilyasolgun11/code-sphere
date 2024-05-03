from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from .models import CustomUser

# Create your views here.

def landing_page(request):
    return render(request, 'base/landing_page.html')

def register(request):
    # Initialise user creation form
    form = MyUserCreationForm()

    # If the request from the view is post
    if request.method == "POST":
        # use the requests data to create the user
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Redirect user to login page when user is registered
            return redirect('login')
        else:
            # Throw error when there is an error
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}        
    return render(request, 'base/register.html', context)

def login_page(request):
    # If the request from the view is post
    if request.method == 'POST':
        # Use the data passed from the view to get the email and password
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        # See if the email being used is in the database or not
        try:
            user = CustomUser.objects.get(email=email)
        except:
            # If it is not then throw an error
            messages.error(request, 'User does not exist')
        # Authenticate the user 
        user = authenticate(request, email=email, password=password)
        # Login the user
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'base/login.html')


def logout_user(request):
    # Logout the user
    logout(request)
    return redirect('landing_page')