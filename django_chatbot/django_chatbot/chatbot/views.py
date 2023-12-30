from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from chatbot.models import Chat

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist



def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    if request.user.is_authenticated:
        try:
            chats = Chat.objects.filter(user=request.user)
        except ObjectDoesNotExist:
            # Handle the case when no Chat object is found for the given user
            chats = None

        if request.method == 'POST':
            message = request.POST.get('message')
            response = ask_openai(message)

            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        return render(request, 'chatbot.html', {'chats': chats})

    else:
         
        return redirect('login')  

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('chatbot')
#         else:
#             error_message = 'Invalid username or password'
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
    
#         return render(request, 'login.html')


# def logout_page(request):
#     logout(request, )
#     return redirect('login.html')

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('login')
#         else:
#             messages.error(request, 'Error in registration. Please check the form.')

#     else:
#         form = UserCreationForm()
        
#     return render(request, 'register.html', {'form': form})


