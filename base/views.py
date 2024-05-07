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
    """
    Retrieves topics, related items, and recent messages from the database.
    Filters rooms based on the search query and renders the home page
    with the retrieved data.
    """
    topics = Topic.objects.all()
    related_to = RelatedTo.objects.all()
    recent_messages = Message.objects.all().order_by('-created')[0:7]
    q = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(room_related_to__related_to__icontains=q) |
        Q(name__icontains=q)
    ).order_by('-created')
    context = {'topics': topics, 'rooms': rooms, 'related_to': related_to, 'recent_messages': recent_messages}
    return render(request, 'base/index.html', context)

def room(request, pk):
    """
    Retrieves a specific room and its messages.
    Message adding functionality.
    Handles banning participants and posting messages.
    Redirects banned users to the home page.
    """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    form = MessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if 'ban' in request.POST:
            if room.host == request.user:
                participant_id = request.POST.get('participant_id')
                participant = CustomUser.objects.get(id=participant_id)
                room.banned_participants.add(participant)
                room.participants.remove(participant)
                return redirect('room', pk=pk)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = room
            message.save()
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        if 'delete-room' in request.POST:
            room.delete()
            return redirect('home')
        
    if request.user in room.banned_participants.all():
        return redirect('home')
    context = {'room': room, 'room_messages': room_messages, 'form': form, 'participants': participants}
    return render(request, 'base/room.html', context)

def create_room(request):
    """
    Renders the room creation form.
    Handles creating a new room.
    """
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

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        if 'room-delete' in request.POST:
            room.delete()
            return redirect('home')
    return render(request, 'base/delete_room.html')

def register_page(request):
    """
    Renders the user registration form.
    Handles registering a new user.
    """
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
    """
    Renders the login form.
    Handles user login.
    """
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
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'base/login.html')

    return render(request, 'base/login.html')


def logout_page(request):
    """
    Logs out the current user and redirects to the landing page.
    """
    # Logout the user
    logout(request)
    return redirect('landing_page')