# import requests
# import json

# def get_coordinates(city, state, country):
#     if country.lower() == "us" or country.lower() == "united states":
#         api_url = 'https://api.api-ninjas.com/v1/geocoding?city=' + city + '&state=' + state + 'country=' + country
#     else: 
#         api_url = 'https://api.api-ninjas.com/v1/geocoding?city=' + city + 'country=' + country
    
#     response = requests.get(api_url + city, headers={'X-Api-Key': '6NwQY7rx9RkELLWbuzlktQ==C0X9Dtj2twZRhg9W'})
    
#     if response.status_code == requests.codes.ok:
#         locations = json.loads(response.text)
        
#         # Get the first location from the location list
#         first_location = locations[0]

#         # Extract the details of the first location
#         name = first_location['name']
#         latitude = first_location['latitude']
#         longitude = first_location['longitude']
#         country1 = first_location['country']
#         state1 = first_location['state']

#         return latitude, longitude
#     else:
#         return ("Error:", response.status_code, response.text)
    
# coordinates = get_coordinates(city="Campbell", state="California", country="us")
# latidude = coordinates[0]
# longitude = coordinates[1]

# # def convert_coordinates_to_humidity(lat, lon):
# #     api_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={"796666b6a274950bf900b688681b895d"}'
# #     current_weather = 