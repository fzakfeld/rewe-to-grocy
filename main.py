from rewe import ReweClient
from grocy import GrocyClient
import json
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO)

rewe = ReweClient(
    auth_token = config['REWE']['auth_token'],
    base_url= 'https://shop.rewe.de/api'
)
grocy = GrocyClient(
    api_key = config['Grocy']['api_key'],
    base_url = config['Grocy']['base_url']
)

def get_state() -> dict:
    try:
        f = open('state.json', 'r')
        state = json.load(f)
    except:
        state = {
            'parsed_receipts': []
        }
    return state

def save_state(state: dict):
    f = open('state.json', 'w')
    json.dump(state, f)

def parse_receipt(receipt: dict):
    logging.info(f'Parsing receipt {receipt["receiptId"]}')
    for article in receipt['articles']:
        if ('productName' not in article):
            continue
        product_id = grocy.find_or_create_product(
            rewe_id=article['nan'],
            name=article['productName']
        )
        logging.info(f'Adding {article["quantity"]} of {product_id} ({article["productName"]}) to stock')
        grocy.add_stock(
            product_id=product_id,
            amount=article['quantity'],
            price=article['unitPrice']
        )

def main():
    state = get_state()

    receipts = rewe.get_receipts()

    for r in receipts:
        if r['receiptId'] not in state['parsed_receipts']:
            receipt = rewe.get_receipt(r['receiptId'])
            parse_receipt(receipt)
            state['parsed_receipts'].append(r['receiptId'])

    save_state(state)

if __name__ == '__main__':
    main()