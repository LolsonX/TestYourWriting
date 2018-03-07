from __future__ import unicode_literals
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime, Qt, QSize
from PyQt5.QtGui import QFont, QBrush, QPalette, QImage, QIcon
import sys
import random


class WordGenerator:
    def __init__(self):
        self.filePath = "words.txt"
        self.fileHandle = None
        self.words = None
        self.load_words()

    def random_word(self):
        return random.choice(self.words)

    def load_words(self):
        try:
            self.fileHandle = open(self.filePath, "r")
            self.words = str(self.fileHandle.read())
            self.words = self.words.split(",")
        finally:
            self.fileHandle.close()


class WritingTest(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.configPath = "config.cfg"
        self.clock = QTimer()
        self.time = QTime(0, 0, 0)
        self.userInput = QLineEdit()
        self.generatedWord = QLineEdit()
        self.timeOutput = QLineEdit()
        self.generateButton = QPushButton()
        self.timeLabel = QLabel()
        self.generatedLabel = QLabel()
        self.inputLabel = QLabel()
        self.grid = QGridLayout()
        tmp_image = QImage("back.png")
        tmp_scaled = tmp_image.scaled(QSize(650, 480))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(tmp_scaled))  # 10 = Window role
        self.setPalette(palette)
        self.draw_interface()
        self.words = WordGenerator()
        self.limit = 30
        self.load_config()

    def draw_interface(self):
        self.grid.addWidget(self.timeLabel, 1, 3,)
        self.grid.setAlignment(self.timeLabel, Qt.AlignRight)
        self.grid.addWidget(self.inputLabel, 1, 1)
        self.grid.setAlignment(self.inputLabel, Qt.AlignRight)
        self.grid.addWidget(self.generatedLabel, 0, 1)
        self.grid.setAlignment(self.generatedLabel, Qt.AlignRight)
        self.grid.addWidget(self.generatedWord, 0, 2)
        self.grid.addWidget(self.userInput, 1, 2)
        self.grid.addWidget(self.generateButton, 0, 4)
        self.grid.addWidget(self.timeOutput, 1, 4)
        self.grid.setAlignment(self.timeOutput, Qt.AlignCenter)
        self.setContentsMargins(0, 0, 0, 0)
        self.set_properties()
        self.setLayout(self.grid)
        self.show()
        self.action_slots()

    def set_properties(self):
        self.resize(650, 240)

        self.timeOutput.setFixedSize(40, 40)
        self.timeOutput.setFont(QFont("Times", 15, QFont.Bold))
        self.timeOutput.setText("0" + str(self.time.second()))
        self.timeOutput.setReadOnly(True)

        self.timeLabel.setText("Time: ")
        self.timeLabel.setStyleSheet("margin-top: 0px;")
        self.timeOutput.setObjectName("timeOutput")
        self.inputLabel.setText("Your answer: ")
        self.generatedLabel.setText("Your word: ")
        self.setWindowTitle("Writing tester")
        self.generateButton.setText("Random Word")
        self.generatedWord.setReadOnly(True)
        self.userInput.setFixedSize(260, 30)
        self.generatedWord.setFixedSize(260, 30)
        self.userInput.setFont(QFont("Times", 15, QFont.Bold))
        self.generatedWord.setFont(QFont("Times", 15, QFont.Bold))
        self.generatedWord.setAlignment(Qt.AlignCenter)
        self.userInput.setAlignment(Qt.AlignCenter)
        self.timeOutput.setAlignment(Qt.AlignCenter)

    def action_slots(self):
        self.generateButton.clicked.connect(self.make_action)
        self.generateButton.setShortcut("Return")
        self.userInput.returnPressed.connect(self.make_action)
        self.clock.timeout.connect(self.timeout)

    def make_action(self):
        source = self.sender()
        if source.text() == "Random Word":
            word = self.words.random_word()
            self.generatedWord.setText(word)
            self.userInput.grabKeyboard()
            self.generateButton.setDisabled(True)
            self.clock.start(1000)
            self.timeOutput.setText(str(self.limit - self.time.second()))
        if source.text() == self.generatedWord.text():
            self.reset()
            tmp = QMessageBox.about(self, "Win", "<font size=15>You won!</font>")

    def timeout(self):
        self.time = self.time.addSecs(1)
        diff = str(self.limit - self.time.second())
        if len(diff) < 2:
            diff = "0" + diff
        self.timeOutput.setText(diff)
        if self.time.second() == self.limit:
            self.reset()
            tmp = QMessageBox.about(self, "Lose", "<font size=15>You've lost!</font>")

    def reset(self):
        self.generatedWord.clear()
        self.userInput.clear()
        self.generateButton.setDisabled(False)
        self.clock.stop()
        self.time = QTime(0, 0, 0)
        tmp = "0" + str(self.time.second())
        self.timeOutput.setText(tmp)

    def load_config(self):
        try:
            config = open(self.configPath, "r")
            time = config.readlines()
            self.limit = int(time[0][5:])

        finally:
            config.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QIcon("fav.png")
    app.setWindowIcon(icon)
    app.setStyleSheet(
'''
QLineEdit {
padding: 1px;
border-style: solid;
border: 2px solid gray;
border-radius: 8px;
min-height : 50px;
background-color : rgb(192,192,255);
}
QLineEdit#timeOutput
{
}
QPushButton {
color: white;
background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c);
border-width: 1px;
border-color: #339;
border-style: none;
border-radius: 1;
padding: 3px;
font-size: 20px;
padding-left: 5px;
padding-right: 5px;
min-width: 100px;
max-width: 200px;
min-height: 50px;
max-height: 75px;
}

QPushButton:hover 
{
color: black;
}

QMessageBox
{
padding: 1px;
border-style: solid;
border: 2px solid gray;
border-radius: 1px;
font: 10px;
}
QLabel {
margin-top:30px;
font-weight: bold;
font-size: 20px;
}

''')
    window = WritingTest()
    sys.exit(app.exec_())

