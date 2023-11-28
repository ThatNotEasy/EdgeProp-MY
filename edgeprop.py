# Author: Cai

import requests
import json
import os
import random
import configparser
from sys import stdout
from colorama import Fore, Style
from lib.postgresdb import POSTGRESQL

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

FY = Fore.YELLOW
FG = Fore.GREEN
FR = Fore.RED
FW = Fore.WHITE
FC = Fore.CYAN
RC = Fore.RESET

def dirdar():
    if not os.path.exists('Results'):
        os.mkdir('Results')
dirdar()

def edgeprop():
    os.system('clear' if os.name == 'posix' else 'cls')
    stdout.write("                                                                                         \n")
    stdout.write(""+Fore.LIGHTRED_EX +"███████╗██████╗  ██████╗ ███████╗██████╗ ██████╗  ██████╗ ██████╗ \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗\n")
    stdout.write(""+Fore.LIGHTRED_EX +"█████╗  ██║  ██║██║  ███╗█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝ \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╔══╝  ██║  ██║██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝\n")
    stdout.write(""+Fore.LIGHTRED_EX +"███████╗██████╔╝╚██████╔╝███████╗██║     ██║  ██║╚██████╔╝██║\n")
    stdout.write(""+Fore.LIGHTRED_EX +"╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝\n")
    stdout.write(""+Fore.YELLOW +"═════════════╦═════════════════════════════════╦══════════════════════════════\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"DESCRIPTION     "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   AUTOMATED WEB SCRAPPING & CRAWLER                "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n")
edgeprop()

def users_agents():
    with open("lib/ua.txt", "r") as ua_file:
        user_agents = [ua.strip() for ua in ua_file.readlines() if ua.strip()]
    return user_agents

def make_request(url, payload, headers):
    try:
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"{FR}An error occurred during the request:", e)
        exit()
    except ValueError:
        print(f"{FR}Invalid JSON response")
        exit()

def output(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def read_json_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def insert_data_into_db(data, data_type):
    db = POSTGRESQL()
    insert_query = """
        INSERT INTO property."EDGEPROP" ("TYPE", "AGENT_NAME", "AGENT_CONTACT", "TITLE", "STATE", "DISTRICT", "STREET", "ZIP_CODE", "LONGITUDE", "LATITUDE", "PRICE", "DESC", "URL")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ("TYPE", "AGENT_NAME", "AGENT_CONTACT", "TITLE", "STATE", "DISTRICT", "STREET", "ZIP_CODE")
        DO UPDATE SET
        ("TYPE", "AGENT_NAME", "AGENT_CONTACT", "TITLE", "STATE", "DISTRICT", "STREET", "ZIP_CODE") = (EXCLUDED."TYPE", EXCLUDED."AGENT_NAME", EXCLUDED."AGENT_CONTACT", EXCLUDED."TITLE", EXCLUDED."STATE", EXCLUDED."DISTRICT", EXCLUDED."STREET", EXCLUDED."ZIP_CODE");
    """
    for property_data in data:
        values = (
            data_type,
            property_data['agent_name_s_lower'],
            property_data['agent_contact_s_lower'],
            property_data['title_t'],
            property_data['state_s_lower'],
            property_data['district_s_lower'],
            property_data.get('field_prop_street_t', ''),
            str(property_data.get('field_prop_postcode_i', '')),
            '',
            '',
            '',
            property_data.get('desc', ''),
            property_data.get('url_s', '')
        )

        location_p = property_data.get('location_p')
        if location_p:
            location_parts = location_p.split(',')
            if len(location_parts) >= 2:
                values = values[:8] + (location_parts[0].strip(), location_parts[1].strip()) + values[10:]

        price = property_data.get('field_prop_asking_price_d')
        if isinstance(price, int):
            values = values[:10] + (price,) + values[11:]
        elif isinstance(price, str) and 'RM' in price:
            price_value = float(price.replace('RM', '').replace(',', '').strip())
            values = values[:10] + (price_value,) + values[11:]

        db.execute(insert_query, values)
    db.commit()
    print(Fore.GREEN + '[SUCCESS]   : ', Fore.CYAN + 'Inserted Into Databases' + '\n')

def main():
    print(f"{FY}[1] - {FG}BUY (SALE)      {FY}[2] - {FG}RENT\n")
    options = input(f"{FY}[CHOOSE]  : {FG}")
    state = input(f"{FY}[AREA]    : {FG}")

    property_url = "https://www.edgeprop.my/jwdsonic/api/v1/property/search"
    user_agents = users_agents()
    headers = {'user-agent': random.choice(user_agents)}

    sale_payload = {'listing_type': 'sale', 'state': 'Malaysia', 'property_type': 'rl', 'keyword': state, 'start': 0, 'size': 520}
    rent_payload = {'listing_type': 'rent', 'state': 'Malaysia', 'property_type': 'rl', 'keyword': state, 'start': 0, 'size': 520, 'type': 'web'}

    if options == '1':
        data = make_request(property_url, sale_payload, headers)
        print(json.dumps(data, indent=4))
        filename = f"Results/{state}_sale_data.json"
        output(data, filename)
        insert_data_into_db(data['property'], 1)

    elif options == '2':
        data = make_request(property_url, rent_payload, headers)
        print(json.dumps(data, indent=4))
        filename = f"Results/{state}_rent_data.json"
        output(data, filename)
        insert_data_into_db(data['property'], 2)

    else:
        print(f"{FR}Invalid choice!")
        exit()

if __name__ == "__main__":
    main()