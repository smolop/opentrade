from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import SafeString
from django.http import JsonResponse, HttpResponse
import http.client
import requests
import json

from opentrade.users.models import Profile, User

from rest_framework.authtoken.models import Token

@login_required
def index(request):
    
    # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes)

    # Headers

    headers = {"Accept":"application/json",
            "Authorization":"Bearer nTk5eX7GH6Zq3TLXQElBopuoTXCY"}

    # Send synchronously

    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': 'AAPL,IBM,MSFT,FB,AMZN,TSLA'},
        headers=headers
    )
    
    json_response = response.json()
    
    print(response.status_code)

    assets=json.loads(
        str(
            json.dumps(
                json_response['quotes']
            )
        )
    )



    # print(assets)
    print("##############################")
    print("##############################")
    # print(assets_history)
    print(request)
    user = User.objects.get(username=request.user, is_active=True)
    print("USER:"+str(user))
    profile = Profile.objects.get(user=user)
    token = token, created = Token.objects.get_or_create(user=user) 
    return render(
        request, 
        'home.html', 
        context={
            'assets':assets,
            'profile': profile,
            'token': token
            },
    )


def get_price(symbol):

    # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes)

    # Headers

    headers = {"Accept":"application/json",
            "Authorization":"Bearer nTk5eX7GH6Zq3TLXQElBopuoTXCY"}

    # Send synchronously

    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': symbol},
        headers=headers
    )

    json_response = response.json()

    asset=json.loads(
        str(
            json.dumps(
                json_response['quotes']['quote']['bid']
            )
        )
    )
    print(asset)
    return asset