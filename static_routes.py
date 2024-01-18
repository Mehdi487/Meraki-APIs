import json
import requests
import csv
import yaml

orgs = {'org-name': 'org-id'}
org_names = orgs.keys()

base_url = 'https://api.meraki.com/api/v1/'
API_KEY = 'personal-key'

headers = {'X-Cisco-Meraki-API-Key': API_KEY, 'Content-Type': 'application/json'}

csv_file = open('static_routes1.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['Network Name', 'Switch Name', 'Static Route Name', 'Subnet', 'Next Hop IP'])

for org_name, org_id in orgs.items():
    response = requests.get(base_url + f'/organizations/{org_id}/networks', headers=headers)

    for network in response.json():
        statics = requests.get(base_url + f'/networks/{network["id"]}/appliance/staticRoutes', headers=headers)
        for static_route_str in statics.json():
            try:
                if isinstance(static_route_str, dict):
                    static_route = static_route_str
                else:
                    static_route = json.loads(static_route_str)

                switch_name = network["name"]
                subnet = static_route.get("subnet", "N/A")
                next_hop_ip = static_route.get("nextHopIp", "N/A")
                static_route_name = static_route.get("name", "N/A")
                csv_writer.writerow([network['name'], switch_name, static_route_name, subnet, next_hop_ip])
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for static route: {static_route_str}")
csv_file.close()
