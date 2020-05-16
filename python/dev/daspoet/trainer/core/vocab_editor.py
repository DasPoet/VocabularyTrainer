from glob import glob

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QShortcut
# from win32api import GetSystemMetrics as getScreenSize

from python.dev.daspoet.trainer.utils.clickable_label import ClickLabel
from python.dev.daspoet.trainer.utils.file_handling import *
from python.dev.daspoet.trainer.assets.editor_ui import *


class VocabAPI(Ui_API):
    """API that allows users to manipulate the vocabulary that is used by the trainer.
    Users can:
                I) add new vocabulary
                II) remove existing vocabulary
                III) modify existing vocabulary
                IV) specify a breakpoint after which no further vocabulary is considered by the trainer
                    (called "END" in the following)
    """

    config_file = "txt/config.txt"
    config_data = get_config(config_file)
    current_word = None
    searched = False

    def __init__(self, window):
        """Initialise the API window, provide all buttons with functionality and load the vocabulary."""

        # screen_width, screen_height = getScreenSize(0), getScreenSize(1)
        # window_width, window_height = window.size().width(), window.size().height()
        #
        # window.setGeometry((screen_width - window_width) / 2, (screen_height - window_height) / 2,
        #                    window_width, window_height)
        self.setupUi(window)
        window.setWindowTitle("Editor - github.com/daspoet")
        self.window = window

        # manual error correction
        self.language1Label.setMinimumWidth(50)
        self.language2Label.setMinimumWidth(50)
        self.languageList.setMinimumHeight(25)
        self.addButton.setMinimumWidth(40)
        self.deleteButton.setMinimumWidth(40)
        self.saveButton.setMinimumWidth(40)

        self.addButton.clicked.connect(self.add_vocab)
        self.addButton.setShortcut(QKeySequence("Return"))
        self.saveButton.clicked.connect(self.save_vocab)
        self.saveButton.setShortcut(QKeySequence("Ctrl+S"))
        self.deleteButton.clicked.connect(self.delete_vocab)
        self.deleteButton.setShortcut(QKeySequence.Delete)

        def tab():
            if self.language1Entry.hasFocus():
                self.language2Entry.setFocus()
            elif self.language2Entry.hasFocus():
                self.language1Entry.setFocus()

        tab_shortcut = QShortcut(QKeySequence("TAB"), self.window)
        tab_shortcut.activated.connect(tab)

        self.vocabList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.vocabList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vocabList.setWidgetResizable(False)

        self.language1Label.setText(self.config_data.get("language 1") + ":")
        self.language2Label.setText(self.config_data.get("language 2") + ":")

        self.switchLanguageButton.clicked.connect(self.switch_languages)
        self.searchBar.textChanged.connect(lambda: self.update_scroll_area(self.searchBar.text()))
        self.old_label = QLabel("")

        self.languageList.addItems(file.strip("\.txt") for file in glob("txt/*.txt") if not file == "txt\config.txt")
        self.languageList.currentTextChanged.connect(lambda text: self.update_language_pair(text))

        self.language_pair = f"{self.config_data.get('language 1').replace('/', ',')}-{self.config_data.get('language 2').replace('/', '')}"
        self.languageList.setCurrentIndex(self.languageList.findText(self.language_pair))

        self.vocab_file = f"txt/{self.language_pair}.txt"
        self.vocab = get_vocab(self.vocab_file, with_end=True)

        self.scroll_layout = QVBoxLayout()
        self.update_layout(self.vocab)

    def update_language_pair(self, new_pair):
        """Reload the vocabulary with respect a new pair of languages."""

        self.language_pair = new_pair

        language1, language2 = new_pair.strip(".txt").split("-")

        self.language1Label.setText(language1)
        self.language2Label.setText(language2)

        self.vocab_file = f"txt/{self.language_pair}.txt"
        self.vocab = get_vocab(self.vocab_file, with_end=True)
        self.update_layout(self.vocab)

    def delete_handling(self):
        """Test if the underlying C/C++ object of the old label has been deleted by the compiler."""

        try:
            self.old_label.objectName()
        except RuntimeError:
            self.old_label = QLabel()

    def insert_end(self, widget):
        """Add END command to the current vocab file in order to limit the vocabulary to every word up to the
        selected. """

        label = widget.sender()
        self.delete_handling()

        if not self.searched:
            with open(self.vocab_file, "r") as read_file:
                lines = read_file.read().split("\n")

            with open(self.vocab_file, "w") as file:
                for line in lines:
                    if not line.strip() == "":
                        left_part, right_part = line.split(":")
                        left_part = left_part.replace(" ", "")
                        right_part = right_part.replace(" ", "")

                        if not left_part.strip().lower() == right_part.strip().lower() == "end":
                            file.write(line + "\n")
                        if label.text() in left_part.strip().split(",") or label.text() in right_part.strip().split(
                                ","):
                            file.write("END : END\n")

        self.update_vocab_and_scroll_area()

    def label_clicked(self, widget):
        """Change the background of the label that has been clicked on and fill the language entries with
        its text and its translation."""

        self.delete_handling()

        if (text := (label := widget.sender()).text()).lower() == "end":
            return

        if label is not self.old_label:
            self.old_label.setStyleSheet("background:rgb(240, 240, 240)")  # reset background colour to default

        self.current_word = next(filter(lambda el: text in (el.first_form, el.last_form), self.vocab))

        label.setStyleSheet("background:rgb(150, 150, 150)")

        self.language1Entry.setText(self.current_word.real_first)
        self.language2Entry.setText(self.current_word.real_last)
        self.old_label = label

    def update_vocab_and_scroll_area(self):
        """Upgrade the scroll area and reload the vocabulary."""

        self.vocab = get_vocab(self.vocab_file, with_end=True)
        self.vocab = get_vocab(self.vocab_file, with_end=True)
        self.update_scroll_area("")

    def update_layout(self, vocab):
        """Update the scroll layout with new vocabulary."""

        self.scroll_layout = QVBoxLayout()
        container = QtWidgets.QWidget()

        for i in vocab:
            if isinstance(i, str):
                txt = i
            elif isinstance(i, Vocab):
                txt = i.first_form
            else:
                raise TypeError("Vocab must contain only Vocab() objects or strings")

            label = ClickLabel(txt)
            label.left_clicked.connect(lambda: self.label_clicked(label))
            label.right_clicked.connect(lambda: self.insert_end(label))

            if txt.lower() == "end":
                label.setStyleSheet("background:rgb(255, 0, 0)")

            label.setFixedWidth(140)
            self.scroll_layout.addWidget(label)

        container.setLayout(self.scroll_layout)
        self.vocabList.setWidget(container)

    def update_scroll_area(self, search_target):
        """Update the scroll area so that it only contains labels starting with some target string."""

        if search_target in [None, ""]:
            self.searched = False
            self.update_layout(self.vocab)
        else:
            self.searched = True
            self.update_layout(self.filter_vocab(search_target))

    def filter_vocab(self, target):
        """Return a list of words that start with some target string."""

        return [word for word in self.vocab if word.first_form.startswith(target)]

    def switch_languages(self):
        """Fill the vocabulary scrollbar with the vocabulary from the other language
        (flip the first and the second form of each word)."""

        for word in self.vocab:
            word.swap_languages()

        texts = list(self.scroll_layout.itemAt(i).widget().text() for i in range(self.scroll_layout.count()))

        self.update_layout((word.first_form for word in self.vocab if word.last_form in texts))

    def add_vocab(self):
        """Add a new expression to the vocabulary file and update the scrollbar with the modified vocabulary."""

        if "" in (first := self.language1Entry.text().strip(), last := self.language2Entry.text().strip()):
            return

        with open(self.vocab_file, "a") as file:
            file.write(f"\n{first} : {last}\n")

        self.language1Entry.clear()
        self.language2Entry.clear()

        self.update_vocab_and_scroll_area()

    def delete_vocab(self):
        """Remove the currently selected expression from the vocabulary file
        and update the scrollbar with the modified vocabulary.
        """

        self.delete_handling()

        with open(self.vocab_file, "r") as read_file:
            lines = read_file.read().split("\n")

        with open(self.vocab_file, "w") as write_file:
            to_remove = self.language1Entry.text().strip() + " : " + self.language2Entry.text().strip()
            for line in lines:
                if not line == to_remove:
                    write_file.write(line + "\n")

        self.language1Entry.clear()
        self.language2Entry.clear()

        self.update_vocab_and_scroll_area()

    def save_vocab(self):
        """Save the changes made to the currently selected expression to the vocabulary file and update the scroll
        area. """

        self.delete_handling()

        with open(self.vocab_file, "w") as file:
            file.write(
                "\n".join(
                    f"{self.language1Entry.text()} : {self.language2Entry.text()}\n" if word == self.current_word else
                    f"{word.real_first} : {word.real_last}" for word in self.vocab
                )
            )

        self.update_vocab_and_scroll_area()
