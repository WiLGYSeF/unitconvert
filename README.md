# unitconvert

## **This project was an old coding exercise and is no longer maintained**

Python module for converting units and performing basic arithmetic operations.
This is a proof-of-concept project, and was written to practice parsing.
You probably shouldn't use it in any real-world projects.
It has not been written to ensure precision, but rather made for simplicity.

# Installing the Module
To install the module for importing into other scripts, you can put the files in a directory called unitconvert in one of these paths:
```
~/.local/lib/python3.6/site-packages/
/usr/local/lib/python3.6/dist-packages/
/usr/lib/python3/dist-packages/
```
To import it into a script:
```python
from unitconvert.number import Number
from unitconvert.parser import Parser

num = Number("74 m/s")
```

# Examples
### Converting Numbers
####Converting with metric:
```python
num = Number("115 cm/s")
print(num.string(converts="m/s", roundnum=4)) #1.15 m s-1

num = Number("12 N")
print(num.string(converts="kg")) #12.0 kg m s-2

num = Number("17.8 kg m s-2")
print(num.string(converts="N")) #17.8 N

num = Number("23 kg/s^2")
print(num.string(converts="N")) #23.0 N m-1
```

####Converting with customary:
```python
prsr = parser.Parser(system="customary")

num = Number("115 ft", prsr)
print(num.string(converts="m", roundnum=4)) #35.052 m

num = Number("6341 lb/ft⋅s2", prsr=prsr)
print(num.string(converts="psi", sigfig=4, prsr=prsr)) #1.369 psi

num = Number("2 cp", prsr)
print(num.string(converts="cm3")) #473.17646 cm3
```

### Parser Systems
 - metric
 - customary (can specify subset systems, ex: customary_troy, customary_dry_troy)
   - dry
   - wet
   - avoirdupois
   - troy

Default systems: metric (default), customary_wet_avoirdupois

### Arithmetic
This module makes sure that numbers can only be added, multiplied, etc. with proper units.
Adding `7 kg` and `30 cm` will raise a TypeError exception.

```python
Number("1 m") + Number("27 cm") #1.27 m

num = Number("1 m")

# add to copy of num
newnum = num + Number("27 cm")

# add to num object
num.add(Number("27 cm"))

print((Number("7 kg") * Number("30 cm")).string(converts="kg m")) #2.1 kg m
```

### Comparison

```python
print(Number("1.3 m") > Number("140 cm")) #False
print(Number("1 m") > Number("3 ft", prsr=Parser(system="customary"))) #True
```
