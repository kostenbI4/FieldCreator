import configparser
import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from configparser import ConfigParser
import JasperFileGenerator as JFG
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

    textForCreateJasper = """
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
            Main.createStandartFiles(self.dirForStandart)
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
        if not os.path.exists('config.properties'):
            with open('config.properties', 'w'): pass
        self.configParser = ConfigParser()
        self.configParser.read('config.properties')
        if not self.configParser.has_section("Settings"):
            self.configParser.add_section("Settings")
            self.configParser.set("Settings", "dir", "")

        self.dir = self.configParser.get("Settings", "dir")
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
        createStandartFiles = QHBoxLayout()
        self.radioStandart = QRadioButton("Стандартный генератор")
        createStandartFiles.addWidget(self.radioStandart)
        self.className = QLineEdit()
        self.className.setPlaceholderText("введите имя файла")
        self.className.setDisabled(True)
        createStandartFiles.addWidget(self.className)
        self.openDirButtonForStandart = QPushButton("Выберите папку")
        self.openDirButtonForStandart.setDisabled(True)
        self.openDirButtonForStandart.clicked.connect(self.getDirectoryForStandart)
        createStandartFiles.addWidget(self.openDirButtonForStandart)
        self.dirLabelForStandart = QLabel(self.dir)
        self.dirLabelForStandart.setMinimumWidth(300)
        createStandartFiles.addWidget(self.dirLabelForStandart)

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
        checkBoxLayout.addLayout(createStandartFiles)
        checkBoxLayout.addWidget(self.radioReport)
        checkBoxLayout.addWidget(self.radioReportFilter)
        checkBoxLayout.addWidget(self.radioJaserFilds)
        checkBoxLayout.addLayout(createJasperLayout)

        self.move(300, 150)
        self.show()

    def getDirectory(self):  # <-----
        self.dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.configParser.set("Settings", "dir", self.dir)
        with open("config.properties", "w") as config_file:
            self.configParser.write(config_file)
        self.dirLabel.setText(self.dir)

    def getDirectoryForStandart(self):  # <-----
        self.dirForStandart = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.configParser.set("Settings", "dirForStandart", self.dirForStandart)
        with open("config.properties", "w") as config_file:
            self.configParser.write(config_file)
        self.dirLabelForStandart.setText(self.dirForStandart)

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

        if self.radioStandart.isChecked():
            self.openDirButtonForStandart.setDisabled(False)
            self.className.setDisabled(False)
            self.textInput.setPlaceholderText(self.textForInputPlaceholder)
        else:
            self.openDirButtonForStandart.setDisabled(True)
            self.className.setDisabled(True)
            self.textInput.setPlaceholderText(self.textForInputPlaceholder)

    def createJasper(self):
        try:
            if self.textInput.toPlainText():
                JasperFileGenerator = JFG.JasperFileGenerator(filds=self.textInput.toPlainText(),
                                                              fileName=self.fileName.text())
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
        except Exception as err:
            print(str(err), "TUT")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(err))
            msg.exec_()



if __name__ == "__main__":
    # try:
        app = QApplication(sys.argv)
        win = QtDesignPage()
        win.setWindowIcon(QtGui.QIcon('icon.ico'))
        app.setWindowIcon(QtGui.QIcon('icon.ico'))
        sys.exit(app.exec_())
    # except Exception as e:
    #     pass