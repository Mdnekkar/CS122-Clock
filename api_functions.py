import requests
import json
import os

def verify_location_and_get_coordinates(city, country, state=" "):
    different_usa = ["us", "united states", "usa", "united states of america"]
    if country.lower() in different_usa:
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}&state={state}&country={country}'
    else: 
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}'
    
    try: 
        response = requests.get(api_url, headers={'X-Api-Key': "6NwQY7rx9RkELLWbuzlktQ==C0X9Dtj2twZRhg9W"})
        
        if response.status_code == requests.codes.ok:
            locations = json.loads(response.text)
            
            if locations: 
                # Get the first location from the location list
                first_location = locations[0]

                # Extract the details of the first location
                latitude = first_location['latitude']
                longitude = first_location['longitude']

                return latitude, longitude
            else: 
                return 0
        else:
            return 0
    except requests.exceptions.RequestException as e:
        return 0
        

def convert_coordinates_to_humidity(lat, lon):

    import requests

    url = "https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey=qkmebBv8ketyz5R6Iomew2Cb07rGJTMu"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    weather_data = json.loads(response.text)

    humidity = weather_data['data']['values']['humidity']
    celcius_temp = weather_data['data']['values']['temperature']

    farenheit_temp = (celcius_temp*9/5) + 32

    return (humidity, farenheit_temp)
    
print(convert_coordinates_to_humidity(33.44, -94.04))

    