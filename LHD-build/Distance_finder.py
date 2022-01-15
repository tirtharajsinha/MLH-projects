from math import radians, asin, cos, sin, sqrt
import urllib.request, urllib.parse, urllib.error
import json
import ssl


def gloc_address(address):
    api_key = False
    # If you have a Google Places API key, enter it here
    # api_key = 'place api key here'
    # https://developers.google.com/maps/documentation/geocoding/intro

    if api_key is False:
        api_key = 42
        serviceurl = 'http://py4e-data.dr-chuck.net/json?'
    else:
        serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        if len(address) < 1: break

        parms = dict()
        parms['address'] = address
        if api_key is not False: parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)

        print('Retrieving', url, end="\r")
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()

        try:
            js = json.loads(data)
        except:
            js = None

        if not js or 'status' not in js or js['status'] != 'OK':
            print('==== Failure To Retrieve ====')
            continue

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        return [lat, lng]


def finder(loc1, loc2, unit="kilometer"):
    lat1 = radians(loc1[0])
    lat2 = radians(loc2[0])
    lon1 = radians(loc1[1])
    lon2 = radians(loc2[1])
    print(loc1, loc2)
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    result = round((c * r), 2)

    if unit.lower() == "meter":
        return result * 1000
    return result

def distance_finder(place1,place2,unit):
    loc1 = gloc_address(place1)
    loc2 = gloc_address(place2)
    return finder(loc1, loc2, unit=unit)

place1 = "london"
place2 = "kolkata"

unit = "KM"
print("Distance between {} and {} is : ".format(place1, place2), distance_finder(place1, place2, unit=unit),
      unit)
