from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import SafeString
from django.http import JsonResponse, HttpResponse
import http.client

from datetime import timedelta, date
from django.utils import timezone
import requests
import json


def get_quotes(symbol):
    # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes)

    # Headers

    headers = {"Accept":"application/json",
            "Authorization":"Bearer nTk5eX7GH6Zq3TLXQElBopuoTXCY"}

    # Send synchronously

    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': symbol},
        headers=headers
    )

    return response

def get_price(symbol):

    response = get_quotes(symbol)

    json_response = response.json()

    asset=json.loads(
        str(
            json.dumps(
                json_response['quotes']['quote']['last']
            )
        )
    )
    return asset

def get_chage_percentage(symbol):

    response = get_quotes(symbol)

    json_response = response.json()

    asset=json.loads(
        str(
            json.dumps(
                json_response['quotes']['quote']['change_percentage']
            )
        )
    )
    return asset

def exists(symbol):
    response = get_quotes(symbol)
    if response.status_code == 200:
        return True
    return False


def get_history(
                symbol, 
                interval='daily', 
                start=date.today().replace(month=date.today().month-1).isoformat(), 
                end=date.today().isoformat()
                ):
    # Request: Market History (https://sandbox.tradier.com/v1/markets/history)

    # Headers

    headers = {"Accept":"application/json",
            "Authorization":"Bearer nTk5eX7GH6Zq3TLXQElBopuoTXCY"}

    # Send synchronously

    response = requests.get('https://sandbox.tradier.com/v1/markets/history',
    params={'symbol': symbol, 'interval': interval, 'start': start, 'end': end},
    headers=headers
    )

    return response

def get_json_share(symbol):
    response = get_quotes(symbol)
    
    json_response = response.json()
    
    quote = json.loads(
        str(
            json.dumps(
                json_response['quotes']['quote']
            )
        )
    )

    return quote

def get_json_history(response):
    response = response

    json_response = response.json()

    history = json.loads(
        str(
            json.dumps(
                json_response['history']
            )
        )
    )
    return history

## Chart functions ##
def get_dates_to_chart(symbol):
    response = get_history(symbol)
    json_history = get_json_history(response)
    history = json_history['day']

    dates = []
    closed_prices = []
    for e in history:
        dates.append(e['date'])
        closed_prices.append(e['close'])
    print(dates)
    print(closed_prices)
    return dates, closed_prices
    