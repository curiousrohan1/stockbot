import csv
import math
import sys


def should_buy_after_consecutive_growth(seen):
    # Buy if the last buy_threshold consecutive changes are "effectively" positive.
    # "Effectively" means that we treat changes between +-epsilon as 0%.

    positive_count = 0
    for evt in reversed(seen):
        change = evt[2]
        if change < epsilon and change > -epsilon:
            continue
        if change > 0.0:
            positive_count += 1
        else:
            # Change is negative
            break
    return positive_count >= buy_threshold


def should_sell_after_loss_limit(seen, buy_price):
    # Sell if we've had a big loss.
    change = (seen[-1][1] - buy_price) / buy_price
    if change <= -loss_limit / 100.0:
        print("    Hit loss limit!!!")
        return True


def should_sell_after_gain_limit(seen, buy_price):
    # Sell if we've had a gain of at least gain_limit percent.
    change = (seen[-1][1] - buy_price) / buy_price
    if change >= gain_limit / 100.0:
        print("    Hit gain limit!!!")
        return True


def should_sell_at_eod(seen, buy_price):
    # Sell if it's 3:30pm
    if sell_eod and '15:30:00-04:00' in seen[-1][0]:
        print("    EOD sale!!!")
        return True

def should_sell_after_consecutive_loss(seen, buy_price):
    # Sell if the last three consecutive changes are "effectively" negative.
    # "Effectively" means that we treat changes between +-epsilon as 0%.

    negative_count = 0
    for evt in reversed(seen):
        change = evt[2]
        if change < epsilon and change > -epsilon:
            continue
        if change < 0.0:
            negative_count += 1
        else:
            # Change is positive
            break
    return negative_count >= sell_threshold


def growth(buy_price, sell_price):
    return (sell_price - buy_price) / buy_price

# Changes from one minue to the next can be tiny. We don't want to treat super-small
# changes as significant. epsilon sets our tolerance: change between last price
# and current price (fractional) must be greater than epsilon and less than -epsilon
# to count as a real change.
epsilon=0.0004

# We must see buy_threshold consecutive significant price increases to trigger a buy
buy_threshold = 2

# We must see sell_threshold consecutive significant price decreases to trigger a sell
sell_threshold = 2

# Set the max loss percentage
loss_limit = 10.0

# Initial cash at the begining of time.
initial_cash = 2000.0

# Do we sell at the end of each day
sell_eod = False

# Set the max gain percentage
gain_limit = 1.0

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <file>')
    sys.exit(1)

seen = []
buy = None
cash = initial_cash
symbol = 'ABCD'
taxable_profit = 0.0
with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        new_price = float(row[1])
        change = growth(seen[-1][1], new_price) if len(seen) > 0 else 0.0
        seen.append((row[0], new_price, change))
        if not buy and should_buy_after_consecutive_growth(seen):
            num_shares = math.floor(cash / new_price)
            cost = num_shares * new_price
            cash -= cost
            print(f'Buying: {num_shares} of {symbol} at {new_price} on {row[0]} for ${cost}. Cash=${cash}')
            buy = (num_shares, new_price)
        elif buy and (
                should_sell_after_loss_limit(seen, buy[1]) or
                should_sell_at_eod(seen, buy[1]) or
                should_sell_after_gain_limit(seen, buy[1])):
#                should_sell_after_consecutive_loss(seen, buy[1])):
            change = growth(buy[1], new_price)
            proceeds = buy[0] * new_price
            cash += proceeds
            profit = proceeds - buy[0] * buy[1]
            if profit > 0:
                taxable_profit += profit
            print(f'Selling: {buy[0]} of {symbol} at {new_price} on {row[0]} for ${proceeds}. Cash=${cash}  Gain={change * 100.0:.2f}%')
            buy = None

if buy:
    print("Dropping last buy")
    cash += buy[0] * buy[1]

profit = cash - initial_cash
taxes = taxable_profit / 4.0
net_profit = profit - taxes
print(f'Initial cash:     ${initial_cash:.2f}')
print(f'Final cash:       ${cash:.2f}')
print(f'Profit:           ${profit:.2f}')
print(f'Taxable Profit:   ${taxable_profit:.2f}')
print(f'Taxes Due:        ${taxes:.2f}')
print(f'Net Profit:       ${net_profit:.2f}')
print(f'Overall growth:   {100.0 * net_profit / initial_cash:.2f}%')
print(f'Change in period: {100.0 * growth(seen[0][1], seen[-1][1]):.2f}%')
