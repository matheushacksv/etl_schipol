from datetime import datetime, timezone

def attributes_dict(flight, list_attributes):

    results = dict()

    for attribute in list_attributes:
        results[attribute] = flight.get(attribute)

    results

def attributes_date_dict(flight, list_attributes):
    
    results = {}

    for attribute in list_attributes:
        date = flight.get(attribute)

        if date:
            try:
                date = datetime.fromisoformat(date).astimezone(timezone.utc)
            except:
                date = None

        results[attribute] = date

    return results

def transform_flights(flights_pages):
    
    results = []
    flights = []

    for flight_page in flights_pages:
        flights.extend(flight_page['flights'])
    
    for flight in flights:

        aircraftType = flight.get('aircraftType')

        aircraftType_iataMain = None
        aircraftType_iataSub = None

        if aircraftType:
            aircraftType_iataMain = aircraftType.get('iataMain')
            aircraftType_iataSub = aircraftType.get('iataSub')

        route = None
        eu = None
        visa = None
        flight_route = flight.get('route')
        if flight_route:
            destinations = flight_route.get('destinations')
            eu = flight_route.get('eu')
            visa = flight_route.get('visa')
            if destinations:
                route = ','.join(destinations)
        
        codeshares = None
        flight_codeshares = flight.get('codeshares')
        if flight_codeshares:
            flight_codeshares = flights.get('codeshares')
            if flight_codeshares:
                codeshares = ','.join(flight_codeshares)

        flights_states = None
        public_flight_states = flight.get('publicFlightstate')
        if public_flight_states:
            flight_states = public_flight_states.get('flightStates')
            if flights_states:
                flights_states = ','.join(flights_states)
        
        attributes = {
            'aircraftType_iataMain': aircraftType_iataMain,
            'aircraftType_iataSub': aircraftType_iataSub,
            'route': route,
            'codeshares': codeshares,
            'flightStates': flight_states,
            'eu': eu,
            'visa': visa
        }

        attributes.update(
            attributes_dict(
                flight,
                [
                    'flightDirection',
                    'flightName',
                    'gate',
                    'pier',
                    'id',
                    'isOperationalFlight',
                    'mainFlight',
                    'prefixIATA',
                    'prefixICAO',
                    'airlineCode',
                    'aircraftRegistration',
                    'serviceType',
                    'terminal',
                ]
            )
        )

        attributes.update(
            attributes_date_dict(
                flight,
                [
                    'estimatedLandingTime',
                    'lastUpdateAt',
                    'actualLandingTime',
                    'scheduleDateTime',
                    'actualOffBlockTime',
                    'expectedTimeGateClosing',
                    'expectedTimeGateOpen',
                    'expectedTimeOnBelt',
                    'expectedSecurityFilter',
                    'publicEstimatedOffBlockTime',
                ]
            )
        )

        results.append(attributes)
    return results

def transform_destinations(destinations_pages):

    results = []
    destinations = []

    for page in destinations_pages:
        destinations.extend(page.get('destinations'))

    for destination in destinations:
        name = destination.get('publicName')
        if name:
            name = name.get('english')
        results.append(
            {
            'name': name,
            'country': destinations.get('country'),
            'iata': destinations.get('iata'),
            'city': destinations.get('city')
            }
        )
    return results


def transform_aircraft_types(aircraft_types_pages):

    results = []
    aircraft_types = []

    for page in aircraft_types_pages:
        aircraft_types.extend(page.get('aircraftTypes'))

    for aircraft in aircraft_types:
        results.append(
            {
            'iataMain': aircraft.get('iataMain'),
            'iataSub': aircraft.get('iataSub'),
            'description': aircraft.get('longDescription')
            }
        )
    return results

def transform_airlines(airlines_pages):

    results = []
    airlines = []

    for page in airlines_pages:
        airlines.extend(page.get('airlines'))

    for airline in airlines:
        results.append(
            {
            'iata': airline.get('iata'),
            'icao': airline.get('icao'),
            'nvls': airline.get('nvls'),
            'name': airline.get('publicName')
            }
        )
    return results

