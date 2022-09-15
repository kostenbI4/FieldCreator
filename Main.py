import re

CLASSES = {
    'i': "BigInteger",
    "s": "String",
    "f": "Double",
    "b": "Integer",
    "n": "Integer",
    "d": "LocalDate",
    "t": "LocalTime"
}


def getFildByName(name, rusText):
    fildName = ""
    if name[:1] == 'i':
        fildName = name
    else:
        fildName = name[1:]
    head = f"""
        @JsonProperty(value = "{name}", access = JsonProperty.Access.READ_ONLY)
        @Column(name = "{name}")
        @ApiModelProperty(notes = "{rusText}")
        private {getClass(name)} {fildName};
"""
    return head


def getFildForReport(name, rusText):
    fildName = ""
    if name[:1] == 'i':
        fildName = name
    else:
        fildName = name[1:]
    head = f"""
        //{rusText}
        @Column(name = "{name}")        
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
    reg = r"^[a-zA-Z0-9_.]+"
    match = re.search(reg, rez)
    rez = match[0] if match else 'Not found'
    match = re.search(r"[a-zA-z0-9_]+\.", rez)
    if match: rez = rez.replace(match[0], "")
    return rez.lower()


def getClass(fildName):
    bukva = fildName[:1]
    return CLASSES.get(bukva)


def getFilds(text):
    new_str = '\n'.join(el.strip() for el in text.split('\n') if el.strip())
    lines = new_str.split("\n")
    str = ""
    schForTable = 1  # Счетчик строк для варианта с маркдауном
    MDFildName = ""
    MDRusString = ""
    match = re.search(r".+\s.+", lines[0])
    if match:
        for i in lines:
            str += getFildByName(getFildName(i), getRussianString(i))
        return str
    else:
        for i in lines:
            if schForTable == 1:
                MDFildName = getFildName(i)
                schForTable += 1
            elif schForTable == 2:
                schForTable += 1
            else:
                MDRusString = i
                print("rs: ", i)
                str += getFildByName(MDFildName, MDRusString)
                schForTable = 1
                MDFildName = ""
                MDRusString = ""
        return str


def getReportFilds(text):
    new_str = '\n'.join(el.strip() for el in text.split('\n') if el.strip())
    lines = new_str.split("\n")
    str = ""
    schForTable = 1  # Счетчик строк для варианта с маркдауном
    MDFildName = ""
    match = re.search(r".+\s.+", lines[0])
    if match:
        for i in lines:
            str += getFildForReport(getFildName(i), getRussianString(i))
        return str
    else:
        for i in lines:
            if schForTable == 1:
                MDFildName = getFildName(i)
                schForTable += 1
            elif schForTable == 2:
                schForTable += 1
            else:
                MDRusString = i
                str += getFildForReport(MDFildName, MDRusString)
                schForTable = 1
                MDFildName = ""
        return str