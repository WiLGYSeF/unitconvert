from token import Token, TokenType

unitsymbols = ["°"]

class Lex:
	token_putback = None
	stream = None

	def __init__(self, stream):
		self.stream = stream

	def getToken(self):
		if self.token_putback is not None:
			token = self.token_putback
			self.token_putback = None
			return token

		return self.getNextToken()

	def ungetToken(self, token):
		if self.token_putback is not None:
			raise RuntimeError("ungetToken called more than once")

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

				return Token(TokenType.ICONST, s, self.stream.tell())
			if ch == ".":
				return Token(TokenType.PERIOD, "", self.stream.tell())
			if ch == ",":
				return Token(TokenType.COMMA, "", self.stream.tell())
			if self.isUnitChar(ch):
				if ch == "E" or ch == "e":
					if not self.stream.peek().isalpha():
						return Token(TokenType.ENOT, ch, self.stream.tell())

				s = ch
				while True:
					ch = self.stream.get()
					if ch is None:
						break
					if self.isUnitChar(ch):
						s += ch
					else:
						self.stream.unget()
						break

				return Token(TokenType.SCONST, s, self.stream.tell())

			return Token(TokenType.ERR, ch, self.stream.tell())
		return Token(TokenType.DONE, "", self.stream.tell())

	@staticmethod
	def isUnitChar(ch):
		return ch.isalpha() or ch in unitsymbols
