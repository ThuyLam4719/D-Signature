import requests
import json
import os

CA_SERVER = "http://127.0.0.1:5000/api/submit_request"

def gui_yeu_cau(pubkey_path, cn, org, country):
    try:
        with open(pubkey_path, "r") as f:
            pubkey_pem = f.read()

        data = {
            "cn": cn,
            "org": org,
            "country": country,
            "public_key": pubkey_pem
        }

        response = requests.post(CA_SERVER, json=data)
        if response.status_code == 200:
            return "OK"
        else:
            return f"Lỗi từ CA: {response.text}"
    except Exception as e:
        return str(e)
