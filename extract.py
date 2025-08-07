from dotenv import load_dotenv, find_dotenv
import os
from constantes import BASE_URL
import requests
import logging
from pathlib import Path
import re
import time
from datetime import datetime, timedelta
import pytz

_ = load_dotenv(find_dotenv())

logging.basicConfig(filename=os.path.join(str(Path.home()), 'airport.log'),
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_endpoint(endpoint, endpoint_id=None, params=None):
    
    headers = {
        'Accept': 'application/json',
        'app_id': os.environ.get('APP_ID'),
        'app_key': os.environ.get('APP_KEY'),
        'ResourceVersion': 'v4'
    }
    url = BASE_URL + endpoint

    if endpoint_id:
        url = url + '/' + endpoint_id

    results = []

    response = requests.get(url=url, headers=headers, params=params)
    response.raise_for_status()

    results.append(response.json())

    number_pages = process_pages_number(response.headers)

    while link := process_headers_next(response.headers):
        time.sleep(0.5)
        logger.info(f'Páginas: {number_pages} link: {link}')
        response = requests.get(url=link, headers=headers)
        response.raise_for_status()
        results.append(response.json())
    return results

def process_headers_next(headers):
    headers_link = headers.get('link')

    if not headers_link:
        return None
    
    parts_link = headers_link.split(',')

    reg = r'<(.*)>'

    for link_part in parts_link:
        if 'rel="next"' in link_part:
            link = link_part.split(';')[0]
            link = re.search(reg, link)
            return link.group(1)


def process_pages_number(headers):
    headers_link = headers.get('link')

    if not headers_link:
        return 0

    parts_link = headers_link.split(',')

    reg = r'.*page=([0-9]+).*'

    for part_link in parts_link:
        if 'rel="last"' in part_link:
            number = part_link.split(';')[0]
            number = re.search(reg, number)
            return number.groups()[0]
    return 0

def get_today_flights():
    return get_endpoint('flights')

def get_yesterday_flights():

    now = datetime.now(pytz.timezone('Europe/Amsterdam'))
    yesterday = now.date() - timedelta(days=1)

    yesterday = yesterday.strftime('%Y-%m-%d')

    params = {
        'scheduleDate': yesterday
    }

    return get_endpoint(endpoint='flights', params=params)

def get_flight_by_id(flight_id):
    return get_endpoint(endpoint='flights', endpoint_id=flight_id)

def get_airlines():
    return get_endpoint(endpoint='airlines')

def get_airlines_by_cod(iata):
    return get_endpoint(endpoint='airlines', endpoint_id=iata)

def get_aircraft_types():
    return get_endpoint(endpoint='aircrafttypes')

def get_destinations():
    return get_endpoint(endpoint='destinations')

def get_destinations_by_cod(iata):
    return get_endpoint(endpoint='destinations', endpoint_id=iata)
