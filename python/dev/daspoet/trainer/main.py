"""The main module for easy execution of the trainer. Just run this and be happy :)"""

import sys

from PyQt5 import QtWidgets
from core.vocabulary_window import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    vocab_window = VocabWindow(window)

    window.show()

    app.exec_()
