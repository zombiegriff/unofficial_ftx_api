import time
import hmac
import json
from requests import Request, Session, Response


class FTXPrivateClient(object):
    def __init__(self, api_key = None, api_secret = None, subaccount = None):
        self.session = Session()
        self.url = 'https://ftx.com'
        self.api_key = api_key
        self.api_secret = api_secret
        self.subaccount = subaccount

    def authorise(self, request):
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f"{ts}{prepared.method}{prepared.path_url}".encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self.api_secret.encode(), signature_payload,
        'sha256').hexdigest()
        request.headers['FTX-KEY'] = self.api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self.subaccount is not None:
            request.headers['FTX-SUBACCOUNT'] = self.subaccount

    def private_get_request(self, query):
        endpoint = self.url + query
        request = Request('GET', endpoint)
        self.authorise(request)
        return self.session.send(request.prepare())

    def post_request(self, query, data):
        endpoint = self.url + query
        request = Request('POST', endpoint, json=data)
        self.authorise(request)
        return self.session.send(request.prepare())

    def delete_request(self, query, data):
        endpoint = self.url + query
        request = Request('DELETE', endpoint, json=data)
        self.authorise(request)
        return self.session.send(request.prepare())

    def private_response_status(self):
        query = '/api/'
        response = self.private_get_request(query)
        return response.status_code

    def get_account_info(self):
        query = '/api/account'
        response = self.private_get_request(query)
        return response.json()


    def get_postitions(self, show_avg_price = True):
        query = f'/api/positions?showAvgPrice={show_avg_price}'
        response = self.private_get_request(query)
        return response.json()

    def get_balances(self):
        query = '/api/wallet/balances'
        response = self.private_get_request(query)
        return response.json()

    def get_open_orders(self, pair):
        query = f'/api/orders?market={pair}'
        response = self.private_get_request(query)
        return response.json()

    def get_order_history(self, pair, start_time = None, end_time = None):
        if start_time is None or end_time is None:
            query = f'/api/orders?market={pair}'
            response = self.private_get_request(query)
        else:
            query = f'/api/orders?market={pair}&start_time={start_time}&end_time={end_time}'
            response = self.private_get_request(query)
        return response.json()

    def get_open_conditional_orders(self, pair, order_type = None):
        if order_type is None:
            query = f'/api/conditional_orders?market={pair}'
            response = self.private_get_request(query)
        else:
            query = f'/api/conditional_orders?market={pair}&type={order_type}'
            response = self.private_get_request(query)
        return response.json()

    def get_conditional_order_history(self, pair):
        query = f'/api/conditional_orders/history?market={pair}'
        response = self.private_get_request(query)
        return response.json()


    def place_order(self, pair, side, size, type = 'market', limit_price = None,
    reduce_only = False, client_id = None):
        query = '/api/orders'
        data = {
        'market': pair,
        'side': side,
        'price': limit_price,
        'type': type,
        'size': size,
        'reduceOnly': reduce_only,
        'ioc': False,
        'postOnly': False,
        'clientId': client_id
        }
        response = self.post_request(query, data)
        return response.json()

    def place_stop_order(self, pair, side, trigger_price, size,
    limit_price = None, reduce_only = False, retry = False):
        query = '/api/orders'
        data = {
        'market': pair,
        'side': side,
        'triggerPrice': trigger_price,
        'orderPrice': limit_price,
        'size': size,
        'type': 'stop',
        'reduceOnly': reduce_only,
        'retryUntilFilled': retry
        }
        response = self.post_request(query, data)
        return response.json()

    def place_trailing_stop_order(self, pair, side, trail_value, size,
    reduce_only = False, retry = False):
        query = '/api/orders'
        data = {
        'market': pair,
        'side': side,
        'trailValue': trail_value,
        'size': size,
        'type': 'trailingStop',
        'reduceOnly': reduce_only,
        'retryUntilFilled': retry
        }
        response = self.post_request(query, data)
        return response.json()

    def place_take_profit_order(self, pair, side, trigger_price, size,
    limit_price = None, reduce_only = False, retry = False):
        query = '/api/orders'
        data = {
        'market': pair,
        'side': side,
        'triggerPrice': trigger_price,
        'orderPrice': limit_price,
        'size': size,
        'type': 'takeProfit',
        'reduceOnly': reduce_only,
        'retryUntilFilled': retry
        }
        response = self.post_request(query, data)
        return response.json()

    def modify_order_ftx_id(self, order_id, size = None, price = None,
    client_id = None):
        query = f'/api/orders/{order_id}/modify'
        data = {
        "size": size,
        "price": price,
        "clientId": client_id
        }
        response = self.post_request(query, data)
        return response.json()

    def modify_order_client_id(self, client_id, size, price):
        query = f'/api/orders/by_client_id/{client_id}/modify'
        data = {
        "size": size,
        "price": price,
        "clientId": client_id
        }
        response = self.post_request(query, data)
        return response.json()

    def modify_stop_order(self, order_id, trigger_price, size,
    limit_price = None):
        query = f'/api/conditional_orders/{order_id}/modify'
        data = {
        "triggerPrice": trigger_price,
        "size": size,
        "orderPrice": limit_price
        }
        response = self.post_request(query, data)
        return response.json()

    def modify_trailing_stop_order(self, order_id, trail_value, size):
        query = f'/api/conditional_orders/{order_id}/modify'
        data = {
        "trailValue": trail_value,
        "size": size
        }
        response = self.post_request(query, data)
        return response.json()

    def modify_take_profit_order(self, order_id, trigger_price, size,
    limit_price = None):
        query = f'/api/conditional_orders/{order_id}/modify'
        data = {
        "triggerPrice": trigger_price,
        "size": size,
        "orderPrice": limit_price
        }
        response = self.post_request(query, data)
        return response.json()

    def cancel_order_ftx_id(self, order_id):
        query = f'/api/orders/{order_id}'
        data = {}
        response = self.delete_request(query, data)
        return response.json()

    def cancel_conditional_order_ftx_id(self, order_id):
        query = f'/api/conditional_orders/{order_id}'
        data = {}
        response = self.delete_request(query, data)
        return response.json()

    def cancel_order_client_id(self, client_id):
        query = f'/api/orders/by_client_id{client_id}'
        data = {}
        response = self.delete_request(query, data)
        return response.json()

    def cancel_all_orders(self, pair = None, side = None, conditional_only = False,
    limit_only = False):
        query = '/api/orders'
        data = {
        'market': pair,
        'side': side,
        'conditionalOrdersOnly': conditional_orders,
        'limitOrdersOnly': limit_orders,
        }
        response = self.delete_request(query, data)
        return response.json()

    def get_fill_history(self, pair, start_time = None, end_time = None):
        if start_time is None or end_time is None:
            query = f'/api/fills?market={pair}'
        else:
            query = f'/api/fills?market={pair}&start_time={start_time}&end_time={end_time}'
        response = self.private_get_request(query)
        return response.json()
