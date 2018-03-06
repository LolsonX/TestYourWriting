from __future__ import unicode_literals
from PyQt5.QtWidgets import *
import sys
import random
import time


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
        self.userInput = QLineEdit()
        self.generatedWord = QLineEdit()
        self.generateButton = QPushButton()
        self.grid = QGridLayout()
        self.draw_interface()
        self.words = WordGenerator()
        self.clock = 0

    def draw_interface(self):
        self.grid.addWidget(self.generatedWord, 1, 0)
        self.grid.addWidget(self.userInput, 2, 0)
        self.grid.addWidget(self.generateButton, 1, 1)

        self.set_properties()

        self.setGeometry(550, 350, 300, 100)
        self.setLayout(self.grid)
        self.show()
        self.action_slots()

    def set_properties(self):
        self.resize(640, 480)
        self.setWindowTitle("Writing tester")
        self.generateButton.setText("Random Word")
        self.generatedWord.setReadOnly(True)

    def action_slots(self):
        self.generateButton.clicked.connect(self.make_action)
        self.generateButton.setShortcut("Return")
        self.userInput.returnPressed.connect(self.make_action)

    def make_action(self):
        source = self.sender()
        if source.text() == "Random Word":
            word = self.words.random_word()
            self.generatedWord.setText(word)
            self.userInput.grabKeyboard()
            self.generateButton.setDisabled(True)
            self.clock = time.time()
        if source.text() == self.generatedWord.text():
            self.generatedWord.clear()
            self.userInput.clear()
            self.generateButton.setDisabled(False)
            self.clock = time.time() - self.clock
            tmp = QMessageBox.about(self, "Win", "You won!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WritingTest()
    sys.exit(app.exec_())

