from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *

def health_check(request):
    return JsonResponse({'status': 'ok'})
