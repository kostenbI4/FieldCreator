import sys

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import JasperFileGenerator as JFG
import JasperTemplates as jt
import Main


class QtDesignPage(QWidget):
    textForInputPlaceholder = """
        Введите Исходные данные типа:
        snumber - character varying - № КТП
        scaption - character varying - КТП
        sFlow - character varying - Маршрут

        Также воспринимаются Мишины данные типа:
        MNF_Capacity.Get(rbt.id) as scapacity, --  [Код вида мощности]

        Также воспринимаются данные типа:
         smnemocode
         varchar 
         Номер
         """

    textForCreateJasper="""
        Введите данные типа:
        // Деталь код SAP
        @Column(name = "scodesap")
        private String codeSap; 
    
        // Количество в задании
        @Column(name = "fqty_plan")
        private Double quantityPlan; 
    """

    def btnEvent(self):
        if self.radioStandart.isChecked():
            self.textOutput.setPlainText(Main.getFilds(self.textInput.toPlainText()))
        elif self.radioReportFilter.isChecked():
            self.textOutput.setPlainText(Main.getFiltersFilds(self.textInput.toPlainText()))
        elif self.radioJaserFilds.isChecked():
            self.textOutput.setPlainText(Main.getJasperFilds(self.textInput.toPlainText()))
        elif self.radioCreateJasper.isChecked():
            self.createJasper()
        else:
            self.textOutput.setPlainText(Main.getReportFilds(self.textInput.toPlainText()))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dir = ""
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Генератор полей")  # заголовок окна
        self.move(300, 300)  # положение окна
        self.resize(1024, 768)  # размер окна

        outContainer = QVBoxLayout()
        self.setLayout(outContainer)

        scrollsContainer = QHBoxLayout()
        outContainer.addLayout(scrollsContainer)
        self.textInput = QTextEdit()
        self.textInput.setPlaceholderText(self.textForInputPlaceholder)
        self.textOutput = QPlainTextEdit()
        self.textOutput.setPlaceholderText("Тут будет результат")
        self.textOutput.setReadOnly(True)
        scrollsContainer.addWidget(self.textInput)
        scrollsContainer.addWidget(self.textOutput)

        bottomContainer = QGridLayout()

        outContainer.addLayout(bottomContainer)

        btnLayout = QHBoxLayout()
        btn = QPushButton("Выполнить")
        btn.clicked.connect(self.btnEvent)
        btnLayout.addWidget(btn)
        btnLayout.addSpacing(50)
        # btn.setFixedWidth(180)
        btn.setMinimumWidth(80)
        btn.setMaximumWidth(180)

        # btn.clicked.connect(lambda : bottomContainer.addSpacing(200))
        bottomContainer.addLayout(btnLayout, 0, 0)
        checkBoxLayout = QVBoxLayout()
        bottomContainer.addLayout(checkBoxLayout, 0, 1)
        # bottomContainer.addStretch(1)
        self.radioStandart = QRadioButton("Стандартный генератор")
        self.radioReport = QRadioButton("Генератор для отчетов")
        self.radioReportFilter = QRadioButton("Генератор для фильтров")
        self.radioJaserFilds = QRadioButton("Поля для Jasper")
        self.radioStandart.toggled.connect(self.radioClick)
        self.radioReport.toggled.connect(self.radioClick)
        self.radioReportFilter.toggled.connect(self.radioClick)
        self.radioJaserFilds.toggled.connect(self.radioClick)

        createJasperLayout = QHBoxLayout()
        self.radioCreateJasper = QRadioButton("Создать файл jasper")
        createJasperLayout.addWidget(self.radioCreateJasper)
        self.fileName = QLineEdit()
        self.fileName.setPlaceholderText("введите имя файла")
        self.fileName.setDisabled(True)
        createJasperLayout.addWidget(self.fileName)
        self.openDirButton = QPushButton("Выберите папку")
        self.openDirButton.setDisabled(True)
        self.openDirButton.clicked.connect(self.getDirectory)
        createJasperLayout.addWidget(self.openDirButton)
        self.dirLabel = QLabel(self.dir)
        self.dirLabel.setMinimumWidth(300)
        createJasperLayout.addWidget(self.dirLabel)
        self.createButton = QPushButton("Создать")
        self.createButton.setFixedWidth(100)
        self.createButton.setDisabled(True)
        self.createButton.clicked.connect(self.createJasper)
        # createJasperLayout.addWidget(self.createButton)
        self.radioCreateJasper.toggled.connect(self.radioClick)

        self.radioStandart.setChecked(True)
        # checkBoxLayout.addStretch(1)
        checkBoxLayout.addWidget(self.radioStandart)
        checkBoxLayout.addWidget(self.radioReport)
        checkBoxLayout.addWidget(self.radioReportFilter)
        checkBoxLayout.addWidget(self.radioJaserFilds)
        checkBoxLayout.addLayout(createJasperLayout)

        self.move(300, 150)
        self.show()

    def getDirectory(self):  # <-----
        self.dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.dirLabel.setText(self.dir)

    def radioClick(self):
        if self.radioCreateJasper.isChecked():
            self.openDirButton.setDisabled(False)
            self.fileName.setDisabled(False)
            self.createButton.setDisabled(False)
            self.textInput.setPlaceholderText(self.textForCreateJasper)
        else:
            self.openDirButton.setDisabled(True)
            self.fileName.setDisabled(True)
            self.createButton.setDisabled(True)
            self.textInput.setPlaceholderText(self.textForInputPlaceholder)

    def createJasper(self):
        if self.textInput.toPlainText():
            JasperFileGenerator = JFG.JasperFileGenerator(filds=self.textInput.toPlainText(), fileName=self.fileName.text())
            JasperFileGenerator.getJasper(path=self.dir)
            self.textOutput.setPlainText(JasperFileGenerator.getFulJasperText())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Введите поля")
            txt = """Введите поля в формате:
                //Время окончания
    @Column(name = "tend")
    private LocalTime end;

    //Исключения к календарю профиля (
    @Column(name = "sclndexception")
    private String clndException;
            """
            msg.setInformativeText(txt)
            msg.setWindowTitle("Внимание")
            msg.exec_()
        # print(self.dir)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QtDesignPage()
    win.setWindowIcon(QtGui.QIcon('icon.png'))
    sys.exit(app.exec_())
