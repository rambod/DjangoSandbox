from django.shortcuts import render

def frontPage(request):
    return render(request, 'core/base.html')
