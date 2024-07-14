def get_exchange_rate(current_currency, target_currency):
    currency_data = {
        "$": 1,
        "AZN": 1.7,
        "€": 0.93,
    }
    return currency_data[target_currency] / currency_data[current_currency]


def get_price_currency(price, current_currency, target_currency):

    exchange_rate = get_exchange_rate(current_currency, target_currency)
    # Convert the price to the target currency
    target_price = price * exchange_rate
    return round(target_price, 1)
