from django.shortcuts import render

# Create your views here.
rooms = [
    {
        'id': 1,
        'name': 'Learning Vue js'
    },
    {
        'id': 2,
        'name': 'Learning React js'
    },
    {
        'id': 3,
        'name': 'Learning Angular js'
    }
]


def home(request):
    context = { 'rooms': rooms }
    return render(request,'base/home.html',context=context)

def room(request,pk):
    room = None
    for i in rooms:
        if i['id'] == pk:
            room = i
    context = { 'room' : room}
            
    return render(request,'base/room.html',context)
