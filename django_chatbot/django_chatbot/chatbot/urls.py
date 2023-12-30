from django.urls import path
# from .views import register
# from .views import login

from . import views
urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    # path('login/', login, name='login'),
    # path('register/', register, name='register'),
   
]