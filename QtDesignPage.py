import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

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
    def btnEvent(self):
        if self.radioStandart.isChecked():
            self.textOutput.setText(Main.getFilds(self.textInput.toPlainText()))
        else:
            self.textOutput.setText(Main.getReportFilds(self.textInput.toPlainText()))

    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.textOutput = QTextEdit()
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
        self.radioStandart.setChecked(True)
        # checkBoxLayout.addStretch(1)
        checkBoxLayout.addWidget(self.radioStandart)
        checkBoxLayout.addWidget(self.radioReport)

        self.move(300, 150)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QtDesignPage()
    sys.exit(app.exec_())
