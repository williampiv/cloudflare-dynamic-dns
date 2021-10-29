import cloudflare as cf
import currentip as ip
import configparser as c
import json

def main() -> None:
    current_ip = ip.get_current_ip()
    cloudflare_creds = c.ConfigParser()
    cloudflare_creds.read('cloudflare_creds.ini')
    dns_configs = c.ConfigParser()
    dns_configs.read('dns.ini')
    for section in dns_configs.sections():
        print('Updating Records Under: {}'.format(section))
        records = json.loads(dns_configs.get(section, 'records'))
        for rec in records:
            record_data = cf.get_zone_record_ids(cloudflare_creds['cloudflare_creds']['email'],cloudflare_creds['cloudflare_creds']['auth_key'], section, rec)
            update_record = cf.update_record(cloudflare_creds['cloudflare_creds']['email'],cloudflare_creds['cloudflare_creds']['auth_key'], record_data['zone_id'], record_data['record_id'], current_ip)
            print('{}.{} Updated: {}'.format(rec, section, update_record))
    return None

if __name__ == '__main__':
    main()
