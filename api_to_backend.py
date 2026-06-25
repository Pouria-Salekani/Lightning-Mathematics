import requests

URL = 'http://127.0.0.1:8000/analyze'

def expression_analyzer(expression, bundle=None):
    hash = {
        'expression':expression,
        'bundle':bundle
    }


    try:
        print(hash)
        req = requests.post(URL, json=hash, timeout=5)  #sends a POST; create data;
                                                        #to that one method in backend/main.py
        req.raise_for_status()
        return req.json()
    except requests.RequestException:
        return None