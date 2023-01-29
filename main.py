import sys

import bcrypt
from PyQt5 import QtSvg
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import *

import handleUser

WIN_SIZE = 500
with open("resources/css/styles.css", 'r') as f:
    css = f.read()

error = 0


def popout():
    p.show()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initial
        self.setWindowTitle("Password Manager")
        self.setFixedSize(WIN_SIZE, WIN_SIZE)
        self.setStyleSheet(" background-color: #fff; ")

        # central widget
        self.centralwidget = QStackedWidget()
        self.setCentralWidget(self.centralwidget)
        self.main_window = QWidget(self)

        # Creating Layouts
        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        middleLayout = QVBoxLayout()
        bottomLayout = QVBoxLayout()

        # Layouts alignment and spacing
        outerLayout.setAlignment(Qt.AlignCenter)
        middleLayout.setAlignment(Qt.AlignCenter)
        middleLayout.setSpacing(30)
        bottomLayout.setAlignment(Qt.AlignCenter)

        # creating widgets
        self._createLabel()
        self._createButtons()

        # adding created widgets
        topLayout.addWidget(self.label)
        middleLayout.addWidget(self.loginBtn)
        middleLayout.addWidget(self.signupBtn)

        # adding layouts to outerlayout and setting central Layout
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(middleLayout)
        outerLayout.addLayout(bottomLayout)
        self.main_window.setLayout(outerLayout)
        self.centralwidget.addWidget(self.main_window)

    def signed(self):
        popout()
        self.centralwidget.setCurrentWidget(self.main_window)

    # switch between widgets
    def back(self):
        self.centralwidget.setCurrentWidget(self.main_window)

    def signupView(self):
        signup_widget = signUpWidget(self)
        signup_widget.cancelBtn.clicked.connect(self.back)
        self.centralwidget.addWidget(signup_widget)
        self.centralwidget.setCurrentWidget(signup_widget)

    def loginView(self):
        login_widget = logInWidget(self)
        login_widget.cancelBtn.clicked.connect(self.back)
        self.centralwidget.addWidget(login_widget)
        self.centralwidget.setCurrentWidget(login_widget)

    def _createLabel(self):
        self.label = QLabel("Password Manager")
        self.label.setObjectName("mainLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(300, 200)
        self.label.setStyleSheet(css)

    def _createButtons(self):
        self.loginBtn = QPushButton("Log In")
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.setFixedSize(150, 50)
        self.signupBtn = QPushButton("Sign up")
        self.signupBtn.setObjectName("signupBtn")
        self.signupBtn.setFixedSize(150, 50)
        self.signupBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.signupBtn.clicked.connect(self.signupView)
        self.loginBtn.clicked.connect(self.loginView)
        self.loginBtn.setStyleSheet(css)
        self.signupBtn.setStyleSheet(css)


class signUpWidget(QWidget):
    def __init__(self, parent=None):
        super(signUpWidget, self).__init__(parent)
        self.setFixedSize(350, 350)
        self.parent = parent
        # create layouts
        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        formLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        # layouts alignment
        outerLayout.setAlignment(Qt.AlignCenter)
        formLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.setAlignment(Qt.AlignRight)

        # create Form
        self._signupForm()

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
        outerLayout.addSpacing(60)
        outerLayout.addLayout(bottomLayout)
        self.setLayout(outerLayout)

    def _signupForm(self):
        self.errorLabel = QLabel("")
        self.infoLabel = QLabel("Create Profile")
        self.labelName = QLabel("Name:")
        self.labelPassword = QLabel("Password:")
        self.name = QLineEdit()
        self.password = QLineEdit()
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

    def handleInputsChange(self):
        if self.errorLabel.text() != "":
            self.errorLabel.setText("")

    def errorUserExists(self, value):
        self.errorLabel.setText("User {} already exists!".format(value))

    def invalidCredentials(self):
        if self.name.text() == "" or self.password.text() == "":
            self.errorLabel.setText("Invalid credentials")
            return True
        return False

    def handleErrors(self, user):
        if not self.invalidCredentials():
            if not handleUser.userExists(user):
                handleUser.createUserFiles(user)
                return True
            else:
                self.errorUserExists(user)
                return False
        return False

    def _submitForm(self):
        user = self.name.text()
        if self.handleErrors(user):
            password = self.password.text()
            try:
                key_one = handleUser.create_firstKey()
                # print(key_one)
                key_two = handleUser.create_secondKey(password)
                # print(key_two)
                encrypted_first_key = handleUser.encrypt_firstKey(key_one, key_two)
                # print(encrypted_first_key)
                salt = handleUser.generateRandomSalt()
                # print(salt)
                hashed_password = handleUser.hash_password(password.encode(), salt)
                # print(hashed_password)
                handleUser.write_firstKey(user, encrypted_first_key)
                handleUser.write_info(user, hashed_password, salt)
                self.parent.signed()
            except error:
                return error


class logInWidget(QWidget):
    def __init__(self, parent=None):
        super(logInWidget, self).__init__(parent)
        self.setFixedSize(350, 350)

        # create layouts
        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        formLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        # layout alignment
        outerLayout.setAlignment(Qt.AlignCenter)
        formLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.setAlignment(Qt.AlignRight)

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
        outerLayout.addSpacing(60)
        outerLayout.addLayout(bottomLayout)
        self.setLayout(outerLayout)

    def _logInForm(self):
        self.errorLabel = QLabel("")
        self.infoLabel = QLabel("Log In")
        self.labelName = QLabel("Name:")
        self.labelPassword = QLabel("Password:")
        self.name = QLineEdit()
        self.password = QLineEdit()
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

    def createErrorLabel(self):
        self.errorLabel.setText("Invalid credentials!")

    def handleInputsChange(self):
        if self.errorLabel.text() != "":
            self.errorLabel.setText("")

    def invalidCredentials(self):
        if self.name.text() == "" or self.password.text() == "":
            self.errorLabel.setText("Invalid credentials")
            return True
        return False

    def _submitForm(self):
        user = self.name.text()
        if not self.invalidCredentials():
            if handleUser.userExists(user):
                password = self.password.text()
                if handleUser.compare_passwords(user, password):
                    print("zalogowano")
                else:
                    print("zle haslo")


class popoutWidget(QDialog):
    def __init__(self):
        super(popoutWidget, self).__init__()
        self.setModal(True)
        # self.setFixedSize(180, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Successfully created profile.")
        self.label.setObjectName("signedPopoutLabel")
        self.label.setStyleSheet(css)
        layout.addWidget(self.label)
        self.setLayout(layout)


# user_info = []
# # add rows
# user_info.append({"Name:": "dzang", "Password": 123})
# p = "123"
# encrypted = handleUser.encrypt_data(p, user_info)
# print(encrypted)
# decrypted = handleUser.decrypt_data(p, encrypted)
# print(decrypted)
#
# salt = b'$2b$12$./wcHVff.h/qJd1sxo9dau'
# print("salt", salt)
# p = b'OSDkoasd8721nzc#$asdlqwpo'
# p = handleUser.hash_password(p, salt)
# handleUser.write_info("dzang", p, salt)
# p = b'OSDkoasd8721nzc#$asdlqwpo'
# handleUser.compare_passwords("dzang", p)
if __name__ == "__main__":
    handleUser.initializeDirectory()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    p = popoutWidget()
    sys.exit(app.exec_())
