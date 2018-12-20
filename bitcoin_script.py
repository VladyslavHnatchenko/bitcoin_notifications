import requests


bitcoin_api_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
response = requests.get(bitcoin_api_url)
response_json = response.json()

print(type(response_json))

print(response_json[0])

# url_webhooks = 'https://maker.ifttt.com/trigger/test_event/with/key/nCj28vvxKM651WKfyzU2rfDSiWu214W6i-b7uJujpxe'
