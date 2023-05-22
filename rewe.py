import requests

class ReweClient():
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_receipts(self):
        data = self.make_request('/receipts')
        return data['items']
    
    def get_receipt(self, receipt_id: str):
        data = self.make_request(f'/receipts/{receipt_id}')
        return data

    def make_request(self, url: str):
        cookies = {
            'rstp': self.auth_token
        }
        r = requests.get(self.base_url + url, cookies=cookies)
        return r.json()
    