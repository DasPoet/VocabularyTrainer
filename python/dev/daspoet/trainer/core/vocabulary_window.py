from random import choice

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QShortcut

from utils.download_manager import *
from utils.pdf_handling import *
from core.settings_window import *
from utils.tts import speak
from core.vocab_editor import *
from assets.vocab_ui import *


class VocabWindow(Ui_Vokabeltrainer):
    """This is the main window. Here, the user can test their knowledge of the vocabulary previously entered.
    They furthermore have the option to switch between two modes; "random" and "linear".
    For further information on those see switch_modes()."""

    target_language = None  # the language that should be translated to
    current_word = None
    vocab = None
    tts_languages = tts_langs()
    tts_languages_reversed = {value: key for key, value in zip(tts_languages.keys(), tts_languages.values())}

    progress_bar_value = 0
    score = 0

    config_parameters = get_config("txt/config.txt")

    def __init__(self, window):
        """Initialise the vocabulary window, provide all buttons with functionality, load the vocabulary
        and start the first round."""

        # screen_width, screen_height = getScreenSize(0), getScreenSize(1)
        # window_width, window_height = window.size().width(), window.size().height()

        # window.setGeometry((screen_width - window_width) / 2, (screen_height - window_height) / 2,
        #                    window_width, window_height)
        self.setupUi(window)

        self.dict_file = f"txt/{self.config_parameters.get('language 1').replace('/', ',')}-{self.config_parameters.get('language 2').replace('/', ',')}"

        self.vocab = get_vocab(self.dict_file)
        self.total_words = int(self.config_parameters.get("round length"))
        self.current_mode = "random"  # possible:  random / linear

        words = [list(word.first_form for word in self.vocab), list(word.last_form for word in self.vocab)]

        reversed_langs = {value.replace("/", ","): key for key, value in zip(self.tts_languages.keys(),
                                                                             self.tts_languages.values())}

        self.l1 = self.config_parameters.get("language 1")
        self.l2 = self.config_parameters.get("language 2")

        tts_l1 = reversed_langs.get(self.l1)
        tts_l2 = reversed_langs.get(self.l2)

        self.downloadButton.clicked.connect(
            lambda: download_to_multiple_directories(words=words, dirs=(self.l1, self.l2), langs=[tts_l1, tts_l2]))
        self.deleteButton.clicked.connect(
            lambda: clear_multiple_directories(paths=(self.l1, self.l2), with_warning_dialogue=True))

        self.buttonCheck.clicked.connect(self.compare_inputs)
        self.entryInput.returnPressed.connect(self.compare_inputs)

        self.modeButton.clicked.connect(self.switch_modes)

        # Miscellaneous menu
        self.editLabel.triggered.connect(self.open_editor)
        self.settingsLabel.triggered.connect(self.open_settings)

        # File menu
        self.downloadLabel.triggered.connect(
            lambda: download_to_multiple_directories(words=words, dirs=[self.l1, self.l2], langs=[tts_l1, tts_l2]))
        self.deleteLabel.triggered.connect(
            lambda: clear_multiple_directories(paths=(self.l1, self.l2), with_warning_dialogue=True))

        self.save_as_pdf_label.triggered.connect(self.save_as_pdf)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), window)
        save_shortcut.activated.connect(self.save_as_pdf)

        self.editor_window = None
        self.settings_window = None

        self.lang1 = self.config_parameters.get("language 1")
        self.lang2 = self.config_parameters.get("language 2")

        if " (" in self.lang1:
            self.lang1 = self.lang1[:self.lang1.index("(") - 1]
        if " (" in self.lang2:
            self.lang2 = self.lang2[:self.lang2.index("(") - 1]

        self.labelLeft.setText(self.lang1)
        self.labelRight.setText(self.lang2)

        self.soundButtonLeft.clicked.connect(
            lambda: self.make_sound(text=self.entryInput.text(), lang=self.get_left_lang()))
        self.soundButtonRight.clicked.connect(
            lambda: self.make_sound(text=self.labelOutput.text(), lang=self.get_right_lang()))

        self.init_round()

    def open_editor(self):
        """Open an editor window in which the user can modify the vocabulary."""

        self.editor_window = QtWidgets.QMainWindow()

        # a reference to the window must be kept in order to ensure
        # that the underlying C/C++ object is not destroyed
        editor_window = VocabAPI(self.editor_window)

        self.editor_window.show()

    def open_settings(self):
        """Open a settings window in which the user can modify standard parameters such as:
            I) the first language
            II) the second language
            III) the length of one round
        """

        self.settings_window = QtWidgets.QMainWindow()
        # a reference to the window must be kept in order to ensure
        # that the underlying C/C++ object is not destroyed
        settings_window = Settings(self.settings_window, self.dict_file)

        self.settings_window.show()

    def get_left_lang(self):
        return self.tts_languages_reversed.get(self.labelLeft.text())

    def get_right_lang(self):
        return self.tts_languages_reversed.get(self.labelRight.text())

    def save_as_pdf(self):
        filename = QFileDialog.getSaveFileName()
        create_pdf(path=filename[0], content=get_vocab(self.dict_file))

    def init_round(self):
        """Initialise a new round."""

        self.progress_bar_value = 0
        self.progressBar.setValue(0)
        self.entryInput.clear()
        self.swap_languages()
        self.next_word()

    def make_sound(self, text, lang):
        """Construct a sound file from the text of a label and play it."""

        speak(text=text, directory=self.tts_languages.get(lang), lang=lang)
        self.entryInput.setFocus()

    def swap_languages(self):
        """Swap the languages, and reposition the input and output labels to match the new direction.
        (direction: expressions from one language are given and need to be translated into the other one by the user)
        e.g.:
            language1 -> language2 becomes language2 -> language2
            and vice versa
        """

        (langs := [self.lang1, self.lang2]).remove(target := choice(langs))
        base = langs[0]

        self.labelLeft.setText(target)
        self.labelRight.setText(base)

        self.target_language = target

    def switch_modes(self):
        """Switch between "linear" and "random" mode.
        linear mode: expressions are randomly chosen from the input vocabulary, but only appear once per round
        random mode: expressions are taken at random from the input vocabulary, thus might appear multiple times per round
        """

        if self.current_mode == "linear":
            self.current_mode = "random"
            self.modeButton.setText("random mode")
        elif self.current_mode == "random":
            self.current_mode = "linear"
            self.modeButton.setText("linear mode")

        self.vocab = get_vocab(self.dict_file)
        self.swap_languages()
        self.next_word()

    def next_word(self):
        """Get the next expression from the input vocabulary and display it."""

        if not self.vocab:
            self.swap_languages()
            self.vocab = get_vocab(self.dict_file)

        self.entryInput.setFocus()

        if len(self.vocab) >= 1:
            self.current_word = choice(self.vocab)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Info")
            msg.setText("No vocabulary for the selected languages has been added. Consider adding new words via "
                        "Miscellaneous > Editor")
            msg.exec_()
            return

        if self.current_mode == "linear":
            self.vocab.remove(self.current_word)

        # choose only one translation to display if multiple are available
        if self.current_word.languages[0] == self.labelLeft.text():
            txt = choice(self.current_word.last_form.split(",")).strip()
        else:
            txt = choice(self.current_word.first_form.split(",")).strip()

        self.labelOutput.setText(txt)

    def compare_inputs(self):
        """Compare the input provided by the user with the expected translation from the input vocabulary
        and validate it.
        """

        if self.current_word is None:
            print("debug: current word is none; returning")
            return

        if self.current_word.languages[0] == self.labelLeft.text():
            possible_translations = list(i.strip() for i in self.current_word.first_form.lower().split(","))
        else:
            possible_translations = list(i.strip() for i in self.current_word.last_form.lower().split(","))

        # make "to" optional for verbs (e.g. "to be" and "be" are both valid solutions)
        possible_translations = list(map(lambda word: word.replace("to ", "") if word.startswith("to ") else word,
                                         possible_translations))

        if self.entryInput.text().lower() in possible_translations:  # correct word entered
            if self.progress_bar_value < 100 - (100 // self.total_words):
                self.progress_bar_value += 100 / self.total_words
                self.progressBar.setValue(self.progress_bar_value)
                self.entryInput.clear()

                self.swap_languages()
                self.next_word()

                if self.progress_bar_value == 100:
                    self.score += 1
                    self.labelScore.setText("Score: " + str(self.score))
                    self.init_round()
            else:
                self.score += 1
                self.labelScore.setText("Score: " + str(self.score))
                self.init_round()
        else:
            print("Moeglich waere gewesen:",
                  *list(el + "," if not i == len(possible_translations) - 1 else el for i, el
                        in enumerate(possible_translations)))
