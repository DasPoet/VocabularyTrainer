# **VocabularyTrainer**

This vocabulary trainer was made as an easy tool to help people learn new vocabulary. It is meant to be easy to use and to understand. In the following, the usage will be explained, and all necessary dependencies will be laid out.

# **Dependencies**

* PyQt5
* playsound
* gtts
* fpdf

  * the END command: a breakpoint after which no further vocabulary is considered by the trainer (applicable in the editor window by right     clicking any of the displayed words)
  * the philosophy behind the END command is that progress should be linear; therefore, no specific ranges of words are
    eligible for selection in the editor
  * characters like "ä", "ö", "ü" and "ß" are to be expressed as "ae", "oe", "ue" and "ss" respectively
