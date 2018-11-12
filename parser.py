from lex import Lex
from stringstream import StringStream
from token import Token, TokenType

import units

class Parser:
	decimaltype = TokenType.PERIOD

	errmsg = ""
	lex = None

	def __init__(self):
		self.errmsg = ""

	def parse(self, num, numstr):
		if numstr is None:
			return

		self.lex = Lex(StringStream(numstr))
		r = self._number()

		if not r:
			raise ValueError("invalid number (char " + str(self.lex.peekToken().character) + ", " + self.errmsg + "): " + numstr)

		tcount = 0
		for key in num.units:
			if key in units.temperaturemap:
				tcount += 1
		if tcount > 1:
			raise ValueError("too many temperature units: " + numstr)

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

	@staticmethod
	def unitParse(num, unitstr, power):
		prefix = ""
		prefixmult = 1
		i = 0
		triedprefix = None

		while i < len(unitstr):
			#triedprefix: if parsing with a prefix fails, try again without a prefix
			if triedprefix is None:
				#check if the unit has a prefix
				if i != len(unitstr) - 1 and unitstr[i] in units.prefixmap:
					prefix = unitstr[i]
					prefixmult = units.prefixmap[prefix]
					triedprefix = i
					i += 1
			else:
				prefixmult = 1
				i = triedprefix
				triedprefix = None

			#find longest matching unit in table
			j = len(unitstr)
			while i <= j and unitstr[i:j] not in units.unitmap:
				j -= 1

			#if unit found
			if i <= j:
				ustr = unitstr[i:j]
				multiplier, unitdict = units.unitmap[ustr]

				if ustr in units.temperaturemap:
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
				triedprefix = None
			else:
				if triedprefix is None:
					raise ValueError("unknown unit: " + unitstr[i:])

			i = j

def temperature_rpn(num, u):
	ustack = units.temperaturemap[u]
	curstack = []

	for e in ustack:
		if isinstance(e, str):
			if len(curstack) == 0:
				raise ValueError("unit conversion stack is empty for '" + u + "'")

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
				raise ValueError("invalid unit conversion operation for '" + u + "': " + e)
		else:
			curstack.append(e)

	if len(curstack) != 0:
		raise ValueError("temperature stack is not empty")
