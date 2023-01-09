import re

line = 'Код вида уведомления snoticetypemc string(254) mes_noticetype.smnemocode'
reg = r".+[\s\t]as[\s\t]"
match = re.search(reg, line)
rez = ""
if match:
    rez = rez.replace(match[0], "")
else:
    rez = line
reg = r"[a-zA-Z0-9_\.]+"
match = re.search(r'[a-zA-z0-9_]+\.', rez)

rez = match[0] if match else 'Not found'
print(rez)
match = re.search(r"[a-zA-z0-9_]+\.", rez)
if match: rez = rez.replace(match[0], "")
print(rez.lower())
