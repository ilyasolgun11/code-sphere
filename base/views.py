from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm
from .models import CustomUser, Topic, Room, RelatedTo

# Create your views here.

def landing_page(request):
    return render(request, 'base/landing_page.html')

@login_required(login_url='login')
def home(request):
    topics = Topic.objects.all()
    related_to = RelatedTo.objects.all()
    q = ''
    if request.GET.get('q') is not None:
        q = request.GET.get('q')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(room_related_to__related_to__icontains=q) |
        Q(name__icontains=q)
    )
    participants = []
    for room in rooms:
        participants.extend(room.participants.all())
    participant_count = len(participants)
    context = {'topics': topics, 'rooms': rooms, 'related_to': related_to, 'participants': participants, 'participant_count': participant_count}
    return render(request, 'base/index.html', context)

def register_page(request):
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
            # Get the form errors and display them as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

    context = { 'form': form }        
    return render(request, 'base/register.html', context)

def login_page(request):
    # If the request from the view is post
    if request.method == 'POST':
        # Grab the email and password from the request
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # Check if the email passed is in the database
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login.html')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        # Login the user or throw error
        if user is not None:
            login(request, user)
            redirect('home')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'base/login.html')

    return render(request, 'base/login.html')


def logout_page(request):
    # Logout the user
    logout(request)
    return redirect('landing_page')