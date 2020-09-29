import requests
import json
import simplejson as json


class SpinRewritter():
    def __init__(self):
        self.url = 'https://www.spinrewriter.com/action/api'
        self.email_address = 'info@katacc.co.uk'
        self.api_key = '97cf48d#cbb77ea_e5e1040?3fbcbf3'

    def unique_variation(self, text):
        try:
            params = {'email_address': self.email_address,
                      'api_key': self.api_key,
                      'action': 'unique_variation',
                      'text': text.encode('utf-8'),
                      'protected_terms': '',
                      'confidence_level': 'high',
                      'nested_spintax': 'true',
                      'spintax_format': 'spin_tag'}
            result = requests.post(self.url, data=params)
            response = json.loads(result.text)
            return response['response']
        except Exception as e:
            print(e)
            return None


def get_spinned(text):
    spin = SpinRewritter()
    return spin.unique_variation(text)