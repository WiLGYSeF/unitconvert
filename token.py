from enum import Enum

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
