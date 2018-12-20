import requests
import time
from datetime import datetime


BITCOIN_API_URL = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
IFTTT_WEBHOOKS_URL = "https://maker.ifttt.com/trigger/test_event/with/key/nCj28vvxKM651WKfyzU2rfDSiWu214W6i-b7uJujpxe"
BITCOIN_PRICE_THRESHOLD = 10000


def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # Converts a rate to floating point number.
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    data = {'value1': value}
    # Insert desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sending an HTTP POST request to a URL webhook
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Date string format '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({
            'date': date,
            'price': price
        })

        # Sending urgent notice
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Sending Telegram notification
        # After receiving 5 objects in bitcoin_history - send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update',
                               format_bitcoin_history(bitcoin_history))
            # Reset history
            bitcoin_history = []

        # Sleep for 30 minutes
        time.sleep(30 * 60)


if __name__ == '__main__':
    main()
