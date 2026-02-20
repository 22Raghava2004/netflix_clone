from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render

def index(request):
    return render(request, "index.html")


def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')



@require_POST
def add_to_list(request):
    return JsonResponse({"message": "Added to List"})
