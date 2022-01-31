import json
from requests import Request, Session, Response


class FTXPublicClient(object):
    def __init__(self):
        self.session = Session()
        self.url = 'https://ftx.com'

    def public_get_request(self, query):
        endpoint = self.url + query
        request = Request('GET', endpoint)
        return self.session.send(request.prepare())

    def public_response_status(self):
        query = '/api/'
        response = self.public_get_request(query)
        return response.status_code

    def get_market(self, pair):
        query = f'/api/markets{pair}'
        response = self.public_get_request(query)
        return response.json()

    def get_future(self, pair):
        query = f'/api/futures/{pair}'
        response = self.public_get_request(query)
        return response.json()

    def get_market_history(self, pair, resolution, start_time, end_time):
        query = f'/api/markets/{pair}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
        response = self.public_get_request(query)
        return response.json()

    def get_future_history(self, pair, resolution, start_time, end_time):
        query = f'/api/indexes/{pair}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
        response = self.public_get_request(query)
        return response.json()
