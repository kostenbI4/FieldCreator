import JasperTemplates as jt

#Строю на основании отчета EquipCatalog

class JasperFileGenerator:

    def __init__(self, filds="", width=1644):
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
    def createTitle(self):
        title = "<title>" + jt.titleHead
        title += self.getFildnames()
        title += "</title>"
        print(title)
        return title

    # Возвращает jr поля с именами столбцов
    def getFildnames(self):
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
    def getColumnHeader(self):
        print(jt.columnHeader.format(data=self.getColumnHeaderData()))
        return jt.columnHeader.format(data=self.getColumnHeaderData())

    # Возвращает данные для columnHeader
    def getColumnHeaderData(self):
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


JasperFileGenerator = JasperFileGenerator(jt.testData)
JasperFileGenerator.createTitle()
