from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from gtts.lang import tts_langs

from assets.settings_ui import *
from utils.file_handling import *
from utils.file_handling import get_vocab


# from win32api import GetSystemMetrics as getScreenSize


class Settings(Ui_MainWindow):
    """Settings window that allows the user to specify
        I) both of the languages used by the trainer
        II) the length of one round
    """

    config_path = "txt/config.txt"

    def __init__(self, window, vocab_path):
        """Initialise the settings window and fill in the entries with their respective parameters.
        the entries currently are:
            first language: ...
            second language: ...
            round length : ...
        """

        # screen_width, screen_height = getScreenSize(0), getScreenSize(1)
        # window_width, window_height = window.size().width(), window.size().height()
        #
        # window.setGeometry((screen_width - window_width) / 2, (screen_height - window_height) / 2,
        #                    window_width, window_height)
        self.setupUi(window)
        self.window = window

        raw_config = get_config(self.config_path)
        self.config_parameters = {
            key: value[:value.index("(")] + " " + value[value.index("("):] if "(" in value else value for key, value in
            zip(raw_config.keys(), raw_config.values())}
        self.vocab_path = vocab_path

        self.config_parameters = raw_config

        languages = tts_langs().values()
        self.language1List.addItems(map(lambda el: el.replace("/", ","), languages))
        self.language2List.addItems(map(lambda el: el.replace("/", ","), languages))

        self.language1List.setCurrentIndex(self.language1List.findText(self.config_parameters.get("language 1").replace("/", ",")))
        self.language2List.setCurrentIndex(self.language2List.findText(self.config_parameters.get("language 2").replace("/", ",")))

        self.roundLengthCounter.setValue(int(self.config_parameters.get("round length")))

        self.saveButton.clicked.connect(lambda: self.save())
        self.standardLengthButton.toggled.connect(self.use_standard_length)

        save_shortcut = QShortcut(QKeySequence("Strg+S"), self.window)
        save_shortcut.activated.connect(self.save)

    def save(self):
        """Write the inputs of all entries to the config file.
        e.g.:
            first language : ...
            second language : ...
            round length : ...
        """

        try:
            int(self.roundLengthCounter.value())
        except ValueError:
            print("ERROR: Length can only consist of numbers")

        with open(self.config_path, "w") as file:
            file.write(self.language1Label.text().lower() + self.language1List.currentText() + "\n")
            file.write(self.language2Label.text().lower() + self.language2List.currentText() + "\n")
            file.write("round length: " + str(self.roundLengthCounter.value()))

    def use_standard_length(self):
        """Set the length of one round to the number of words up to END in the vocabulary file."""

        self.roundLengthCounter.setReadOnly(not self.roundLengthCounter.isReadOnly())

        if self.roundLengthCounter.isReadOnly():
            self.roundLengthCounter.setStyleSheet("background-color:rgb(120, 120, 120)")
            self.roundLengthCounter.setValue(int((len(get_vocab(self.vocab_path)))))
        else:
            self.roundLengthCounter.setStyleSheet("")
