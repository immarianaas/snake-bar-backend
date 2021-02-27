from gametest.models import Message
from django.shortcuts import render

# Create your views here.

def message(request):
    messages = Message.objects.all()
    print(messages)
    return render(request, 'msgs.html', {'messages':messages})