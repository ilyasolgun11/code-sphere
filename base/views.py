from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, MessageForm, RoomForm
from .models import CustomUser, Topic, Room, RelatedTo, Message

# Create your views here.

def landing_page(request):
    return render(request, 'base/landing_page.html')

@login_required(login_url='login')
def home(request):
    topics = Topic.objects.all()
    related_to = RelatedTo.objects.all()
    recent_messages = Message.objects.all().order_by('-created')[0:7]
    q = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(room_related_to__related_to__icontains=q) |
        Q(name__icontains=q)
    )
    context = {'topics': topics, 'rooms': rooms, 'related_to': related_to, 'recent_messages': recent_messages}
    return render(request, 'base/index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    form = MessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = room
            message.save()
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'form': form, 'participants': participants}
    return render(request, 'base/room.html', context)

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            form.save_m2m()
            return redirect('room', pk=room.id)
    else:
        form = RoomForm()
    return render(request, 'base/create_room.html', {'form': form})

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