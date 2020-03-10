from threading import Thread
from .PkFile import PkFile
import socket, pickle

class Server(Thread):
	def __init__(self, client_sock, root):
		super(Server, self).__init__()
		self.client = client_sock
		self.root = root

	def run(self):
		while not self.root._shutdown:
			if not self.root._shutdown:
				massage = input("Massage: ")
				try:
					data = PkFile("massage.pk")({"app":"pirate", "send":"ALL", "massage":massage})
					self.client.send(pickle.dumps(data))
				except:
					pass