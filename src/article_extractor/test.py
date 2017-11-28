import pycountry

isocode = pycountry.countries.get(name="Russia").alpha_2
print isocode
