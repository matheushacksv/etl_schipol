from extract import *
from save import save
from transform import *

def main_etl():
    # Extract
    
    airlines_pages = get_airlines()
    aircraft_types_pages = get_aircraft_types()
    destinations_pages = get_destinations()
    flights_pages = get_today_flights()
    
    
    # Transform

    airlines = transform_airlines(airlines_pages)
    aircraft_types = transform_aircraft_types(aircraft_types_pages)
    destinations = transform_destinations(destinations_pages)
    flights = transform_flights(flights_pages)

    # Load

    save(
        './',
        [
            airlines,
            aircraft_types,
            destinations,
            flights
        ],
        [
            'airlines',
            'aircraft_types',
            'destinations',
            'flights'
        ]
    )

if __name__ == '__main__':
    main_etl()      