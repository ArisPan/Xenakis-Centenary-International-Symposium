import pyOSC3 as osc

IP = '127.0.0.1'
PORT = 57120

if __name__ == '__main__':
	client = osc.OSCClient()
	client.connect((IP, PORT))

	msg = osc.OSCMessage()
	msg.setAddress('/print')
	msg.append(150)

	client.send(msg)
