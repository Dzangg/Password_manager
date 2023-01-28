import sys
import os
from PyQt5 import QtSvg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import *

WIN_SIZE = 500
with open("resources/css/styles.css", 'r') as f:
    css = f.read()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(WIN_SIZE, WIN_SIZE)
        self.setStyleSheet(" background-color: #fff; ")

        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        middleLayout = QVBoxLayout()

        outerLayout.setAlignment(Qt.AlignCenter)
        middleLayout.setAlignment(Qt.AlignCenter)
        middleLayout.setSpacing(30)

        self._createLabel()
        self._createButtons()

        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)

        topLayout.addWidget(self.label)
        middleLayout.addWidget(self.loginBtn)
        middleLayout.addWidget(self.signupBtn)

        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(middleLayout)
        centralwidget.setLayout(outerLayout)

    def _createLabel(self):
        self.label = QLabel("Password Manager")
        self.label.setObjectName("mainLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(300, 200)
        self.label.setStyleSheet(css)
        return self.label

    def _createButtons(self):
        self.loginBtn = QPushButton("Log In")
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.setFixedSize(150, 50)
        self.signupBtn = QPushButton("Sign up")
        self.signupBtn.setObjectName("signupBtn")
        self.signupBtn.setFixedSize(150, 50)
        self.signupBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.signupBtn.clicked.connect(self.on_button_signUp)
        self.loginBtn.clicked.connect(self.on_button_logIn)

        self.loginBtn.setStyleSheet(css)
        self.signupBtn.setStyleSheet(css)

    def on_button_logIn(self):
        formLogIn = form("logIn")

    def on_button_signUp(self):
        self.setCentralWidget(signUp())


class signUp(QWidget):
    def __init__(self):
        super().__init__()
        # self.setModal(True)  # disable interaction with prev window until this one close
        self.setFixedSize(350, 350)
        self.main_window = Window()
        self.appLabel = self.main_window.label

        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        formLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        outerLayout.setAlignment(Qt.AlignCenter)
        formLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.setAlignment(Qt.AlignRight)

        self._createForm()

        topLayout.addWidget(self.appLabel)
        formLayout.addWidget(self.labelName)
        formLayout.addWidget(self.name)
        formLayout.addWidget(self.labelPassword)
        formLayout.addWidget(self.password)
        bottomLayout.addWidget(self.acceptBtn)
        bottomLayout.addWidget(self.cancelBtn)

        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(formLayout)
        outerLayout.addSpacing(100)
        outerLayout.addLayout(bottomLayout)
        self.setLayout(outerLayout)

    def _createForm(self):
        self.labelName = QLabel("Name:")
        self.labelPassword = QLabel("Password:")
        self.name = QLineEdit()
        self.password = QLineEdit()
        self.name.setFixedSize(200, 20)
        self.password.setFixedSize(200, 20)
        self.password.setEchoMode(QLineEdit.Password)

        self.acceptBtn = QPushButton("Ok")
        self.cancelBtn = QPushButton("Cancel")

        self.acceptBtn.setFixedSize(100, 40)
        self.cancelBtn.setFixedSize(100, 40)

        self.acceptBtn.setObjectName("okButton")
        self.cancelBtn.setObjectName("cancelButton")

        self.acceptBtn.setStyleSheet(css)
        self.cancelBtn.setStyleSheet(css)

        self.acceptBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.acceptBtn.clicked.connect(self._submitForm)
        self.cancelBtn.clicked.connect(self._cancelForm)

    def _submitForm(self):
        pass

    def _cancelForm(self):
        self.setCentralWidget(signUp())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()

    window.show()

    sys.exit(app.exec_())
