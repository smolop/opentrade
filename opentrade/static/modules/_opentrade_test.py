from _opentrade import OpenTradeActions as OPA

opa = OPA(username='user_test_01')

# ----------------
# Users test functions
# ----------------

sign_up = opa.sign_up(data={})
print(sign_up)

print("-- User Details --")
user_details = opa.get_user_details()
print(user_details)

print("-- User Patch --")
data = {'email': 'user_patch_01@example.com'}
user_patch = opa.user_patch(data)
print(user_patch)


# ----------------
# Shares test unctions
# ----------------

print("-- Get Quote --")
quote = opa.get_quote_info({'symbol': 'IBM'})
print(quote)

print("-- Get Quote History--")
data = {
    'symbol': 'IBM', 
    'interval': 'weekly',
    'start': '2019-06-02',
    'end': '2019-08-28'
    }
quote_history = opa.get_quote_history(data)
print(quote_history)

print("-- Get Quote Price --")
quote_price = opa.get_quote_price({'symbol': 'IBM'})
print(quote_price)

print("-- Buy --")
data = {'symbol': 'IBM', 'quantity': 1}
buy_res = opa.buy(data)
print(buy_res)

print("-- Sell --")
data = {'symbol': 'IBM', 'quantity': 1}
sell_res = opa.sell(data)
print(sell_res)

print("-- Close Order --")
data = {'ref': 51}
close_order = opa.close_order(data)
print(close_order)


# -------------------
# Favorites test funcitons 
# -------------------

print("-- Follow --")
follow_to = opa.follow({'symbol': 'IBM'})
print(follow_to)

print("-- Get Favorites --")
favorites = opa.get_favorites()
print(favorites)

print("-- Unfollow --")
unfollow_to = opa.unfollow({'symbol': 'IBM'})
print(unfollow_to)


# -------------------
# Portfolio test functions 
# -------------------

print("-- Get All Portfolio Info --")
portfolio_info = opa.get_all_portfolio_info()
print(portfolio_info)

print("-- Get Summary --")
summary = opa.get_summary()
print(summary)

print("-- Get Buyings --")
buyings = opa.get_buyings_info()
print(buyings)

print("-- Get Sellings --")
sellings = opa.get_sellings_info()
print(sellings)

print("-- Get Portfolio Value --")
portfolio_value = opa.get_portfolio_value()
print(portfolio_value)


# -------------------
# Wallet test functions
# -------------------

print("-- Get Wallet Amount --")
wallet_amount = opa.get_wallet_amount()
print(wallet_amount)


# --------------------------------
# Schedule operation test funcitons 
# --------------------------------

print("--- Schedule Share Operation ---")
data = {
    'symbol': 'IBM',
    'quantity': 1,
    'min_price': 120,
    'max_price': 140,
    'operation': 's',
    'schedule_start': '2019-10-08 20:00:00'
}
schedule_share_op = opa.schedule_share_operation(data)
print(schedule_share_op)

print("-- Get Schedule Shares Operations --")
shcedules_shares_ops = opa.get_schedule_shares_operations()
print(shcedules_shares_ops)

print("-- Cancel Schedule Share Operation --")
data = {'ref': 78}
cancel_schedule_op = opa.cancel_schedule_share_operation(data)
print(cancel_schedule_op)