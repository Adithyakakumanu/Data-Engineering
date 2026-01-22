"""string functions:lower(),upper(),title(),strip(),lstrip(),rstrip(),replace("old","new"),split(),join(),find():return -1 if not found,index():error if not found,startswith(),endswith(),count(),isalpha(),isdigit(),isalnum(),isupper(),islower(),capitalize(),zfill():pads zeros on left"""
t="data Engineering"
print(t.lower())#data engineering
print(t.upper())#DATA ENGINEERING
print(t.title())#Data Engineering
d=" Data "
print(d.strip())
date="2024-01-10"
print(date.replace("-","/"))
print(date.split("-"))
v=["1","2","3"]
print("-".join(v))
print(t.find("engine"))
print(date.endswith("10"))
print(t.count())
print("123".isdigit())
print("abcde".isalpha())
print("123abc".isalnum())
print("DATA".isupper())
print("Data".islower())
print(t.capitalize())
id="45"
print(id.zfill(5)) #00045



