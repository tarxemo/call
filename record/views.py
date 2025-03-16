from django.shortcuts import render
from .models import CustomUser

# Create your views here.
def call(request):
    return render(request, "record.html")

from django.shortcuts import render

def call_page(request):
    users = CustomUser.objects.exclude(id=request.user.id)  # Exclude the current user
    return render(request, "call.html", {"users": users})
