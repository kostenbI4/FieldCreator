import re

import JasperTemplates as jt

defFilds="""//DEFAULT
    @Column(name = "sdefault")
    private String default;"""

# Строю на основании отчета EquipCatalog
class JasperFileGenerator:

    def __init__(self, filds=defFilds, width=1644, fileName="DefaultName"):
        self.fileName = fileName
        self.JASPERCLASSES = {
            'i': "java.math.BigInteger",
            "s": "java.lang.String",
            "f": "java.lang.Double",
            "b": "java.lang.Integer",
            "n": "java.lang.Integer",
            "d": "java.time.LocalDate",
            "t": "java.time.LocalTime",
            "dt": "java.time.LocalDateTime"
        }

        self.FORMATTERSNAMES = {
            "java.time.LocalDate": "DateFormatter",
            "java.time.LocalTime": "TimeFormatter",
            "java.time.LocalDateTime": "DateTimeFormatter",
        }

        self.VARIABLESDICT = {
            "d": "java.time.LocalDate",
            "dt": "java.time.LocalDateTime",
            "t": "java.time.LocalTime",

        }

        self.widthReport = width
        # Создаем массив типа [['//Бизнес-процесс', '@Column(name = "swcmnemocode")', 'private String wcMnemocode;'],
        # ['//Наименование', '@Column(name = "scaption")', 'private String caption;']]
        # из данных типа
        #     //   Чертежный номер
        #     @Column(name = "sdrawcode")
        #     private String drawCode;
        new_str = '\n'.join(el.strip() for el in filds.split('\n') if el.strip())
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

        self.filds = newFildsList  # массив типа [['//Бизнес-процесс', '@Column(name = "swcmnemocode")', 'private String wcMnemocode;'],
        # ['//Наименование', '@Column(name = "scaption")', 'private String caption;']]
        self.widthFild = int(self.widthReport / len(self.filds))  # Длина столбца
        self.countFilds = len(newFildsList)  # Количество столбцов

        # определяем длинну последнего столбца
        self.widthLastFild = self.widthFild + (self.widthReport - self.widthFild * self.countFilds)

        # определяем координаты ячеек
        self.coordX = [0]
        for i in range(1, self.countFilds):
            self.coordX.append(self.coordX[-1] + self.widthFild)

    # Возвращает jr <title>
    def _getTitle(self):
        title = "    <title>" + jt.titleHead
        title += self._getFildnames()
        title += "        </band>\n"
        title += "   </title>"
        return title

    # Возвращает jr поля с именами столбцов
    def _getFildnames(self):
        fildNames = ""
        for i in zip(self.filds, self.coordX, range(1, len(self.filds) + 1)):
            name = i[0][0].strip()[2:].strip()
            coord = i[1]
            if i[2] == len(self.filds):
                fildNames += jt.fildName.format(name=name, coord=coord, width=self.widthLastFild)
            else:
                fildNames += jt.fildName.format(name=name, coord=coord, width=self.widthFild)
        return fildNames

    # Возвращает columnHeader
    def _getColumnHeader(self):
        # print(jt.columnHeader.format(data=self.getColumnHeaderData()))
        return jt.columnHeader.format(data=self._getColumnHeaderData())

    # Возвращает данные для columnHeader
    def _getColumnHeaderData(self):
        columns = ""
        for i in zip(self.filds, self.coordX, range(1, len(self.filds) + 1)):
            coord = i[1]
            count = i[2]
            if i[2] == 1:
                columns += jt.columnHeaderFirstField.format(coord=coord, count=count, width=self.widthFild)
            elif i[2] == len(self.filds):
                columns += jt.columnHeaderField.format(coord=coord, count=count, width=self.widthLastFild)
            else:
                columns += jt.columnHeaderField.format(coord=coord, count=count, width=self.widthFild)
        return columns

    def _getDetaIl(self):
        # print(jt.detail.format(data=self.getDataFields()))
        return jt.detail.format(data=self._getDataFields())

    # Возвращает Jasper поля блока details
    def _getDataFields(self):
        columns = ""
        for i in zip(self.filds, self.coordX, range(1, len(self.filds) + 1)):
            fildName = i[0][2].strip().split(" ")[-1:][0][:-1]
            coord = i[1]
            pattern = self._getPattern(fildName)
            fildNameTemplate = f"""$F{{{fildName}}}{self._getFormat(re.findall(r'"(.*)"', i[0][1].strip())[0])}"""
            if i[2] == len(self.filds):
                columns += jt.detailTextField.format(coord=coord, name=fildNameTemplate, width=self.widthLastFild,
                                                     pattern=pattern)
            else:
                columns += jt.detailTextField.format(coord=coord, name=fildNameTemplate, width=self.widthFild,
                                                     pattern=pattern)
        return columns

    def _getFormat(self, fildName):
        format = ""
        bukva = fildName[:1]
        # print(fildName)
        if bukva == "d":
            nextBukva = fildName[1:2]
            if nextBukva == "t":
                return f".format($V{{{self.FORMATTERSNAMES.get('java.time.LocalDateTime')}}})"
            return f".format($V{{{self.FORMATTERSNAMES.get('java.time.LocalDate')}}})"
        elif bukva == "t":
            return f".format($V{{{self.FORMATTERSNAMES.get('java.time.LocalTime')}}})"
        else:
            return format

    def _getPattern(self, fildName):
        bukva = fildName[:1]
        if bukva == "d":
            nextBukva = fildName[1:2]
            bukva += nextBukva if nextBukva == "t" else ""
        if (bukva == "i" or bukva == "b" or bukva == "n"):
            return "0"
        elif bukva == "d":
            return "0.0"
        else:
            return "@"

    # возвращает Fields поле
    def _getFildForJasper(self, list):
        # print(list)
        fildName = list[2].strip().split(" ")[-1:][0][:-1]
        fildForClassName = list[1].strip()
        match = re.findall(r'"(.*)"', fildForClassName)[0]
        head = f"""
    <field name="{fildName}" class="{self._getJasperClass(match)}"/>
    """
        return head

    def _getJasperClass(self, fildName):
        bukva = fildName[:1]
        if bukva == "d":
            nextBukva = fildName[1:2]
            bukva += nextBukva if nextBukva == "t" else ""

        return self.JASPERCLASSES.get(bukva)

    # возвращает Fields поля
    def _getJasperFilds(self):
        str = ""
        for i in self.filds:
            str += self._getFildForJasper(i)
        return str

    # Возвращает поля Variables
    def _getVariables(self):
        str = ""
        for i in self.filds:
            str += self._getVariable(re.findall(r'"(.*)"', i[1].strip())[0])
        return str

    def _getVariable(self, fildName):
        bukva = fildName[:1]
        nextBukva = fildName[1:2]
        if nextBukva == "t":
            bukva += "t"

        if self.VARIABLESDICT.get(bukva):
            if bukva == "d":
                return jt.variable.format(name=self.FORMATTERSNAMES.get(self.VARIABLESDICT.pop(bukva)),
                                          pattern="dd.MM.yyyy")
            elif bukva == "dt":
                return jt.variable.format(name=self.FORMATTERSNAMES.get(self.VARIABLESDICT.pop(bukva)),
                                          pattern="dd.MM.yyyy HH:mm")
            elif bukva == "t":
                return jt.variable.format(name=self.FORMATTERSNAMES.get(self.VARIABLESDICT.pop(bukva)),
                                          pattern="HH:mm:ss")
            else:
                return ""
        else:
            return ""

    def getFulJasperText(self):
        jasper = ""
        jasper += jt.header.format(name=self.fileName)
        jasper += self._getJasperFilds()
        jasper += self._getVariables()
        jasper += self._getTitle()
        jasper += self._getColumnHeader()
        jasper += self._getDetaIl()
        jasper += "</jasperReport>"
        new_str = jasper.replace('\n\n', '\n')
        return new_str

    def getJasper(self, path=""):
        print(f"{path}/{self.fileName}.jrxml")
        try:
            with open(f"{path}/{self.fileName}.jrxml", mode="w", encoding="utf-8") as f:
                print(f"{path}/{self.fileName}.jrxml")
                f.write(self.getFulJasperText())
        except Exception as e:
            print(str(e))

# JasperFileGenerator = JasperFileGenerator(filds = jt.testData)
# print(JasperFileGenerator.getFulJasperText())
