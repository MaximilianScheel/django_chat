from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

@login_required(login_url='/login/')
def index(request): # request is an HttpRequest object
    if request.method == 'POST': # If the form has been submitted as post
        print(request.POST['textmessage']) # print the textmessage
        myChat = Chat.objects.get(id=1) # get the chat with id 1
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user) # create a message with the textmessage, the chat with id 1, the author and the receiver
        serialized_obj = serializers.serialize('json', [ new_message, ]) # serialize the message
        return JsonResponse(serialized_obj[1:-1], safe=False) # return a json response with success true
    chatMessages = Message.objects.filter(chat__id=1) # get the messages with chat id 1
    return render(request, 'chat/index.html', {'messages': chatMessages}) # render the index.html template with the messages



def login_view(request):
    redirect = request.GET.get('next', '/chat') # get the next parameter from the url
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else: 
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})


def register_view(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                login(request, user)
                return HttpResponseRedirect('/login')
            except:
                return render(request, 'auth/register.html', {'error': 'Username already exists'})
        else:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})
    return render(request, 'auth/register.html')



def logout_view(request):
    logout(request)
    return redirect('login')