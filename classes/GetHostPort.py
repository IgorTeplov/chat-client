class GetHostPort:
	def get_host_port(self):
		host = input("HOST (IP): ")
		if host == "":
			host = '127.0.0.1'
		port = input("PORT: ")
		if port == "":
			port = 61661
		else:
			port = int(port)
		return (host, port)

	def __call__(self):
		return self.get_host_port()