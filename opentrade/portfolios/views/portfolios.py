from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
import requests
import json

from opentrade.users.models import Profile, User

from rest_framework.authtoken.models import Token

@login_required
def portfolio(request):
    user = User.objects.get(username=request.user, is_active=True)
    profile = Profile.objects.get(user=user)
    token = token, created = Token.objects.get_or_create(user=user) 
    return render(
        request, 
        'portfolio/my_portfolio.html', 
        context={
            'profile': profile,
            'token': token
            },
    )

@login_required
def summary(request):
    user = User.objects.get(username=request.user, is_active=True)
    profile = Profile.objects.get(user=user)
    token = token, created = Token.objects.get_or_create(user=user) 
    return render(
        request, 
        'portfolio/my_summary.html', 
        context={
            'profile': profile,
            'token': token
            },
    )
