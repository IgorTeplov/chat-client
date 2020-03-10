from .FileStone import FileObject
from typing import Union, List
import os

class PkFile(FileObject):
	def __init__(self, name: str, path: Union[str, List[str]] = os.getcwd()):
		super(PkFile, self).__init__(name, path)
		self.read()

	def read(self) -> None:
		with open(self.full, "r") as pkfile:
			self.body = pkfile.read()

	def create_pk(self, opt: dict) -> tuple:
		self.body = self.body.format(*opt.values())
		data = {}
		for line in self.body.split("\n"):
			if not "/" in line and not line.startswith("-"):
				continue
			line = line[1:]
			line = line.split("/")
			data[line[0]] = line[1]
		if not "app" in data.keys():
			return (False, False)

		return (data, "From {}: {}")

	def __call__(self, opt: dict) -> tuple:
		return self.create_pk(opt)