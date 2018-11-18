from token import Token, TokenType

start_unitsymbols = ["°"]
middle_unitsymbols = ["-"]
end_unitsymbols = []

class Lex:
	def __init__(self, stream):
		self.stream = stream
		self.token_putback = None

	def getToken(self):
		if self.token_putback is not None:
			token = self.token_putback
			self.token_putback = None
			return token

		return self.getNextToken()

	def ungetToken(self, token):
		# maintain efficiency O(n)
		if self.token_putback is not None:
			raise RuntimeError("fatal: ungetToken() called more than once")

		self.token_putback = token

	def peekToken(self):
		if self.token_putback is not None:
			return self.token_putback

		token = self.getToken()
		self.ungetToken(token)
		return token

	def getNextToken(self):
		while True:
			ch = self.stream.get()
			if ch is None:
				break

			if ch == " " or ch == "\t":
				continue
			if ch == "+":
				return Token(TokenType.PLUS, "", self.stream.tell())
			if ch == "-":
				return Token(TokenType.MINUS, "", self.stream.tell())
			if ch == "^":
				return Token(TokenType.CARET, "", self.stream.tell())
			if ch.isdigit():
				char = self.stream.tell()
				s = ch

				while True:
					ch = self.stream.get()
					if ch is None:
						break
					if ch.isdigit():
						s += ch
					else:
						self.stream.unget()
						break

				return Token(TokenType.ICONST, s, char)
			if ch == ".":
				return Token(TokenType.PERIOD, "", self.stream.tell())
			if ch == ",":
				return Token(TokenType.COMMA, "", self.stream.tell())
			if self.isStartUnitChar(ch):
				if ch == "E" or ch == "e":
					peek = self.stream.peek()
					if peek is not None and not peek.isalpha():
						return Token(TokenType.ENOT, ch, self.stream.tell())

				char = self.stream.tell()
				s = ch

				while True:
					ch = self.stream.get()
					if ch is None:
						if not self.isEndUnitChar(s[-1]):
							s = s[:-1]
							self.stream.unget()
						break

					if self.isUnitChar(ch):
						s += ch
					else:
						if not self.isEndUnitChar(s[-1]):
							s = s[:-1]
							self.stream.unget()
						self.stream.unget()
						break

				return Token(TokenType.SCONST, s, char)

			return Token(TokenType.ERR, ch, self.stream.tell())
		return Token(TokenType.DONE, "", self.stream.tell())

	@staticmethod
	def isStartUnitChar(ch):
		return ch.isalpha() or ch in start_unitsymbols

	@staticmethod
	def isUnitChar(ch):
		return ch.isalpha() or ch in start_unitsymbols or ch in middle_unitsymbols or ch in end_unitsymbols

	@staticmethod
	def isEndUnitChar(ch):
		return ch.isalpha() or ch in end_unitsymbols
