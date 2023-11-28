import requests
import json

property_search_url = "https://www.edgeprop.my/jwdsonic/api/v1/property/search"
property_search_payload = {
    'listing_type': 'sale',
    'state': 'Malaysia',
    'property_type': 'rl',
    'keyword': 'putrajaya',
    'start': 0,
    'size': 20
}

agent_area_specialist_url = "https://www.edgeprop.my/jwdsonic/api/v1/agent/pro-area-specialist"
agent_area_specialist_payload = {
    'state': 'keyword',
    'area': 'putrajaya',
    'ptype': 'rl',
    'size': 10
}

global_area_by_state_url = "https://www.edgeprop.my/jwdsonic/api/v1/global/areabystate"
global_area_by_state_payload = {
    'state': 'Malaysia'
}

property_update_list_view_url = "https://www.edgeprop.my/jwdsonic/api/v1/property/update/listview"
property_update_list_view_payload = {}

urls_payloads = [
    (property_search_url, property_search_payload),
    (agent_area_specialist_url, agent_area_specialist_payload),
    (global_area_by_state_url, global_area_by_state_payload),
    (property_update_list_view_url, property_update_list_view_payload)
]

for url, payload in urls_payloads:
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        data = response.json()
        print("URL:", url)
        print("Response:")
        print(json.dumps(data, indent=4))
        print()
    else:
        print("Failed to retrieve data from URL:", url)
