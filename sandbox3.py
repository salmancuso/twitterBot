import re

testString = """This * ( the new Begnning (#(#($*!($@*!$)._>"""

testString = re.sub('[^A-Za-z0-9]+', '', testString)

print testString