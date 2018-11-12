import parser
import units

class Number:
	magnitude = 0
	base = {}
	units = {}

	def __init__(self, num=None, prsr=None):
		self.base = {
			"kg": 0,
			"m": 0,
			"s": 0,
			"K": 0,
			"A": 0,
			"mol": 0,
			"cd": 0
		}
		self.units = {}

		if num is None:
			return

		if prsr is None:
			prsr = parser.Parser()

		r = prsr.parse(self, num)
		self.magnitude = r.magnitude
		self.base = r.base
		self.units = r.units

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
		n = self.copy()

		if not isinstance(o, Number):
			n.magnitude *= o
			return n

		for key in n.base:
			n.base[key] += o.base[key]
		n.units.update(o.units)

		n.magnitude *= o.magnitude
		return n

	def __truediv__(self, o):
		n = self.copy()

		if not isinstance(o, Number):
			n.magnitude /= o
			return n

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
		return self.magnitude < o.magnitude

	def __le__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return self.magnitude <= o.magnitude

	def __eq__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		return self.magnitude == o.magnitude and self.base == o.base

	def __neq__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		return self.magnitude != o.magnitude or self.base != o.base

	def __gt__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return self.magnitude > o.magnitude

	def __ge__(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")
		return self.magnitude >= o.magnitude

	def copy(self):
		n = Number()
		n.magnitude = self.magnitude

		#copy() is shallow copy
		n.base = self.base.copy()
		n.units = self.units.copy()
		return n

	def string(self, converts="", space=False, caret=False, scientific=False, printunits=True):
		order = ["kg", "m", "s", "K", "A", "mol", "cd"]
		s = ""
		tempconvert = False

		n = self

		if converts != "":
			c = Number("1 " + converts)
			n = self.copy()

			for key in c.units:
				if key in units.temperaturemap:
					if key != "K":
						tempconvert = True
						if len(c.units) > 1 or c.base["K"] != n.base["K"]:
							raise TypeError("cannot convert complex temperature units")

						parser.temperature_rpn(n, "_°K_to_" + key)

			#subtract unit bases from base units and create convert string
			converts = ""
			for key in c.units:
				if key in c.base:
					c.base[key] -= c.units[key]
				else:
					converts += key
					if c.units[key] != 1:
						if caret:
							converts += "^"
						converts += c.units[key]
					if space:
						converts += " "

			#take difference from converts units
			if not tempconvert:
				n.magnitude /= c.magnitude
			for key in c.base:
				n.base[key] -= c.base[key]

		#create unit string
		for key in order:
			if n.base[key] != 0:
				s += key
				if n.base[key] != 1:
					if caret:
						s += "^"
					s += str(n.base[key])
				if space:
					s += " "

		magnitudestr = str(n.magnitude)
		unitstr = converts + s

		if scientific:
			mag = n.magnitude
			neg = mag < 0
			power = 0

			if neg:
				mag = -mag

			if mag >= 10:
				while mag >= 10:
					mag /= 10
					power += 1
			elif mag < 1:
				while mag < 1:
					mag *= 10
					power -= 1

			if neg:
				magnitudestr = "-"
			else:
				magnitudestr = ""
			magnitudestr += str(mag) + "E" + str(power)

		if printunits:
			magnitudestr += " " + unitstr.strip()

		return magnitudestr

	def __str__(self):
		return self.string()
