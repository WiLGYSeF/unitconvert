from lex import Lex
from stringstream import StringStream
from token import Token, TokenType

import units

class Parser:
	def __init__(self, system="metric"):
		self.decimaltype = TokenType.PERIOD
		self.system = system

		self.errmsg = ""
		self.lex = None

	def parse(self, numstr):
		if numstr is None:
			return

		self.lex = Lex(StringStream(numstr))
		r = self._number()

		if not r:
			raise NumberParseError("invalid number: " + self.errmsg + " (" + numstr + ")", {"char": self.lex.peekToken().character, "message": self.errmsg, "numstr": numstr})

		tcount = 0
		for key in r.units:
			if key in units.temperature_rpn:
				tcount += 1
		if tcount > 1:
			raise UnitParseError("too many temperature units: " + numstr)

		return r

	# <number> = <float> [ENOT] {SCONST [CARET] [<float>]}
	def _number(self):
		from number import Number

		num = Number()

		n = self._float()
		if n is None:
			return None

		num.magnitude = n

		token = self.lex.getToken()
		if token == TokenType.ENOT:
			n = self._float()
			if n is None:
				return None

			num.magnitude *= 10 ** n

		while True:
			if token is None or token == TokenType.DONE:
				break
			if token != TokenType.SCONST:
				self.lex.ungetToken(token)
				self.errmsg = "expected unit"
				return None

			stok = token
			token = self.lex.getToken()

			if token != TokenType.CARET:
				self.lex.ungetToken(token)

			power = 1
			n = self._float()
			if n is None:
				if token != TokenType.DONE and token != TokenType.SCONST:
					self.lex.ungetToken(token)
					self.errmsg = "expected number or unit"
					return None
			else:
				power = n

			self.unitParse(num, stok.lexeme, power)
			token = self.lex.getToken()

		return num

	"""
	if decimaltype is PERIOD
	<float> = [PLUS|MINUS] <integer> [PERIOD [ICONST]]
	<float> = [PLUS|MINUS] PERIOD ICONST

	if decimaltype is COMMA
	<float> = [PLUS|MINUS] <integer> [COMMA [ICONST]]
	<float> = [PLUS|MINUS] COMMA ICONST
	"""
	def _float(self):
		negative = 1
		n = 0

		token = self.lex.getToken()

		if token == TokenType.PLUS:
			pass
		elif token == TokenType.MINUS:
			negative = -1
		else:
			self.lex.ungetToken(token)

		n = self._integer()
		if n is not None:
			token = self.lex.getToken()
			if token == TokenType.PERIOD:
				token = self.lex.getToken()
				if token == TokenType.ICONST:
					return n + float("." + token.lexeme) * negative

				self.lex.ungetToken(token)
				return n * negative

			self.lex.ungetToken(token)
			return n * negative
		elif token == TokenType.PERIOD:
			token = self.lex.getToken()
			if token == TokenType.ICONST:
				return float("0." + token.lexeme) * negative

			self.lex.ungetToken(token)
			self.errmsg = "expected integer"
			return None

		self.errmsg = "expected number"
		return None

	"""
	if decimaltype is PERIOD
	<integer> = ICONST {COMMA ICONST}

	if decimaltype is COMMA
	<integer> = ICONST {PERIOD ICONST}

	"""
	def _integer(self):
		token = self.lex.getToken()
		value = 0

		if token != TokenType.ICONST:
			self.lex.ungetToken(token)
			self.errmsg = "expected integer constant"
			return None

		value = int(token.lexeme)

		while True:
			token = self.lex.getToken()
			if self.decimaltype == TokenType.PERIOD:
				if token == TokenType.COMMA:
					token = self.lex.getToken()
					if token != TokenType.ICONST:
						self.lex.ungetToken(token)
						self.errmsg = "expected integer constant"
						return None

					value = value * 10 ** len(token.lexeme) + int(token.lexeme)
				else:
					break
			elif self.decimaltype == TokenType.COMMA:
				if token == TokenType.PERIOD:
					token = self.lex.getToken()
					if token != TokenType.ICONST:
						self.lex.ungetToken(token)
						self.errmsg = "expected integer constant"
						return None

					value = value * 10 ** len(token.lexeme) + int(token.lexeme)
				else:
					break

		self.lex.ungetToken(token)
		return value

	def unitParse(self, num, unitstr, power):
		prefix = ""
		prefixmult = 1
		i = 0
		triedprefixidx = -1

		while i < len(unitstr):
			#triedprefix: if parsing with a prefix fails, try again without a prefix
			if triedprefixidx == -1:
				#check if the unit has a prefix
				if i != len(unitstr) - 1 and unitstr[i] in units.prefix_multipliers:
					prefix = unitstr[i]
					prefixmult = units.prefix_multipliers[prefix]
					triedprefixidx = i
					i += 1
			else:
				prefix = ""
				prefixmult = 1
				i = triedprefixidx
				triedprefixidx = -1

			#find longest matching unit in table
			uresult = None
			j = len(unitstr)
			while i <= j:
				uresult = self.getUnit(unitstr[i:j])
				if uresult is not None:
					break
				j -= 1

			if uresult is not None:
				ustr = unitstr[i:j]
				multiplier, _, unitdict = uresult

				if ustr in units.temperature_rpn:
					temperature_rpn(num, ustr)

				#power only applies to last unit if unitstr contains multiple units

				if j == len(unitstr):
					num.magnitude *= multiplier ** power * prefixmult

					for key in unitdict:
						num.base[key] += unitdict[key] * power
				else:
					num.magnitude *= multiplier * prefixmult

					for key in unitdict:
						num.base[key] += unitdict[key]

				ustr = prefix + ustr
				if ustr in num.units:
					if j == len(unitstr):
						num.units[ustr] += power
					else:
						num.units[ustr] += 1
				else:
					if j == len(unitstr):
						num.units[ustr] = power
					else:
						num.units[ustr] = 1

				prefix = ""
				prefixmult = 1
				triedprefixidx = -1
			else:
				if triedprefixidx == -1:
					raise UnitParseError("unknown unit: " + unitstr[i:], {"unit": unitstr[i:]})

			i = j

	def getUnit(self, u):
		if self.system == "metric":
			if u in units.metric_units:
				return units.metric_units[u]
			if u in units.metric_customary_units:
				return units.metric_customary_units[u]
			return None
		if self.system == "customary" or self.system == "customary_dry" or self.system == "customary_wet":
			if u in units.customary_units:
				return units.customary_units[u]
			if u in units.metric_customary_units:
				return units.metric_customary_units[u]

			if self.system == "customary_dry":
				if u in units.customary_dry_units:
					return units.customary_dry_units[u]
				if u in units.customary_wet_units:
					return units.customary_wet_units[u]
			else:
				if u in units.customary_wet_units:
					return units.customary_wet_units[u]
				if u in units.customary_dry_units:
					return units.customary_dry_units[u]

			return None

		raise ValueError("unknown measurement system: " + self.system)

def temperature_rpn(num, u):
	ustack = units.temperature_rpn[u]
	curstack = []

	for e in ustack:
		if isinstance(e, str):
			if len(curstack) == 0:
				raise UnitParseError("unit conversion stack is empty for '" + u + "'", {"unit": u})

			if e == "+":
				num.magnitude += curstack.pop()
			elif e == "-":
				num.magnitude -= curstack.pop()
			elif e == "*":
				num.magnitude *= curstack.pop()
			elif e == "/":
				num.magnitude /= curstack.pop()
			elif e == "^":
				num.magnitude **= curstack.pop()
			else:
				raise UnitParseError("invalid unit conversion operation for '" + u + "': " + e, {"unit": u})
		else:
			curstack.append(e)

	if len(curstack) != 0:
		raise UnitParseError("temperature stack is not empty", {"unit": u})

class NumberParseError(Exception):
	def __init__(self, message, status={}):
		super().__init__(message)

		self.status = status

class UnitParseError(Exception):
	def __init__(self, message, status={}):
		super().__init__(message)

		self.status = status
