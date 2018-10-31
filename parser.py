from lex import Lex
from stringstream import StringStream
from token import Token, TokenType

import units

#temporary global variable
errmsg = ""

def parse(num, numstr):
	if numstr is None:
		return

	lex = Lex(StringStream(numstr))
	r = _number(lex)

	if not r:
		raise ValueError("invalid number (char " + str(lex.peekToken().character) + ", " + errmsg + "): " + numstr)
	return r

# <number> = <float> [ENOT] {SCONST [CARET] [<float>]}
def _number(lex):
	from number import Number

	global errmsg

	num = Number()

	n = _float(lex)
	if n is None:
		return None

	num.magnitude = n

	token = lex.getToken()
	if token == TokenType.ENOT:
		n = _float(lex)
		if n is None:
			return None

		num.magnitude *= 10 ** n

	while True:
		if token is None or token == TokenType.DONE:
			break
		if token != TokenType.SCONST:
			lex.ungetToken(token)
			errmsg = "expected unit"
			return None

		stok = token
		token = lex.getToken()

		if token.tokentype != TokenType.CARET:
			lex.ungetToken(token)

		power = 1
		n = _float(lex)
		if n is None:
			if token.tokentype != TokenType.DONE and token.tokentype != TokenType.SCONST:
				errmsg = "expected number"
				return None
		else:
			power = n

		unitParse(num, stok.lexeme, power)
		token = lex.getToken()

	return num

# <float> = [PLUS|MINUS] ICONST [PERIOD [ICONST]]
# <float> = [PLUS|MINUS] PERIOD ICONST
def _float(lex):
	global errmsg

	negative = 1
	n = 0

	token = lex.getToken()

	if token == TokenType.PLUS:
		token = lex.getToken()
	elif token == TokenType.MINUS:
		negative = -1
		token = lex.getToken()

	if token == TokenType.ICONST:
		wpart = token.lexeme

		token = lex.getToken()
		if token == TokenType.PERIOD:
			token = lex.getToken()
			if token == TokenType.ICONST:
				return float(wpart + "." + token.lexeme) * negative

			lex.ungetToken(token)
			return int(wpart) * negative

		lex.ungetToken(token)
		return int(wpart) * negative
	elif token == TokenType.PERIOD:
		token = lex.getToken()
		if token == TokenType.ICONST:
			return float("0." + token.lexeme) * negative

		lex.ungetToken(token)
		errmsg = "expected integer"
		return None

	lex.ungetToken(token)
	errmsg = "expected number"
	return None

def unitParse( num, unitstr, power):
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
