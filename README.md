# **VocabularyTrainer**

This vocabulary trainer was made as an easy tool to help people learn new vocabulary. It is meant to be easy to use and to understand. In the following, the usage will be explained, and all necessary dependencies will be laid out.

# **Dependencies**

* PyQt5
* playsound
* gtts
* fpdf

# **Commands**

* The _"END" command:_ the trainer will only consider vocabulary before this marker

# **Usage**

* **The main window**
  * _random mode:_ words are picked randomly
  * _linear mode:_ words are picked randomly, but every word will have been tested before a particular word is tested for the second time
* The settings window
 * _language 1:_ the first language to be tested
 * _language 2:_ the second language to be tested
 * _round length:_ the amount of correct answers needed for the score to increase - see the main window
* The editor window
 * to _add vocabulary_, simply fill the entries and click on the add-button, or **press enter**
 * to _remove vocabulary_, simply select the word you would like to remove and click on the remove-button, or **press del**
 * to _save changes to a word_, simply click on the save-button, or press **Strg+S**
 * to _add END_, simply right-click on a word and **select ""Add END**
 * to _edit vocabulary for a particular pair of languages_, simply select the desired pair via **the menu on the bottom right**
 * to _change switch between languages_, simply **press the button on the bottom right**
