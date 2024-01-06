from bitkub import Bitkub
import numpy as np
import datetime
import time
import pandas as pd


API_KEY = ''
API_SECRET = ''

bitkub = Bitkub()
bitkub.set_api_key(API_KEY)
bitkub.set_api_secret(API_SECRET)

percentage_trade = 0.001
amt = 15
symbol = "THB_BTC"
SYMBOL = "BTC_THB"

percentage = np.round(percentage_trade*100,2)#เลข2หมายถึงทศนิยมสองตำแหน่ง


def run():

    def get_price():
        get_price = bitkub.ticker(sym=symbol)
        get_price = get_price[symbol]['last']
        get_price = float(get_price)
        return get_price

    def last_open_order():
        open_order = bitkub.my_open_history(sym=symbol)
        open_order = open_order['result'][0]['rate']
        open_order = float(open_order)
        return open_order

    #def amount_sell():
        #order = bitkub.my_open_history(sym=symbol)
        #rate_order = float(order['result'][0]['rate'])
        #amount_order = float(order['result'][0]['amount'])
        #amount_sell = amount_order/rate_order
        #amount_sell = '{:.9f}'.format(amount_sell)
        #return amount_sell

    get_price = get_price()
    last_open_order = last_open_order()
    #amount_sell = amount_sell()

    sell_price = (last_open_order*percentage_trade)+last_open_order
    sell_price = "{:.2f}".format(sell_price)
    sell_price = float(sell_price)

    buy_price = last_open_order - (last_open_order*percentage_trade)
    buy_price = "{:.2f}".format(buy_price)
    buy_price = float(buy_price)


    print("[{}] Local time" .format(datetime.datetime.now()))
    print(f"Price market at : {get_price}")
    print(f"Last order_open : {last_open_order}")
    print(f"percent : {percentage}% and price sell at: {sell_price}")
    print(f"percent : {percentage}% and price buy at: {buy_price}")

    if get_price <= buy_price:
        buy_price = bitkub.place_bid(sym=SYMBOL,amt=float(amt),typ='market')
        print(f"Buy order:{buy_price}")
    elif get_price >= sell_price:
        order = bitkub.my_open_history(sym=symbol)
        rate_order = float(order['result'][0]['rate'])
        amount_order = float(order['result'][0]['amount'])
        if amount_order <=1:
            amount_sell = amt/get_price
            amount_sell = '{:.9f}'.format(amount_sell)
            print(f"amount_sell: {amount_sell}")
            sell_price = bitkub.place_ask(sym=SYMBOL,amt =float(amount_sell),typ='market')
        elif amount_order == amt:
            amount_buy = amount_order/rate_order
            amount_buy = '{:.9f}'.format(amount_buy)
            print(f"amount_buy:{amount_buy}")
            sell_price = bitkub.place_ask(sym=SYMBOL,amt =float(amount_buy),typ='market')


while True:
    try:
        run()
    except Exception as e:
        print("Error")
    time.sleep(10)
