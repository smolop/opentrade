from _opentrade import OpenTradeActions as OPA

opa = OPA(username='user_test_06')

# print("-- Get Quote --")
# quote = opa.get_quote_info({'symbol': 'IBM'})
# print(quote)

# print("-- Buy --")
# data = {'symbol': 'IBM', 'quantity': 1}
# buy_res = opa.buy(data)
# print(buy_res)

# print("-- Sell --")
# data = {'symbol': 'IBM', 'quantity': 1}
# sell_res = opa.sell(data)
# print(sell_res)

# print("-- Get All Portfolio Info --")
# portfolio_info = opa.get_all_portfolio_info()
# print(portfolio_info)

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



