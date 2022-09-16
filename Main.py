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

CLASSESFORFILTER = {
    "BigInteger": "numeric",
    "String": "string",
    "Integer": "numeric",
    "LocalDate": "date",
    "LocalTime": "date",
    "Double": "numeric",
}

JASPERCLASSES = {
    'i': "java.math.BigInteger",
    "s": "java.lang.String",
    "f": "java.lang.Double",
    "b": "java.lang.Integer",
    "n": "java.lang.Integer",
    "d": "java.time.LocalDate",
    "t": "java.time.LocalTime"
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


def getFildForFilter(name, rusText):
    fildName = ""
    if name[:1] == 'i':
        fildName = name
    else:
        fildName = name[1:]
    head = f'{{"name": "{name}", "datatype": "{getClassFilter(name)}", "operator": null, "val": null}} {rusText} <hr>' + "\\\n"
    return head


def getFildForJasper(list):
    fildName = list[2].strip().split(" ")[-1:][0][:-1]
    fildForClassName = list[1].strip()
    match = re.findall(r'"(.*)"', fildForClassName)[0]
    head = f"""
<field name="{fildName}" class="{getJasperClass(match)}"/>
"""
    return head


def getRussianString(line):
    reg = r"[№а-яА-Я]+[а-яА-Я,. :\-№()]+"
    match = re.search(reg, line)
    rez = match[0] if match else 'Not found'
    if getFildName(line)[:1] == "i":
        rez = "ID " + rez
    return rez


def getJavaName(line):
    fildName = getFildName(line)
    return re.findall(fildName, line, re.IGNORECASE)[-1:]


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


def getClassFilter(fildName):
    className = getClass(fildName)
    return CLASSESFORFILTER.get(className)


def getJasperClass(fildName):
    bukva = fildName[:1]
    return JASPERCLASSES.get(bukva)


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


def getFiltersFilds(text):
    new_str = '\n'.join(el.strip() for el in text.split('\n') if el.strip())
    lines = new_str.split("\n")
    str = ""
    schForTable = 1  # Счетчик строк для варианта с маркдауном
    MDFildName = ""
    match = re.search(r".+\s.+", lines[0])
    if match:
        for i in lines:
            str += getFildForFilter(getFildName(i), getRussianString(i))
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
                str += getFildForFilter(MDFildName, MDRusString)
                schForTable = 1
                MDFildName = ""
        return str


def getJasperFilds(text):
    new_str = '\n'.join(el.strip() for el in text.split('\n') if el.strip())
    fildsList = new_str.splitlines()
    newFildsList = []
    vp = []
    sch = 0
    for i in fildsList:
        if sch == 3:
            sch = 1
            newFildsList.append(vp)
            vp = []
            vp.append(i)
        else:
            vp.append(i)
            sch += 1
    newFildsList.append(vp)
    print(newFildsList)
    str = ""
    for i in newFildsList:
        str += getFildForJasper(i)
    return str
