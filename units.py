# http://www.us-metric.org/detailed-list-of-metric-system-units-symbols-and-prefixes/

unitmap = {
	"g":		(0.001,			"gram",			{"kg": 1}),
	"m":		(1,				"meter",		{"m": 1}),
	"s":		(1,				"second",		{"s": 1}),
	"A":		(1,				"ampere",		{"A": 1}),
	"K":		(1,				"kelvin",		{"K": 1}),
	"mol":		(1,				"mole",			{"mol": 1}),
	"cd":		(1,				"candela",		{"cd": 1}),

	"F":		(1,				"farad",		{"s": 4, "A": 2, "m": -2, "kg": -1}),
	"C":		(1,				"coulomb",		{"A": 1, "s": 1}),
	"V":		(1,				"volt",			{"kg": 1, "m": 2, "s": -3, "A": -1}),
	"Ω":		(1,				"ohm",			{"kg": 1, "m": 2, "s":-3, "A": -2}),
	"J":		(1,				"joule",		{"kg": 1, "m": 2, "s": -2}),
	"N":		(1,				"newton",		{"kg": 1, "m": 1, "s": -2}),
	"Hz":		(1,				"hertz",		{"s": -1}),
	"lx":		(1,				"lux",			{"cd": 1, "m": -2}),
	"lm":		(1,				"lumen",		{"cd": 1}),
	"Wb":		(1,				"weber",		{"V": 1, "s": 1}),
	"T":		(1,				"tesla",		{"V": 1, "s": 1, "m": -2}),
	"W":		(1,				"watt",			{"J": 1, "s": -1}),
	"Pa":		(1,				"pascal",		{"N": 1, "m": -2}),
	"Bq":		(1,				"becquerel",	{"s": -1}),
	"Gy":		(1,				"gray",			{"J": 1, "kg": -1}),
	"Sv":		(1,				"sievert",		{"J": 1, "kg": -1}),
	"kat":		(1,				"katal",		{"mol": 1, "s": -1}),

	"min":		(60,			"minute",		{"s": 1}),
	"h":		(3600,			"hour",			{"s": 1}),
	"d":		(86400,			"day",			{"s": 1}),

	"ha":		(10000,			"hectare",		{"m": 2}),
	"L":		(0.001,			"litre",		{"m": 3}),
	"t":		(1000,			"ton",			{"kg": 1}),

	"bar":		(100000,		"bar",			{"N": 1, "m": -2}),
	"Ci":		(3.7 * 10**10,	"curie",		{"s": -1}),
	"R":		(2.58 * 10**-4,	"roentgen",		{"A": 1, "s": 1, "kg": -1}),
	"rd":		(0.01,			"rad",			{"J": 1, "kg": -1}),
	"rem":		(0.01,			"rem",			{"J": 1, "kg": -1}),

	#handled elsewhere
	"°F":		(1,				"fahrenheit",	{"K": 1}),
	"°C":		(1,				"celsius",		{"K": 1})
}

# https://en.wikipedia.org/wiki/United_States_customary_units

customaryunitmap = {
	"in":		(0.0254,		"inch",			{"m": 1}),
	"ft":		(0.3048,		"foot",			{"m": 1}),
	"yd":		(0.9144,		"yard",			{"m": 1}),
	"mi":		(1609.344,		"mile",			{"m": 1}),

	"li":		(0.201168,		"link",			{"m": 1}),
	"rd":		(5.029,			"rod",			{"m": 1}),
	"ch":		(20.116,		"chain",		{"m": 1}),
	"fur":		(201.168,		"furlong",		{"m": 1}),
	"lea":		(4828,			"league",		{"m": 1}),
	"ftm":		(1.8288,		"fathom",		{"m": 1}),
	"cb":		(219.456,		"cable",		{"m": 1}),
	"nmi":		(1852,			"nautical mile",{"m": 1}),

	"acre":		(4046.873,		"acre",			{"m": 2}),
	"section":	(2589998,		"section",		{"m": 2}),
	"twp":		(93239930,		"township",		{"m": 2}),

	"Btu":		(1055,			"British thermal unit", {"J": 1}),
	"cal":		(4.184,			"calorie",		{"J": 1}),
	"kcal":		(4184,			"kilocalorie",	{"J": 1}),
	"ft-lbf":	(1.356,			"foot-pound",	{"J": 1}),
	"hp":		(745.7,			"horsepower",	{"J": 1, "s": -1}),
	"slug":		(14.5939,		"slug",			{"kg": 1}),
	"psi":		(6894.76,		"pound-per-square-inch", {"N": 1, "m": -2})
}

avoirdupoismap = {
	"gr":		(64798.91,		"grain",		{"kg": 1}),
	"dr":		(0.001771845,	"dram",			{"kg": 1}),
	"oz":		(0.028349523,	"ounce",		{"kg": 1}),
	"lb":		(0.45359237,	"pound",		{"kg": 1}),
	"cwt":		(45.359237,		"hundredweight",{"kg": 1}),
	"ton":		(907.18474,		"ton",			{"kg": 1})
}

troymap = {
	"gr":		(64798.91,		"grain",		{"kg": 1}),
	"dwt":		(0.001555173,	"pennyweight",	{"kg": 1})
}

#rpn stack, front is 0
temperaturemap = {
	"°F": [32, "-", 5, "*", 9, "/", 273.15, "+"],
	"°C": [273.15, "+"],
	"_K_to_°C": [273.15, "-"],
	"_K_to_°F": [273.15, "-", 9, "*", 5, "/", 32, "+"]
}

prefixmap = {
	"Y": 10**24,
	"Z": 10**21,
	"E": 10**18,
	"P": 10**15,
	"T": 10**12,
	"G": 10**9,
	"M": 10**6,
	"k": 10**3,
	"h": 10**2,
	"da": 10**1,
	"d": 10**-1,
	"c": 10**-2,
	"m": 10**-3,
	"µ": 10**-6,
	"n": 10**-9,
	"p": 10**-12,
	"f": 10**-15,
	"a": 10**-18,
	"z": 10**-21,
	"y": 10**-24
}
