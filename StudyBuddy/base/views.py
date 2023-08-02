from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
# rooms = [
#     {
#         'id': 1,
#         'name': 'Learning Vue js'
#     },
#     {
#         'id': 2,
#         'name': 'Learning React js'
#     },
#     {
#         'id': 3,
#         'name': 'Learning Angular js'
#     }
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.add_message(request, messages.ERROR,
                                 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Username or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR,
                                 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'page': page, 'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(
        name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()

    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')[:5]

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,'room_messages':room_messages}
    return render(request, 'base/home.html', context=context)


def userPofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context ={
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
    }
    return render(request, 'base/profile.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participents = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        room.save()
        message.save()
        return redirect('room', pk=room.id)
    print(participents)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participents}

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateMessage(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/message_form.html', context)
