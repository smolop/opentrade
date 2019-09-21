#!/usr/bin/env python3
print("Start startegy...")
from _opentrade import OpenTradeActions as OPA
import time

opa = OPA(username='opentrade')

def run_strategy(username, symbol):
    print("SYMBOL: " + symbol)
    quantity = 20
    wallet_amount = opa.get_wallet_amount()
    #ops.buy_shares(username, symbol, quantity*2)
    data = {'symbol': symbol}
    price = opa.get_quote_price(data)
    print("wallet amount is gte to 0 -> wallet amount: " + str(wallet_amount))
    if wallet_amount >= 0:
        #if price >= (price + (price *0.00005)):
        if price > opa.get_quote_price(data):
            buy(username, symbol, quantity)
    #if price <= (price + (price *0.00005)):
    if price < ops.get_price(symbol):
        sell(username, symbol, quantity)
    print("---------------------------------")
    print("Start : %s" % time.ctime())
    time.sleep( 5 )
    ops.get_price('AAPL')
    print("End : %s" % time.ctime())
    print("---------------------------------")

def buy(symbol, quantity):
    print("buy shares")
    ops.buy_shares(username, symbol, quantity)
    print("wallet amount: " + str(ops.get_wallet_amount(username=username)))

def sell(username, symbol, quantity):
    print("sell shares")
    ops.sell_shares(username, symbol, quantity)
    print("wallet amount: " + str(ops.get_wallet_amount(username=username)))

username = 'opentrade'
# for i in range(3):
#     print('···ITERATION Nro:' + str(i) )
#     run_strategy('user_test_00', 'AAPL')

while ops.get_wallet_amount(username) <= 41000:
    run_strategy(username, 'AAPL')
    run_strategy(username, 'MSFT')
    run_strategy(username, 'TEF')
    run_strategy(username, 'IBM')
    if ops.get_wallet_amount(username) <= 31000:
        while ops.exists_shares(username):
            sell(username, 'AAPL', 100)
            sell(username, 'MSFT', 100)
            sell(username, 'TEF', 100)
            sell(username, 'IBM', 100)
        break

# for i in range(3):
#     buy(username, 'MSFT', 30)
#     buy(username, 'AAPL', 20)
#     buy(username, 'AAPL', 20)
#     print("---------------------------------")
#     print("Start : %s" % time.ctime())
#     ops.get_price('AAPL')
#     print("End : %s" % time.ctime())
#     print("---------------------------------")
#     sell(username, 'AAPL', 10)
#     sell(username, 'AAPL', 40)
#     sell(username, 'MSFT', 50)