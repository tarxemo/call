from django.urls import path
from .views import *

urlpatterns =  [
    path('', call, name='call'),
    path("call/", call_page, name="call_page"),
]