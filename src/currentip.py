import requests

def get_current_ip() -> str:
    primary_check = requests.get('http://ipinfo.io/ip')
    return primary_check.text

