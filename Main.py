import re

CLASSES = {
    'i': "BigInteger",
    "s": "String",
    "f": "Double",
    "b": "Integer",
    "d": "LocalDate",
}


def getFildByName(name, rusText):
    fildName = ""
    if name[:1] == 'i':
        fildName = name
    else:
        fildName = name[1:]
    head = f"""
        @JsonProperty("{name}")
        @Column(name = "{name}")
        @ApiModelProperty(accessMode = ApiModelProperty.AccessMode.READ_ONLY,
            notes = "{rusText}")
        private {getClass(name)} {fildName};
"""
    return head


def getRussianString(line):
    reg = r"[№а-яА-Я]+[а-яА-Я,. :\-№()]+"
    match = re.search(reg, line)
    rez = match[0] if match else 'Not found'
    if getFildName(line)[:1] == "i":
        rez = "ID " + rez
    return rez


def getFildName(line):
    # удаляем Мишины: блаблабла.ХерМоржовый as бубликСраный
    reg = r".+[\s\t]as[\s\t]"
    match = re.search(reg, line)
    rez = ""
    if match:
        rez = line.replace(match[0], "")
    else:
        rez = line
    reg = r"^[a-zA-Z_.]+"
    match = re.search(reg, rez)
    rez = match[0] if match else 'Not found'
    match = re.search(r"[a-zA-z]+\.", rez)
    if match: rez = rez.replace(match[0], "")
    return rez.lower()


def getClass(fildName):
    bukva = fildName[:1]
    return CLASSES.get(bukva)


def getFilds(text):
    new_str = '\n'.join(el.strip() for el in text.split('\n') if el.strip())
    lines = new_str.split("\n")
    str = ""
    for i in lines:
        str += getFildByName(getFildName(i), getRussianString(i))
    return str

# getFilds("""""")
