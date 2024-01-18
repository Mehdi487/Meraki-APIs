import json
import requests
import csv
import yaml

orgs = {'org-name': 'org-id'}
org_names = orgs.keys()

base_url = 'https://api.meraki.com/api/v1/'
API_KEY = 'personal-key'

headers = {'X-Cisco-Meraki-API-Key': API_KEY, 'Content-Type': 'application/json'}

response = requests.get(base_url + '/organizations/228136/networks', headers=headers)
print(response.json())

with open('subnet_info.csv', 'w', newline='') as csvfile:
    fieldnames = ['Network Name', 'VLAN ID', 'VLAN Name', 'Subnet']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for network in response.json():
        vlans = requests.get(base_url + f'/networks/{network["id"]}/appliance/vlans', headers=headers)
        vlans_data = vlans.json()
        print("VLANs Data:", vlans_data)  
        if 'errors' in vlans_data and 'This endpoint only supports MX networks' in vlans_data['errors'][0]:
            print(f"This endpoint only supports MX networks for the network '{network['name']}'. Skipping.")
            continue
        if isinstance(vlans_data, list):
            for vlan in vlans_data:
                network_name = network['name']
                vlan_id = vlan.get('id', '')
                vlan_name = vlan.get('name', '')
                subnet = vlan.get('subnet', '')
                writer.writerow({
                    'Network Name': network_name,
                    'VLAN ID': vlan_id,
                    'VLAN Name': vlan_name,
                    'Subnet': subnet
                })
        else:
            print(f"Unexpected response format for the network '{network['name']}'. Skipping.")
