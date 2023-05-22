import requests

class GrocyClient():
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

    def find_product(self, rewe_id: str):
        data = self.make_request(f'/objects/products?query%5B%5D=description~rewe_id%3D{rewe_id}', 'GET')
        if len(data) == 0:
            return None
        return data[0]['id']

    def create_product(self, rewe_id: str, name: str):
        data = self.make_request(f'/objects/products', 'POST', data={
            "name": f"{name} {rewe_id}",
            "description": f"rewe_id={rewe_id}",
            "location_id": "4", # TODO
            "qu_id_purchase": "3",
            "qu_id_stock": "3",
            "qu_factor_purchase_to_stock": "1.0"
        })

        product_id = data['created_object_id']
        return product_id
    
    def find_or_create_product(self, rewe_id: str, name: str):
        product_id = self.find_product(rewe_id)
        if (product_id == None):
            product_id = self.create_product(rewe_id, name)

        return product_id
    
    def add_stock(self, product_id: int, amount: int, price: int):
        self.make_request(f'/stock/products/{product_id}/add', 'POST', {
            'amount': amount,
            'transaction_type': "purchase",
            'price': f'{price // 100}.{(price % 100):02}'
        })

    def make_request(self, url: str, method = 'GET', data=None):
        headers = {
            'Grocy-Api-Key': self.api_key
        }
        r = requests.request(url=self.base_url + url, headers=headers, method=method, data=data)
        return r.json()
    
