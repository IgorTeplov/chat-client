from classes.GetHostPort import GetHostPort
from classes.Reconected import Reconected

HOST_PORT = GetHostPort()()
NAME = input("Name: ")

def create_client(host_port):
	reconect_thread = Reconected(host_port, NAME)
	reconect_thread.start()

create_client(HOST_PORT)