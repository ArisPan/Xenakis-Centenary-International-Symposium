from pythonosc import udp_client

IP = '127.0.0.1'
PORT = 57120


if __name__ == '__main__':
	client = udp_client.SimpleUDPClient(IP, PORT)
	client.send_message('/print', 440)
