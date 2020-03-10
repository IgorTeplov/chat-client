from threading import Thread
from .PkFile import PkFile
from .Listener import Listener
from .Server import Server
import socket, time, pickle

class Reconected(Thread):
	def __init__(self, host_port, name):
		super(Reconected, self).__init__()
		self.host_port = host_port
		self._shutdown = False
		self.name = name

	def try_connect(self):
		while True:
			try:
				client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client_sock.connect(self.host_port)
				data = PkFile("settings.pk")({"app":"pirate", "type":"echo-test", "send":"server", "name":self.name})
				client_sock.send(pickle.dumps(data))
				client_sock.close()
			except:
				self._shutdown = True
			else:
				self._shutdown = False
				self.connect()
			time.sleep(1)
				

	def connect(self):
		if not self._shutdown:
			client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_sock.connect(self.host_port)
			data = PkFile("settings.pk")({"app":"pirate", "type":"settings", "send":"server", "name":self.name})
			client_sock.send(pickle.dumps(data))

			self.server_thread = Server(client_sock, self)
			self.listener_thread = Listener(client_sock, self)
			self.server_thread.start()
			self.listener_thread.start()
			self.server_thread.join()
			self.listener_thread.join()

	def run(self):
		self.try_connect()