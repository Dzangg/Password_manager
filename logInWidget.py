from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import handleUser

# GLOBAL VARIABLES & FUNCTIONS

WIN_SIZE = 500

with open("resources/css/styles.css", 'r') as f:
    css = f.read()


class logInWidget(QWidget):
    '''
    A class to represent logIn layout
        Parameters:
            QWidget : widget

        Functions:

            _loginForm()

            _createErrorLabel()

            _handleInputsChange()

            _isValid()

            _invalidCredentials()

            _submitForm()

    '''

    def __init__(self, parent=None):
        super(logInWidget, self).__init__(parent)
        self.setMinimumSize(WIN_SIZE, WIN_SIZE)
        self.pr = parent

        # create layouts
        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        formLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        # layout alignment
        topLayout.setAlignment(Qt.AlignCenter)
        formLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.setAlignment(Qt.AlignCenter)
        outerLayout.setAlignment(Qt.AlignCenter)

        # create Form
        self._logInForm()

        # add widgets to layouts
        topLayout.addWidget(self.infoLabel)
        formLayout.addWidget(self.labelName)
        formLayout.addWidget(self.name)
        formLayout.addWidget(self.labelPassword)
        formLayout.addWidget(self.password)
        formLayout.addWidget(self.errorLabel)
        bottomLayout.addWidget(self.acceptBtn)
        bottomLayout.addWidget(self.cancelBtn)

        # add layouts to outer layout
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(formLayout)
        outerLayout.addLayout(bottomLayout)
        self.setLayout(outerLayout)

    # login form creation
    def _logInForm(self):
        self.errorLabel = QLabel("")
        self.infoLabel = QLabel("Log In")
        self.labelName = QLabel("Name:")
        self.labelPassword = QLabel("Password:")
        self.name = QLineEdit()
        self.name.setObjectName("input")
        self.name.setStyleSheet(css)
        self.password = QLineEdit()
        self.password.setObjectName("input")
        self.password.setStyleSheet(css)
        self.name.setFixedSize(200, 20)
        self.password.setFixedSize(200, 20)
        self.password.setEchoMode(QLineEdit.Password)

        self.name.textChanged.connect(self.handleInputsChange)

        self.acceptBtn = QPushButton("Ok")
        self.cancelBtn = QPushButton("Cancel")

        self.acceptBtn.setFixedSize(100, 40)
        self.cancelBtn.setFixedSize(100, 40)

        self.acceptBtn.setObjectName("okButton")
        self.cancelBtn.setObjectName("cancelButton")
        self.infoLabel.setObjectName("createProfileLabel")

        self.acceptBtn.setStyleSheet(css)
        self.cancelBtn.setStyleSheet(css)
        self.infoLabel.setStyleSheet(css)

        self.acceptBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.acceptBtn.clicked.connect(self._submitForm)

    # error label
    def createErrorLabel(self):
        self.errorLabel.setText("Invalid credentials!")

    # switch warning text
    def handleInputsChange(self):
        if self.errorLabel.text() != "":
            self.errorLabel.setText("")

    # validation
    def isValid(self):
        if self.name.text() == "" or self.password.text() == "":
            return False
        return True

    # invalid credentials error
    def invalidCredentials(self):
        self.errorLabel.setText("Invalid credentials")

    # submit form
    def _submitForm(self):
        user = self.name.text()
        if self.isValid():
            if handleUser.userExists(user):
                password = self.password.text()
                if handleUser.compare_passwords(user, password):
                    self.pr.connect_user(user, password)
                else:
                    self.invalidCredentials()
            else:
                self.invalidCredentials()
        else:
            self.invalidCredentials()
