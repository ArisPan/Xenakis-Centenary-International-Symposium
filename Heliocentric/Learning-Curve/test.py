#!/c/Users/Aris/AppData/Local/Programs/Python/Python310/python

import requests
# import json


def main():

	parameters = {
		'data': 'englishName, isPlanet'
	}

	response = requests.get('https://api.le-systeme-solaire.net/rest/bodies', params=parameters)

	if response.status_code == 200:
		# data = json.dumps(response.json(), sort_keys=True, indent=4)
		bodies = response.json()['bodies']
		planets = []
		for body in bodies:
			if body['isPlanet'] is True:
				planets.append(body['englishName'])
		print(planets)
	else:
		print(response.status_code)


if __name__ == '__main__':
	main()
