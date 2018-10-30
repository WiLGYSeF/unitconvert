import units
from enum import Enum
from stringstream import StringStream

class Parser:
	tokenlist = []
	offset = 0
	offsetstore = []

	def __init__(self, num, numstr=None):
		if numstr is None:
			return
		if not self.parse(num, numstr):
			raise ValueError("invalid number: " + numstr)

	def parse(self, num, numstr):
		self.tokenlist = []
		self.offset = 0
		self.offsetstore = []

		stream = StringStream(numstr)
		token = Token(TokenType.PLUS) #throwaway

		while token != TokenType.DONE and token != TokenType.ERR:
			token = self.lex(stream)
			self.tokenlist.append(token)

		for e in self.tokenlist:
			print(e)

		return self._number(num)

	# <number> = <float> [ENOT] {SCONST [CARET] [<float>]}
	def _number(self, num):
		n = self._float()
		if n is None:
			return False

		num.magnitude = n

		token = self._getToken()
		if token == TokenType.ENOT:
			n = self._float()
			if n is None:
				return False

			num.magnitude *= 10 ** n

		while True:
			if token is None or token == TokenType.DONE:
				break
			if token != TokenType.SCONST:
				return False

			stok = token
			token = self._getToken()
			if token.tokentype != TokenType.CARET:
				self._ungetToken()

			power = 1
			n = self._float()
			if n is not None:
				power = n

			self.unitParse(num, stok.lexeme, power)
			token = self._getToken()

		return True

	# <float> = [PLUS|MINUS] ICONST [PERIOD [ICONST]]
	# <float> = [PLUS|MINUS] PERIOD ICONST
	def _float(self):
		self._storeOffset()
		negative = 1
		n = 0

		token = self._getToken()

		if token == TokenType.PLUS:
			token = self._getToken()
		elif token == TokenType.MINUS:
			negative = -1
			token = self._getToken()

		if token == TokenType.ICONST:
			wpart = token.lexeme

			token = self._getToken()
			if token == TokenType.PERIOD:
				token = self._getToken()
				if token == TokenType.ICONST:
					return float(wpart + "." + token.lexeme) * negative

				self._loadOffset()
				return None

			self._ungetToken()
			return int(wpart) * negative
		elif token == TokenType.PERIOD:
			token = self._getToken()
			if token == TokenType.ICONST:
				return float("0." + token.lexeme) * negative

			self._loadOffset()
			return None

		self._loadOffset()
		return None

	def unitParse(self, num, unitstr, power):
		prefix = ""
		prefixmult = 1
		i = 0
		triedprefix = None

		while i < len(unitstr):
			#triedprefix: if parsing with a prefix fails, try again without a prefix
			if triedprefix is None:
				if i != len(unitstr) - 1 and unitstr[i] in units.prefixmap:
					prefix = unitstr[i]
					prefixmult = units.prefixmap[prefix]
					triedprefix = i
					i += 1
			else:
				prefixmult = 1
				i = triedprefix
				triedprefix = None

			j = len(unitstr)
			while i <= j and unitstr[i:j] not in units.unitmap:
				j -= 1

			if i <= j:
				ustr = unitstr[i:j]
				multiplier, unitdict = units.unitmap[ustr]

				if j == len(unitstr):
					num.magnitude *= multiplier ** power * prefixmult
				else:
					num.magnitude *= multiplier * prefixmult

				for key in unitdict:
					if j == len(unitstr):
						num.base[key] += unitdict[key] * power
					else:
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

	def lex(self, stream):
		while True:
			ch = stream.get()
			if ch is None:
				break

			if ch == " " or ch == "\t":
				continue
			if ch == "+":
				return Token(TokenType.PLUS)
			if ch == "-":
				return Token(TokenType.MINUS)
			if ch == "^":
				return Token(TokenType.CARET)
			if ch.isdigit():
				s = ch
				while True:
					ch = stream.get()
					if ch is None:
						break
					if ch.isdigit():
						s += ch
					else:
						stream.unget()
						break

				return Token(TokenType.ICONST, s)
			if ch == ".":
				return Token(TokenType.PERIOD)
			if ch == ",":
				return Token(TokenType.COMMA)
			if ch == "E" or ch == "e":
				if stream.peek().isalpha():
					stream.unget()
				else:
					return Token(TokenType.ENOT, ch)
			if ch.isalpha():
				s = ch
				while True:
					ch = stream.get()
					if ch is None:
						break
					if ch.isalpha():
						s += ch
					else:
						stream.unget()
						break

				return Token(TokenType.SCONST, s)

			return Token(TokenType.ERR, ch)
		return Token(TokenType.DONE)

	def _getToken(self):
		if self.offset == len(self.tokenlist):
			return None
		t = self.tokenlist[self.offset]
		self.offset += 1
		return t

	def _ungetToken(self):
		if self.offset == 0:
			return
		self.offset -= 1

	def _loadOffset(self):
		if len(self.offsetstore) == 0:
			return
		self.offset = self.offsetstore.pop()

	def _storeOffset(self):
		self.offsetstore.append(self.offset)

class Token:
	tokentype = None
	lexeme = ""

	def __init__(self, tokentype, lexeme=""):
		self.tokentype = tokentype
		self.lexeme = lexeme

	def __eq__(self, o):
		if isinstance(o, Token):
			return self.tokentype == o.tokentype and self.lexeme == o.lexeme
		return self.tokentype == o

	def __str__(self):
		s = str(self.tokentype)
		if len(self.lexeme) != 0:
			s += " (" + self.lexeme + ")"
		return s

class TokenType(Enum):
	PLUS = "PLUS"
	MINUS = "MINUS"
	ICONST = "ICONST"
	PERIOD = "PERIOD"
	COMMA = "COMMA"
	ENOT = "ENOT"
	SCONST = "SCONST"
	CARET = "CARET"
	DONE = "DONE"
	ERR = "ERR"

	#def _generate_next_value_(name, start, count, last_values):
	#    return name
