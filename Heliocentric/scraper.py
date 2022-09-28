import requests
import enum
import time
import sys
import pyOSC3 as osc
from bs4 import BeautifulSoup


# Check if item exists in Enum
# Thanks to: https://stackoverflow.com/a/62854511/13272522
class MyEnumMeta(enum.EnumMeta):
	def __contains__(cls, item):
		try:
			cls(item)
		except ValueError:
			return False
		else:
			return True


class Bodies(enum.Enum, metaclass=MyEnumMeta):
	VENUS = 'venus'
	JUPITER = 'jupiter'
	MARS = 'mars'
	SATURN = 'saturn'
	URANUS = 'uranus'
	MERCURY = 'mercury'
	NEPTUNE = 'neptune'


class HTML_IDs(enum.Enum, metaclass=MyEnumMeta):
	RIGHT_ASCENSION = 'ar'
	DECLINATION = 'dec'
	MAGNITUDE = 'mag'
	CONSTELLATION = 'const'
	SUN_DISTANCE = 'dissun'
	SUN_SPEED = 'speedsun'		# Returns empty
	EARTH_DISTANCE = 'disearth'
	EARTH_SPEED = 'speedearth'		# Returns empty


class CelestialBody():

	def __init__(self, name):

		self.right_ascension = None
		self.declination = None
		self.magnitude = None
		self.constellation = None
		self.sun_distance = None
		self.sun_speed = None
		self.earth_distance = None
		self.earth_speed = None

		if name in Bodies:
			self.name = name
		else:
			sys.exit("Unavailable Celestial Body " + name)

	def set_data(self, data):
		try:
			self.right_ascension = data['right_ascension']
			self.declination = data['declination']
			self.magnitude = data['magnitude']
			self.constellation = data['constellation']
			self.sun_distance = data['sun_distance']
			self.sun_speed = data['sun_speed']
			self.earth_distance = data['earth_distance']
			self.earth_speed = data['earth_speed']
		except Exception as exception_instant:
			print(type(exception_instant) + exception_instant)


class Scrapper():

	BASE_URL = 'https://theskylive.com/'
	URL_SUFFIX = '-tracker'

	def __init__(self, celestial_body_name):

		self.url = self.prepare_url(celestial_body_name)
		self.page = None
		self.parsed_page_content = None

	def prepare_url(self, celestial_body_name):
		return self.BASE_URL + celestial_body_name + self.URL_SUFFIX

	def load_page(self):
		self.page = requests.get(self.url)

	def parse_page(self):
		self.parsed_page_content = BeautifulSoup(self.page.content, "html.parser")

	def get_live_data(self):

		self.load_page()
		self.parse_page()

		live_data = {
			'right_ascension': self.parsed_page_content.find(
				id=HTML_IDs.RIGHT_ASCENSION.value).text,
			'declination': self.parsed_page_content.find(
				id=HTML_IDs.DECLINATION.value).text,
			'magnitude': self.parsed_page_content.find(
				id=HTML_IDs.MAGNITUDE.value).text,
			'constellation': self.parsed_page_content.find(
				id=HTML_IDs.CONSTELLATION.value).text,
			'sun_distance': self.parsed_page_content.find(
				id=HTML_IDs.SUN_DISTANCE.value).text,
			'sun_speed': self.parsed_page_content.find(
				id=HTML_IDs.SUN_SPEED.value).text,		# Returns empty
			'earth_distance': self.parsed_page_content.find(
				id=HTML_IDs.EARTH_DISTANCE.value).text,
			'earth_speed': self.parsed_page_content.find(
				id=HTML_IDs.EARTH_SPEED.value).text		# Returns empty
		}

		return live_data


class OSC:
	IP = '127.0.0.1'
	PORT = 57120

	def __init__(self):
		self.client = osc.OSCClient()
		self.client.connect((self.IP, self.PORT))

		self.message = osc.OSCMessage()

	def prepare_message(self, address, values):
		self.message.setAddress(address)
		for value in values:
			self.message.append(value)

	def send_message(self):
		self.client.send(self.message)


def main():
	if len(sys.argv) != 2:
		sys.exit(
			'Wrong number of arguments.\n'
			+ 'Try \'python scrapper.py --help\' for more information.')
	if str(sys.argv[1]) == '--help':
		print_help_dialog()
		sys.exit()

	celestial_body_name = sys.argv[1]

	start_time = time.perf_counter()

	body = CelestialBody(celestial_body_name)
	scrapper = Scrapper(celestial_body_name)

	body.set_data(scrapper.get_live_data())

	finish_time = time.perf_counter()

	temp = vars(body)
	for var in temp:
		print(str(var) + ': ' + str(temp[var]))
	print('[Fetched in', finish_time - start_time, 'seconds]')		# Under 4 seconds.

	while True:
		body.set_data(scrapper.get_live_data())
		temp = vars(body)
		normalized_values = [
			int(temp['earth_distance']) % 1000,
			float(temp['sun_distance']) % 0.3
		]

		print(normalized_values)

		# normalized_earth_distance = int(temp['earth_distance']) % 1000
		# normalized_magnitude = float(temp['earth_distance']) % 10000
		# print("New Frequency: " + str(normalized_earth_distance))
		# print("New delay iterations: " + str(normalized_magnitude))

		messenger = OSC()
		messenger.prepare_message('/sonify', normalized_values)
		messenger.send_message()

		time.sleep(1)


def print_help_dialog():
	print(
		'Usage: python scraper.py [PLANET NAME]\n'
		+ 'Retrieve planet\'s live postion and data.\n'
		+ 'Example: python scraper.py neptune\n\n'
		+ 'Live data available for: '
	)
	for celestial_body in Bodies:
		print(celestial_body.value)


if __name__ == '__main__':
	main()
