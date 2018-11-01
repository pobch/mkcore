from django.http import HttpResponse
from django.shortcuts import redirect, render

def index(request):
    return redirect('app')

def app(request):
    return HttpResponse('Makrub Applicaiton')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')
