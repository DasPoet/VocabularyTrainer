from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QMenu


class ClickLabel(QLabel):
    """ PyQt5 Label (QLabel) that can be clicked on."""

    left_clicked = pyqtSignal()
    right_clicked = pyqtSignal()

    def mousePressEvent(self, event):
        """Override the mousePressEvent() function of QLabel by adding the option to add functionality to a left mouse
        button press event via a custom pyqtSignal.
        """

        self.left_clicked.emit()
        QLabel.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        """Override the contextMenuEvent() function of QLabel by adding a customised context menu that allows the
        user to:
                I) add the "END" command to the vocabulary file
                II) add functionality to a right mouse button press event via a custom pyqtSignal.
        """

        self.setStyleSheet("color:blue")
        menu = QMenu(self)
        custom_action = menu.addAction("Add END")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == custom_action:
            self.right_clicked.emit()
