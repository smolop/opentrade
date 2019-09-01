from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from opentrade.utils.functions import shares as f_shares

from opentrade.users.models import Profile
from opentrade.assets.models import Favorite

from rest_framework.authtoken.models import Token


import json



@login_required
def share_view(request, symbol):

    quote = get_json_share(symbol)

    user = request.user
    profile = Profile.objects.get(user=user)
    token, created = Token.objects.get_or_create(user=user) 
    context = {
        'asset': quote,
        'profile': profile,
        'token': token 
    }

    return render(request, 'shares/details.html' , context)

@login_required
def favorites_view(request):
    context = get_common_context(request)
    return render(request, 'assets_templates/favorites.html', context)

@login_required
def dev_mode_view(request):
    context = get_common_context(request)
    return render(request, 'dev_mode.html', context)

@login_required
def schedule_ops_view(request):
    context = get_common_context(request)
    return render(request, 'assets_templates/shedule_operations.html', context)

@login_required
def help_view(request):
    context = get_common_context(request)
    return render(request, 'help.html', context)

def get_common_context(request):
    user = request.user
 
    profile = Profile.objects.get(user=user)
    token, created = Token.objects.get_or_create(user=user) 
    context = {
        'profile': profile,
        'token': token 
    }
    return context

def get_json_share(symbol):
    response = f_shares.get_quotes(symbol)
    
    json_response = response.json()
    
    quote = json.loads(
        str(
            json.dumps(
                json_response['quotes']['quote']
            )
        )
    )

    return quote

def get_json_history(symbol):
    response = f_shares.get_history(symbol)

    json_response = response.json()

    history = json.loads(
        str(
            json.dumps(
                json_response['history']
            )
        )
    )
    return history