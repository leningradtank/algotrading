import random
import threading
import time

actions = ["Buy", "Sell"]
order_size = range(1,10)
symbol = ["ETH", "BTC", "SOL"]
price = range(1000,1200)


def generate_order(actions, order_size, price):

    while True:
        # print("Action", "Order-Size", "Price")
        new_action = random.choice(actions)
        new_order_size = random.choice(order_size)
        new_price = random.choice(price)

        print(new_action, new_order_size, new_price)
        time.sleep(2.0)
        trade_bot()
        time.sleep(2.0)


def trade_bot():

    currentPosition = 0
    currentTreasury = 2000

    # new_order_size = generate_order.new_order_size
    # new_price = generate_order.new_price

    if currentPosition == 0:
        buy = "True"
        # currentPosition = currentPosition + new_order_size
    elif currentPosition > 0:
        if currentTreasury - new_price > 0:
            buy = "True"
            # currentPosition = currentPosition + new_order_size
        else:
            buy = "False"
    else:
        buy = "False"

    print("Current Position is", currentPosition)
    print(buy)
    



generate_order(actions, order_size, price)



