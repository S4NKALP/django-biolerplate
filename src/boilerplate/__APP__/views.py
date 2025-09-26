from django.http import HttpResponse
from django.views import generic

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

def home(request):
    return HttpResponse("Welcome to {{ project_name }} / {{ app_name }}!")
