import units
from parser import Parser

class Number:
	magnitude = 0
	base = {}
	units = {}

	def __init__(self, num=None):
		self.base = {
			"kg": 0,
			"m": 0,
			"s": 0,
			"A": 0,
			"K": 0,
			"mol": 0,
			"cd": 0
		}
		self.units = {}

		if num is None:
			return

		r = Parser(self, num)

	def __add__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")

		n = self.copy()
		n.magnitude += o.magnitude
		return n

	def __sub__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")

		n = self.copy()
		n.magnitude -= o.magnitude
		return n

	def __mul__(self, o):
		if not isinstance(o, Number):
			n.magnitude *= o
			return n

		n = self.copy()
		for key in n.base:
			n.base[key] += o.base[key]
		n.units.update(o.units)

		n.magnitude *= o.magnitude
		return n

	def __truediv__(self, o):
		if not isinstance(o, Number):
			n.magnitude /= o
			return n

		n = self.copy()
		for key in n.base:
			n.base[key] -= o.base[key]
		n.units.update(o.units)

		n.magnitude /= o.magnitude
		return n

	def __lt__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return n.magnitude < o.magnitude

	def __le__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return n.magnitude <= o.magnitude

	def __eq__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		return n.magnitude == o.magnitude and n.base == o.base

	def __neq__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		return n.magnitude != o.magnitude or n.base != o.base

	def __gt__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return n.magnitude > o.magnitude

	def __ge__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return n.magnitude >= o.magnitude

	def copy(self):
		n = Number()
		n.magnitude = self.magnitude

		#copy() is shallow copy
		n.base = self.base.copy()
		n.units = self.units.copy()
		return n

	def string(self, converts=""):
		order = ["A", "kg", "m", "s", "K", "mol", "cd"]
		s = ""

		n = self

		if converts != "":
			c = Number("1 " + converts)
			n = self.copy()

			converts = ""
			for key in c.units:
				if key in c.base:
					c.base[key] -= c.units[key]
				else:
					converts += key
					if c.units[key] != 1:
						converts += c.units[key]

			n.magnitude /= c.magnitude
			for key in c.base:
				n.base[key] -= c.base[key]

		for key in order:
			if n.base[key] != 0:
				s += key
				if n.base[key] != 1:
					s += str(n.base[key])
		return str(n.magnitude) + " " + converts + s

	def __str__(self):
		return self.string()
