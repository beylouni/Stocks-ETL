import re

text = '3R Petroleum Oleo E Gas Sa (RRRP3)'

print(re.findall(r'\((.*?)\)', text)[0])
print(re.sub(r'\((.*?)\)', '', text))
