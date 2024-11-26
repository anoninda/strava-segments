#Obtention du token  via url : https://www.strava.com/oauth/authorize?client_id=140831&response_type=code&redirect_uri=http://localhost&scope=activity:read,activity:read_all


import requests
import json
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="myApp")

def get_access_token (code) : 
    files = {
        'client_id': (None, '140831'),
       'client_secret': (None, '9560502976b5814e184ccfa8925af04d36f2bb7a'),
      'code': (None, code),
      'grant_type': (None, "authorization_code")
    }
    response = requests.post('https://www.strava.com/oauth/token', files=files)
    return (response.json()['access_token'])

def get_activities (access_token) : 
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': f'Bearer {access_token}'}
    param = {'per_page': 200, 'page': 1}
    data = requests.get(activites_url,headers=header, params=param).json()
    return data

def get_segment_info (id_seg, access_token) :
    segments_url = 'https://www.strava.com/api/v3/segments/' + id_seg
    header = {'Authorization': f'Bearer {access_token}'}
    param = {'per_page': 200, 'page': 1}
    data_segment = requests.get(segments_url,headers=header).json()
    return data_segment

def get_segment_geo_coord (nom_location, distance_km, access_token) :
    explore_url = 'https://www.strava.com/api/v3/segments/explore'
    center = geolocator.geocode(nom_location)
    sw_point = geodesic(kilometers=distance_km).destination((center.latitude, center.longitude), 225) 
    ne_point = geodesic(kilometers=distance_km).destination((center.latitude, center.longitude), 45) 
    bounds = str(sw_point.latitude)+','+str(sw_point.longitude)+','+str(ne_point.latitude)+','+str(ne_point.longitude)
    param = { "bounds": bounds, "activity_type": 'running' }
    header = {'Authorization': f'Bearer {access_token}'}
    data_segments = requests.get(explore_url, headers=header, params=param).json()
    return data_segments


access_token  = get_access_token('83716d4b644b5c93e052fc5799ec4da54fb52ada')

#id_seg = '675241'

data_segments = get_segment_geo_coord('Tour Eiffel', 2, access_token)
