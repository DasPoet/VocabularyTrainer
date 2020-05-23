# **vocabulary-trainer**

This vocabulary trainer was made as an easy tool to help people learn new vocabulary. 
It is meant to be easy to use and to understand.

# **Getting started**

Note that all links [```below```](#**Features**) point to the implementation of the respective features. To see them in action 
start using the vocabulary trainer by cloning this repository and executing
[```main.py```](https://github.com/DasPoet/vocabulary-trainer/blob/master/python/dev/daspoet/trainer/main.py).

# **Dependencies (pip)**

* PyQt5
* playsound
* gtts
* fpdf

# **Features**

**Practicing vocabulary**

The vocabulary trainer supports a variety - over 75 - different languages. You can **change the languages** you want to learn
in the [```settings window```](https://github.com/DasPoet/vocabulary-trainer/blob/master/python/dev/daspoet/trainer/core/settings_window.py).

Entering the correct translation of a word increases your progress in the current round. After completing one round your
score advances. The **length** of one round can also be changed in the
[```settings window```](https://github.com/DasPoet/vocabulary-trainer/blob/master/python/dev/daspoet/trainer/core/settings_window.py).

If you just want to rehearse existing vocabulary you can do that in the 
[```main window```](https://github.com/DasPoet/vocabulary-trainer/blob/master/python/dev/daspoet/trainer/core/vocabulary_window.py).
It provides two practice modes:

* _**random mode:**_ words are picked at random
* _**linear mode:**_ words are also picked at random, but every word will have been tested before a particular word is
                     tested for the second time
                     
If you'd like to hear how a particular word is pronounced, click on the sound button below it.

#

**Modifying vocabulary**

To **modify existing vocabulary,** open the 
[```editor window```](https://github.com/DasPoet/vocabulary-trainer/blob/master/python/dev/daspoet/trainer/core/vocab_editor.py)
and select the correct pair of languages in the **bottom right** corner of the window.

To **add new vocabulary**, fill the entries and click on the add-button, or **press Return**. Note that you can add
**multiple expressions** to a word by separating them by ",".

To **remove existing vocabulary**, select the word you'd like to remove and click on the remove-button, or **press Del**.

You can also **make changes to a particular word** by selecting it and changing at least one of the expressions via the 
entries. Save your changes by clicking on the save-button, or by **pressing Ctrl+S**.

To **limit the range of vocabulary tested**, you can insert the so-called **"END"**-command. The trainer will only consider
vocabulary up to this breakpoint. You can insert it after any expression by **right-clicking** it and selecting "**Add END**".
