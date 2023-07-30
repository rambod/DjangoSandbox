from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {
        'id': 1,
        'name': 'Lets learn python!',
    },
    {
        'id': 2,
        'name': 'Design with me',
    },
    {
        'id': 3,
        'name': 'Frontend development',
    }
]

# Create your views here.
def home(request):
    context = {'rooms': rooms}
    return render(request, 'studybud/home.html',context)

def room(request,pk):
    print(pk)
    room = None
    for i in rooms:
        if i['id'] == pk:
            room = i
            print(f"room is {room}")
    context = {'room': room}
    print(f"conetxt is {context}")
    return render(request, 'studybud/room.html',context)