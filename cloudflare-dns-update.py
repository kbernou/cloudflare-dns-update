# Author: Kaleb Bernou

# Updates old A records in Cloudflare's DNS for the kaleb-bernou.ca zone
# with the new IP address of the server. Needed because I can't get a static IP
# with my current ISP and plan.

# Flow:
#   get public IP address
#   if same as old one, exit
#   update all cloudflare A records with new IP
#   update file with new IP if all records were updated successfully

import requests
import sys
from json import dumps
from datetime import datetime

# TODO: this can probably be handled a bit better
if len(sys.argv) < 3:
    print("Usage: python cloudflare.py <zone_id> <token>")
    exit()

cloudflare_endpoint = "https://api.cloudflare.com/client/v4/"
zone_id = sys.argv[1]
token = sys.argv[2]


def main():
    current_ip = get_current_ip()
    old_ip = get_old_ip()

    if current_ip == old_ip:
        return

    ids = get_dns_records(old_ip)
    all_good = update_dns_records(ids, current_ip)

    if all_good:
        update_old_ip(current_ip)


def get_current_ip():
    return requests.get('https://api.ipify.org').text


def get_old_ip():
    return open("ip", "r").read()


def update_old_ip(ip):
    open("ip", "w").write(ip)


def get_dns_records(old_ip):
    url = f"{cloudflare_endpoint}zones/{zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"type": "A", "content": old_ip}

    res = requests.request("GET", url, data="",
                           headers=headers, params=params).json()
    ids = []

    for record in res["result"]:
        ids.append(record["id"])

    return ids


def update_dns_records(ids, ip):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = dumps({"content": str.rstrip(ip)})

    all_successful = True
    print(ids)
    for dns_id in ids:
        url = f"{cloudflare_endpoint}zones/{zone_id}/dns_records/{dns_id}"
        res = requests.request(
            "PATCH", url, data=payload, headers=headers).json()
        print(res)
        if res["success"] == False:
            all_successful = False
            open("log", "a").write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Record failed to update:\n{res}\n")

    return all_successful
