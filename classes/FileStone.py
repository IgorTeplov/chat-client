from typing import Union, List
import os, json, pickle, xml.etree.ElementTree as ET

# global function
def normal_path(path: Union[str, List[str]]) -> str:
	if isinstance(path, str):
		path = path.replace("\\", "/")+"/"
		if not os.path.isdir(path):
			os.makedirs(path)
		return path
	elif isinstance(path, list):
		path = "/".join(path)+"/"
		if not os.path.isdir(path):
			os.makedirs(path)
		return path
	else:
		raise TypeError

def drivers_win() -> List[str]:
	l_drivers = []
	for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
		if os.path.isdir(drive + ":/"):
			l_drivers.append(drive + ":/")
	return l_drivers

BASE_PATH_LIST = [*os.getcwd().split("\\"), ]
WIN_DRIVE = drivers_win()

class FileObject():

	def __init__(self, name: str, path: Union[str, List[str]] = os.getcwd()) -> None:
		self.path = normal_path(path)
		self.name = name
		self.full = self.path + self.name
		self.extension = self.name.split(".")[-1]

		if not os.path.isfile(self.full):
			with open(self.full, "x") as file:
				pass
			self.last_time = os.path.getctime(self.full)
		else:
			self.last_time = os.path.getctime(self.full)

	def remove(self) -> None:
		os.remove(self.full)

	def rename(self, name: str) -> None:
		os.rename(self.full, self.path + name)
		self.name = name
		self.full = self.path + name

	def relocate(self, path: Union[str, List[str]]) -> None:
		path = normal_path(path)
		os.rename(self.full, path + self.name)
		self.path = path
		self.full = path + self.name

class TextFile(FileObject):

	def __init__(self, name: str, path: Union[str, List[str]] = os.getcwd()) -> None:
		super(TextFile, self).__init__(name, path)

	def write(self, data: Union[str, List[str]], options: str = "w") -> None:
		# options = "w", "a"
		with open(self.full, options) as file:
			if isinstance(data, str):
				file.write(data)
			elif isinstance(data, list):
				for line in data: 
					file.writelines(line+"\n")

		self.last_time = os.path.getctime(self.full)


	def read(self, options: str = "normal") -> Union[str, List[str]]:
		# options = "normal", "lines"
		with open(self.full, "r") as file:
			if options == "normal":
				data = file.read()
			elif options == "lines":
				data = file.readlines()
		return data

	def __call__(self, options: str = "normal") -> Union[str, List[str]]:
		return self.read(options)

class JsonFile(FileObject):
	
	def __init__(self, name: str, path: Union[str, List[str]] = os.getcwd()) -> None:
		super(JsonFile, self).__init__(name, path)

	def upload(self, data: Union[str, dict], options: str = "normal") -> None:
		# options = "normal", "add", "add_rewrite"
		if options == "normal":
			with open(self.full, "w") as jfile:
				if isinstance(data, str):
					json.dump(json.loads(data), jfile, indent=4)
				elif isinstance(data, dict):
					json.dump(data, jfile, indent=4)
		elif options in ("add", "add_rewrite"):
			with open(self.full, "r") as temp_file:
				data_from_file = json.load(temp_file)
			with open(self.full, "w") as jfile:
				if isinstance(data, str):
					user_data = json.loads(data)
				elif isinstance(data, dict):
					user_data = data
				keys1 = data_from_file.keys()
				keys2 = user_data.keys()
				r = keys1^keys2 if options == "add" else keys1|keys2
				r = r&keys2
				for key in r:
					data_from_file[key] = user_data[key]
				json.dump(data_from_file, jfile, indent=4)
		self.last_time = os.path.getctime(self.full)


	def load(self, options: str = "normal") -> Union[dict, str]:
		# options = "normal", "str"||"string"
		with open(self.full, "r") as jfile:
			if options == "normal":
				return json.load(jfile)
			elif options in ("str", "string"):
				return json.dumps(json.load(jfile))

	def __call__(self, options: str = "normal") -> Union[dict, str]:
		return self.load(options)

class BinaryFile(FileObject):

	def __init__(self, name: str, path: Union[str, List[str]] = os.getcwd()) -> None:
		super(BinaryFile, self).__init__(name, path)

	def upload(self, data) -> None:
		with open(self.full, "wb") as bfile:
			pickle.dump(data, bfile)

		self.last_time = os.path.getctime(self.full)

	def load(self):
		with open(self.full, "rb") as bfile:
			return pickle.load(bfile)

	def __call__(self):
		return self.load()

class XMLDocument(FileObject):

	def __init__(self, name: str, path: Union[str, List[str]] = os.getcwd()) -> None:
		super(XMLDocument, self).__init__(name, path)

		self.tree = ET.parse(self.full)
		self.root = self.tree.getroot()

	def get_elements(self):
		elements = []
		for child in self.root:
			elements.append({"tag":child.tag, "atributs":child.attrib, "text":child.text, "XMLTagElement":child})
		return elements

	@property
	def rt(self):
		return self.root.tag
	
	@property
	def ra(self):
		return self.root.attrib

class XMLToJSON():
	
	def __init__(self, XMLDocument_root):
		self.json = {
			"tag": XMLDocument_root.tag,
			"attributs": XMLDocument_root.attrib,
			"text": XMLDocument_root.text,
			"childs": self.get_info(XMLDocument_root)
		}
		self.get_info(XMLDocument_root)

	def get_info(self, element):
		data = {}
		index = 0
		if len(element) > 0:
			for child in element:
				data["{}__{}".format(child.tag, index)] = {
					"tag":child.tag, 
					"attributs":child.attrib, 
					"text":child.text, 
					"childs":self.get_info(child)
				}
				index += 1
		return data