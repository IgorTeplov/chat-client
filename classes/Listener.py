from threading import Thread
import socket, pickle

class Listener(Thread):
	def __init__(self, client_sock, root):
		super(Listener, self).__init__()
		self.client = client_sock
		self.root = root

	def run(self):
		while not self.root._shutdown:
			try:
				data = self.client.recv(2048)
				data = pickle.loads(data)
			except ConnectionResetError:
				if not self.root._shutdown:
					print("Server on {}:{} down... :'(".format(self.root.host_port[0], self.root.host_port[1]))
					self.root._shutdown = True
				else:
					pass
			else:
				if not data:
					break
				print(data)