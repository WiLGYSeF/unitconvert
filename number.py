import math
import parser
import units

class Number:
	def __init__(self, num=None, prsr=None):
		self.magnitude = 0
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
		return self.copy().add(o)

	def add(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")

		self.magnitude += o.magnitude
		return self

	def __sub__(self, o):
		return self.copy().sub(o)

	def sub(self, o):
		if not isinstance(o, Number):
			raise TypeError("must be Number")
		if self.base != o.base:
			raise TypeError("units do not match")

		self.magnitude -= o.magnitude
		return self

	def __mul__(self, o):
		return self.copy().mul(o)

	def mul(self, o):
		if not isinstance(o, Number):
			self.magnitude *= o
			return self

		for key in self.base:
			self.base[key] += o.base[key]
		self.units.update(o.units)

		self.magnitude *= o.magnitude
		return self

	def __truediv__(self, o):
		return self.copy.div(o)

	def div(self, o):
		if not isinstance(o, Number):
			self.magnitude /= o
			return self

		for key in self.base:
			self.base[key] -= o.base[key]
		self.units.update(o.units)

		self.magnitude /= o.magnitude
		return self

	def pow_copy(self, o):
		return self.copy().pow(o)

	def pow(self, o):
		if isinstance(o, Number):
			raise TypeError("expected scalar unit")

		for key in self.base:
			self.base[key] *= o

		self.magnitude **= o
		return self

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

	def string(self, converts="", space=False, caret=False, scientific=False, printunits=True, sigfig=-1, roundnum=None):
		if sigfig >= 0 and roundnum is not None:
			raise ValueError("cannot round and express significant figures")

		order = ["kg", "m", "s", "K", "A", "mol", "cd"]
		s = ""
		tempconvert = False

		n = self

		#convert if converts option is not None
		if converts is not None:
			#if blank, automatically use units when Number was initialized
			if converts == "":
				for key in n.units:
					converts += key
					if n.units[key] != 0:
						converts += self.unitFloatToStr(n.units[key])
					converts += " "

			c = Number("1 " + converts)
			n = self.copy()

			#check if temperature needs to be converted (special case)
			for key in c.units:
				if key in units.temperaturemap:
					if key != "K":
						tempconvert = True
						#can only handle single-unit temperature conversions
						if len(c.units) > 1 or c.base["K"] != n.base["K"]:
							raise TypeError("cannot convert complex temperature units")

						parser.temperature_rpn(n, "_K_to_" + key)

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

			#take difference from convert units and magnitude
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
					s += self.unitFloatToStr(n.base[key])
				if space:
					s += " "

		magnitudestr = str(n.magnitude)
		if converts is None:
			unitstr = s
		else:
			unitstr = converts + s

		if roundnum is not None:
			n.magnitude = round(n.magnitude, roundnum)

		magnitudestr = self.floatToStr(n.magnitude, sigfig, scientific=scientific)

		if printunits:
			magnitudestr += " " + unitstr.strip()

		return magnitudestr

	def __str__(self):
		return self.string()

	@staticmethod
	def floatToStr(f, sigfig, scientific=False):
		fstr = str(f)

		if sigfig >= 0:
			# https://stackoverflow.com/a/3411435
			round_to_n = lambda x, n: round(x, -int(math.floor(math.log10(x))) + (n - 1))
			f = round_to_n(f, sigfig)
			fstr = str(f)

			hasdot = "." in fstr

			#fix up digits
			if (hasdot and len(fstr) - 1 != sigfig) or (not hasdot and len(fstr) != sigfig):
				if not hasdot:
					#add more zeros to fit sigfig
					fstr += "." + ("0" * (sigfig - len(fstr)))
				else:
					if len(fstr) - 1 > sigfig:
						#remove extra trailing ".0"
						fstr = fstr[:fstr.find(".")]
					else:
						#add more zeros to fit sigfig
						fstr += "0" * (sigfig - (len(fstr) - 1))

		if scientific:
			neg = f < 0
			power = 0

			if neg:
				f = -f

			#move decimal until 1 <= abs(number) < 10
			if f >= 10:
				while f >= 10:
					f /= 10
					power += 1
			elif f < 1:
				while f < 1:
					f *= 10
					power -= 1
			fstr = str(f)

			if neg:
				return "-" + fstr + "E" + str(power)
			return fstr + "E" + str(power)
		return fstr

	@staticmethod
	def unitFloatToStr(f):
		return format(f, ".15f").rstrip("0").rstrip(".")
