"""Manage the download of sound files using the Google text-to-speech API (gTTS)."""

from os import rename, mkdir
from os.path import isfile, exists
from threading import Thread

from PyQt5.QtWidgets import QMessageBox
from gtts import gTTS

from utils.file_handling import clear_directory


def sound_from_text(*, text, lang):
    """Return a gTTS object for some particular text and language."""

    return gTTS(text=text, lang=lang)


def create_sound_file(*, word, filename, directory, lang):
    """Construct a sound file from a word and save it to a given directory."""

    filepath = "sounds/" + directory + "/" + filename

    if not isfile(filepath):
        try:
            sound = sound_from_text(text=word, lang=lang)
            sound.save(filename)
            try:
                rename(filename, filepath)
            except PermissionError:
                pass
        except:
            if not isfile(filename):
                print("Check your internet connection.")
        clear_directory(path="", with_warning_dialogue=False)  # remove all sound files from the main directory


def download_file(*, word, use_separate_thread, directory, lang):
    """Download one sound file either using a separate thread or using the main thread."""

    if not exists("sounds/" + directory):
        mkdir("sounds/" + directory)

    if use_separate_thread:
        Thread(target=lambda: create_sound_file(word=word, filename=word + ".mp3", directory=directory, lang=lang))\
            .start()
    else:
        create_sound_file(word=word, filename=word + ".mp3", directory=directory, lang=lang)
        print("Download complete")


def download_to_multiple_directories(*, words, dirs, langs):
    """Download all sound files for a given list of words to some specific directories."""

    print("Not yet implemented")
    return

    for word, directory, lang in zip(words, dirs, langs):
        download_all_files(words=word, directory=directory, lang=lang)


def download_all_files(*, words, directory, lang):
    """Download all sound files for a given list of words to some specific directory."""

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Request")
    msg.setText(f"Download all {directory} sound files?")
    msg.setInformativeText("This could potentially slow down your internet connection for the time of the download. "
                           "Proceed?")
    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

    ret_value = msg.exec_()
    if ret_value == QMessageBox.No:
        return

    if not exists("sounds/" + directory):
        mkdir("sounds/" + directory)

    for word in words:
        download_file(word=word, use_separate_thread=True, directory=directory, lang=lang)
