import public_client as puc
import time as t


# create instance of FTXPublicClient and FTXPrivateClient

public_client = puc.FTXPublicClient()
# private_client = puc.FTXPublicClient(api_key, api_secret) # insert api_key and api_secret

# create btc_future variable and print result

btc_future = public_client.get_future("BTC-PERP")
print(f"BTC-PERP (perpetual futures) market data:\n{btc_future}\n")

# create btc_history variable and print result

btc_history = public_client.get_market_history("BTC-PERP", 60, (t.time() - 60000), t.time())
print(f"BTC-PERP (perpetual futures) market history (One minute chart data):\n{btc_history}\n")
