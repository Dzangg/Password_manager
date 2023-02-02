from PyQt5.QtWidgets import *

with open("resources/css/styles.css", 'r') as f:
    css = f.read()


# signup popout widget
class popoutWidget(QDialog):
    '''
    A class to represent popout widget

        Parameters:
                QDialog : widget

    '''

    def __init__(self):
        super(popoutWidget, self).__init__()
        self.setModal(True)
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Successfully created profile.")
        self.label.setObjectName("signedPopoutLabel")
        self.label.setStyleSheet(css)
        layout.addWidget(self.label)
        self.setLayout(layout)
