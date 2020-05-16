"""Make use of the Google text-to-speech API (gTTS) in order to turn text into sound and to play those sounds using the
playsound module
"""

from os import remove

from playsound import playsound

from python.dev.daspoet.trainer.utils.download_manager import *


def speak_threaded(*, word, directory, lang):
    """Use a separate thread to download a sound file and to play it."""

    file = "sounds/" + directory + "/" + word + ".mp3"

    if not isfile(file):
        download_file(word=word, use_separate_thread=False, directory=directory, lang=lang)
    try:
        playsound(file)
    except:
        try:
            remove(file)
        except:
            pass


def sound_from_text(*, text, lang):
    """Return a gTTS object for some text."""

    return gTTS(text=text, lang=lang)


def speak(*, text, directory, lang):
    """Call speak_threaded()."""

    if not text.strip() == "":
        Thread(target=lambda: speak_threaded(word=text, directory=directory, lang=lang)).start()
