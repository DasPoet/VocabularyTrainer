"""Get information from files and clean up directories."""

from os.path import exists, isfile
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox

from utils.vocab import Vocab


def clear_directory(*, path: str, with_warning_dialogue=False):
    """Delete all .mp3 files from path after asking the user for permission through a dialog window."""

    path = "sounds/" + path

    if not exists(path):
        return

    if with_warning_dialogue:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Request")
        msg.setText(f"Are you sure you want to delete all sound files from {path}?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

        ret_value = msg.exec_()
        if ret_value == QMessageBox.No:
            return

    for f in Path(path).glob("*"):
        if f.is_file() and str(f).endswith(".mp3"):
            try:
                f.unlink()
            except PermissionError:
                print(f"Permission error: file \u0022{f}\u0022 cannot be accessed")


def clear_multiple_directories(*, paths: iter, with_warning_dialogue=False):
    """Delete all .mp3 files from multiple directories after asking the user for permission for each of those through
    a dialog window."""

    print("Not yet implemented")
    return

    for path in paths:
        clear_directory(path=path, with_warning_dialogue=with_warning_dialogue)


def make_vocab_list(li: list, langs, with_end=False):
    """Read the entire vocabulary from the vocab file and return a list containing it.
    For more information see get_vocab()."""

    split_vocab = []
    for i in li:
        if not i.strip() == "":
            left, right = i.split(":")
            if left.strip().lower() == right.strip().lower() == "end" and not with_end:
                break
            split_vocab.append(Vocab(form1=left.strip(), form2=right.strip(),
                                     languages=list(lang[:lang.index("(") - 1] if " (" in lang else lang for lang in
                                                    langs)))
    return split_vocab


def get_config_information(lines, path):
    """Read the standard attributes from the config file and return a dict containing them.
    For more information see get_config()."""

    allowed_parameters = ["language 1", "language 2", "round length"]
    arguments = {}

    for line in lines:
        if line.strip() == "":
            continue

        left, right = tuple(el.strip() for el in line.split(":"))

        if left not in allowed_parameters:
            raise NameError(f"Unexpected parameter \u0022{left}\u0022 in {path}; expected {allowed_parameters}")
        arguments[left] = right
    return arguments


def get_vocab(path: str, with_end=False):
    """Return vocab.

    return value:
    list -- contains Vocab() objects
    for more information on Vocab() see vocab.py
    """

    if not path.endswith(".txt") and "." not in path:
        path += ".txt"

    if not isfile(path):
        with open(path, "w") as _:
            pass

    with open(path) as file:
        return make_vocab_list(file.read().split("\n"), path.strip("/.txt").split("-"), with_end)


def get_config(path: str):
    """Return everything that is needed for configuring initial settings

    return value (example):
    dict -- {language1: "...", language2: "...", round length: "..."}
    """

    with open(path) as file:
        return get_config_information(file.read().split("\n"), path)
