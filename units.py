# http://www.us-metric.org/detailed-list-of-metric-system-units-symbols-and-prefixes/

metricbase = ("kg", "m", "s", "K", "A", "mol", "cd")

metric_units = {
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
	"Wb":		(1,				"weber",		{"kg": 1, "m": 2, "s": -2, "A": -1}),
	"T":		(1,				"tesla",		{"kg": 1, "s": -2, "A": -1}),
	"W":		(1,				"watt",			{"kg": 1, "m": 2, "s": -3}),
	"Pa":		(1,				"pascal",		{"kg": 1, "m": -1, "s": -2}),
	"Bq":		(1,				"becquerel",	{"s": -1}),
	"Gy":		(1,				"gray",			{"m": 2, "s": -2}),
	"Sv":		(1,				"sievert",		{"m": 2, "s": -2}),
	"kat":		(1,				"katal",		{"mol": 1, "s": -1}),

	"ha":		(10000,			"hectare",		{"m": 2}),
	"L":		(0.001,			"litre",		{"m": 3}),
	"t":		(1000,			"ton",			{"kg": 1}),

	"bar":		(100000,		"bar",			{"kg": 1, "m": -1, "s": -2}),
	"Ci":		(3.7 * 10**10,	"curie",		{"s": -1}),
	"R":		(2.58 * 10**-4,	"roentgen",		{"A": 1, "s": 1, "kg": -1}),
	"rd":		(0.01,			"rad",			{"m": 2, "s": -2}),
	"rem":		(0.01,			"rem",			{"m": 2, "s": -2})
}

metric_customary_units = {
	"min":		(60,			"minute",		{"s": 1}),
	"h":		(3600,			"hour",			{"s": 1}),
	"hr":		(3600,			"hour",			{"s": 1}),
	"d":		(86400,			"day",			{"s": 1}),

	#handled elsewhere
	"°F":		(1,				"fahrenheit",	{"K": 1}),
	"°C":		(1,				"celsius",		{"K": 1})
}

# https://en.wikipedia.org/wiki/United_States_customary_units

customary_units = {
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

	"Btu":		(1055,			"British thermal unit", {"kg": 1, "m": 2, "s": -2}),
	"cal":		(4.184,			"calorie",		{"kg": 1, "m": 2, "s": -2}),
	"kcal":		(4184,			"kilocalorie",	{"kg": 1, "m": 2, "s": -2}),
	"ft-lbf":	(1.356,			"foot-pound",	{"kg": 1, "m": 2, "s": -2}),
	"Wh":		(3600,			"watt-hour",	{"kg": 1, "m": 2, "s": -2}),

	"hp":		(745.7,			"horsepower",	{"kg": 1, "m": 2, "s": -3}),

	"slug":		(14.5939,		"slug",			{"kg": 1}),

	"psi":		(6894.76,		"pound-per-square-inch", {"kg": 1, "m": -1, "s": -2}),
	"psf":		(47.88,			"pound-per-square-foot", {"kg": 1, "m": -1, "s": -2}),
	"atm":		(101.325,		"atmosphere",	{"kg": 1, "m": -1, "s": -2})
}

customary_dry_units = {
	"pt":		(0.550610471*10**-3, "pint", {"m": 3}),
	"qt":		(0.001101221, "quart", {"m": 3}),
	"gal":		(0.004404884, "gallon", {"m": 3}),
	"pk":		(0.008809768, "peck", {"m": 3}),
	"bu":		(0.035239070, "bushel", {"m": 3}),
	"bbl":		(0.1156271, "barrel", {"m": 3}),
}

customary_wet_units = {
	#"min":	(),
	"fl dr":	(3.696691195*10**-6, "fluid dram", {"m": 3}),
	"tsp":		(4.928921593*10**-6, "teaspoon", {"m": 3}),
	"tbsp":		(14.786764781*10**-6, "tablespoon", {"m": 3}),
	"fl oz":	(29.573529*10**-6, "fluid ounce", {"m": 3}),
	"jig":		(44.360294*10**-6, "shot", {"m": 3}),
	"gi":		(118.29411*10**-6, "gill", {"m": 3}),
	"cp":		(236.58823*10**-6, "cup", {"m": 3}),
	"pt":		(473.17647*10**-6, "pint", {"m": 3}),
	"qt":		(0.9463529*10**-3, "quart", {"m": 3}),
	"gal":		(3.7854117*10**-3, "gallon", {"m": 3}),
	"bbl":		(0.11924047, "barrel", {"m": 3})
}

customary_possibleprefix = {
	"fl": ["dr", "oz"],
	"short": ["ton"],
	"long": ["hundredweight", "ton"],
	"t": ["oz", "lb"]
}

avoirdupois_units = {
	"gr":		(64.7989*10**-5, "grain",		{"kg": 1}),
	"dr":		(0.001771845,	"dram",			{"kg": 1}),
	"oz":		(0.028349523,	"ounce",		{"kg": 1}),
	"lb":		(0.45359237,	"pound",		{"kg": 1}),
	"cwt":		(45.359237,		"hundredweight", {"kg": 1}),
	"long hundredweight": (50.802345, "long hundredweight",{"kg": 1}),
	"ton":		(907.18474,		"ton",			{"kg": 1}),
	"short ton": (907.18474, "short ton", {"kg": 1}),
	"long ton": (1016.0469, "long ton", {"kg": 1})
}

troy_units = {
	"gr":		(64.7989*10**-5,"grain",		{"kg": 1}),
	"dwt":		(0.001555173,	"pennyweight",	{"kg": 1}),
	"oz":		(0.031103476,	"troy ounce",	{"kg": 1}),
	#also "oz t", but cannot handle
	"t oz":		(0.031103476,	"troy ounce",	{"kg": 1}),
	"lb":		(0.373241721,	"troy pound",	{"kg": 1}),
	#also "lb t", but cannot handle
	"t lb":		(0.373241721,	"troy pound",	{"kg": 1})
}

#rpn stack, front is 0
temperature_rpn = {
	"°F": (32, "-", 5, "*", 9, "/", 273.15, "+"),
	"°C": (273.15, "+"),
	"_K_to_°C": (273.15, "-"),
	"_K_to_°F": (273.15, "-", 9, "*", 5, "/", 32, "+")
}

prefix_multipliers = {
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

prefix_multipliers_name = {
	"Y": "yotta",
	"Z": "zetta",
	"E": "exa",
	"P": "peta",
	"T": "tera",
	"G": "giga",
	"M": "mega",
	"k": "kilo",
	"h": "hecto",
	"da": "deca",
	"d": "deci",
	"c": "centi",
	"m": "milli",
	"µ": "micro",
	"n": "nano",
	"p": "pico",
	"f": "femto",
	"a": "atto",
	"z": "zepto",
	"y": "yocto"
}

def sanitycheck(unitmap):
	for key in unitmap:
		magnitude, name, units = unitmap[key]
		if magnitude < 0:
			raise ValueError("sanitycheck: magnitude less than zero: " + key)
		if name is None or len(name) == 0:
			raise ValueError("sanitycheck: name blank: " + key)
		for uk in units:
			if uk not in metricbase:
				raise ValueError("sanitycheck: unit is not si base: " + key + " (" + uk + ")")

def sanitycheck_defaults():
	maps = (metric_units, metric_customary_units, customary_units, customary_dry_units, customary_wet_units, avoirdupois_units, troy_units)
	for m in maps:
		sanitycheck(m)
