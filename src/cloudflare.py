import requests, json

CLOUDFLARE_API_URL = 'https://api.cloudflare.com/client/v4'

def gen_headers(cf_user: str, cf_key: str) -> dict:
    headers = {
            'X-Auth-Email': cf_user,
            'X-Auth-Key': cf_key,
            'Content-Type': 'application/json'
            }
    return headers

def get_zone_id(cf_user: str, cf_key: str, domain_name: str) -> str:
    req = requests.get('{}/zones?name={}'.format(CLOUDFLARE_API_URL,domain_name), headers=gen_headers(cf_user, cf_key))
    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return e
    if len(req.json()['result']) < 1:
        return "No results"
    zone_id = req.json()['result'][0]['id']
    return zone_id

def get_record_id(cf_user: str, cf_key: str, zone_id: str, dns_record: str) -> str:
    req = requests.get('{}/zones/{}/dns_records?name={}&type=A'.format(CLOUDFLARE_API_URL, zone_id, dns_record), headers=gen_headers(cf_user, cf_key))
    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return e
    if len(req.json()['result']) < 1:
        return "No results"
    record_id = req.json()['result'][0]['id']
    return record_id

def get_zone_record_ids(cf_user: str, cf_key: str, domain_name: str, dns_record: str) -> dict:
    results = {}
    try:
        results['zone_id'] = get_zone_id(cf_user, cf_key, domain_name)
    except Exception as e:
        print(e)
        return {}

    try:
        results['record_id'] = get_record_id(cf_user, cf_key, results['zone_id'], '{}.{}'.format(dns_record, domain_name))
    except Exception as e:
        print(e)
        return {}
    return results

def update_record(cf_user: str, cf_key: str, zone_id: str, record_id: str, record_content: str, proxied: bool=False) -> bool:
    put_data = { 'content': record_content }
    req = requests.patch('{}/zones/{}/dns_records/{}'.format(CLOUDFLARE_API_URL, zone_id, record_id), headers=gen_headers(cf_user, cf_key), data=json.dumps(put_data))
    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return False
    return True

