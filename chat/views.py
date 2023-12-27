from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect

# Create your views here.

def index(request): # request is an HttpRequest object
    if request.method == 'POST': # If the form has been submitted as post
        print(request.POST['textmessage']) # print the textmessage
        myChat = Chat.objects.get(id=1) # get the chat with id 1
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user) # create a message with the textmessage, the chat with id 1, the author and the receiver
    chatMessages = Message.objects.filter(chat__id=1) # get the messages with chat id 1
    return render(request, 'chat/index.html', {'messages': chatMessages}) # render the index.html template with the messages

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/chat/')
        else: 
            return render(request, 'auth/login.html', {'wrongPassword': True})
    return render(request, 'auth/login.html')