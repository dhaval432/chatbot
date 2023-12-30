# chatbot_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Chat
import openai

def ask_openai(message):
    # Use OpenAI API to get a response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.7,
        max_tokens=150,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

def chatbot(request):
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user)

        if request.method == 'POST':
            message = request.POST.get('message')
            response = ask_openai(message)

            chat = Chat(user=request.user, message=message, response=response)
            chat.save()
            return JsonResponse({'message': message, 'response': response})

        return render(request, 'chatbot_app/chatbot.html', {'chats': chats})

  
