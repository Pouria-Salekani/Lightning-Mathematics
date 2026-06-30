#the middle-man

import requests

URL = 'http://127.0.0.1:8000/analyze'

def api_expression_analyzer(expression, bundle=None):
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
    
def get_history():
    try:
        req = requests.get('http://127.0.0.1:8000/history', timeout=5)
        req.raise_for_status()
        return req.json()
    except requests.RequestException:
        return []
    
def delete_expr(expr_id):
    try:
        req = requests.delete(f'http://127.0.0.1:8000/history/{expr_id}', timeout=5)
        req.raise_for_status()
        return req.json()
    except requests.RequestException:
        return {'error': 'Unavailable'}