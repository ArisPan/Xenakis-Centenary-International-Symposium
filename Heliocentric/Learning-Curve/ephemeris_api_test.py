#!/c/Users/Aris/AppData/Local/Programs/Python/Python310/python

import requests
# from urllib2 import Request, urlopen

URL = 'http://ephemeris.kibo.cz/api/v1/planets'

if __name__ == '__main__':

	values = {
		"event": "YYYYMMDDhhmmss",
		"planets": ["Sun", "Moon"],
		"topo": ['longitude', 'latitude', 'geoalt'],
		"zodiac": "sidereal mode name"
	}

	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}

	response = requests.get(URL, params=values, headers=headers)
	print(response.json)

	# request = Request('http://ephemeris.kibo.cz/api/v1/planets', data=values, headers=headers)
	# response_body = urlopen(request).read()
	# print(response_body)
