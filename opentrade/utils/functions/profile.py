from opentrade.users.models import Profile
from datetime import date

def calculate_age(born): 
    today = date.today() 
    try:  
        birthdate = born.replace(year = today.year) 
  
    # raised when birth date is February 29 
    # and the current year is not a leap year 
    except ValueError:  
        birthdate = born.replace(year = today.year, 
                  month = born.month + 1, day = 1) 
  
    if birthdate > today: 
        return today.year - born.year - 1
    else: 
        return today.year - born.year 

def has_funds(user_profile, amount):
    wallet_amount = user_profile.wallet.amount
    if wallet_amount >= amount :
        return True
    return False

def buy_balance(user_profile, amount):
    wallet, portfolio = get_wallet_and_portfolio(user_profile)
    wallet.amount -= amount
    portfolio.value += amount


def get_wallet_and_portfolio(user_profile):
    wallet = user_profile.wallet
    portfolio = user_profile.portfolio
    return wallet, portfolio

def payoff_balance(user_profile, amount):
    wallet, portfolio = get_wallet_and_portfolio(user_profile)
    wallet.amount -= amount
    portfolio.value += amount
    return wallet, portfolio

def close_operation(user_profile, amount):
    wallet, portfolio = get_wallet_and_portfolio(user_profile)
    wallet.amount += amount
    portfolio.value -= amount
    return wallet, portfolio

def save(user_profile):
    wallet, portfolio = get_wallet_and_portfolio(user_profile)
    wallet.save()
    portfolio.save()
    return wallet, portfolio