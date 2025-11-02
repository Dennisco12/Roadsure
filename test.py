#!/usr/bin/python3

import requests
import json

def test_api():
    # base_url = "https://roadsure.onrender.com/roadsure"
    base_url = "http://127.0.0.1:8005/roadsure"
    endpoint = '/users'

    payload = {"email": "dennisivic@gmail.com", 'first_name': " Dennis   ",
            'last_name': "Akinwonjowo", 'password': "Dennisco12"}
    url = base_url + endpoint

    try:
        # resp = requests.post(url, json=payload)
        resp = requests.get(url)
        # resp = requests.delete(url)
        if resp.status_code == 201:
            print(resp.text)
            print(resp.status_code)
        else:
            print("Error in request:", resp.text, "-", resp.status_code)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    test_api()
