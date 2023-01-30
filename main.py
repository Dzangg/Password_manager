import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import *

import handleUser

WIN_SIZE = 500
with open("resources/css/styles.css", 'r') as f:
    css = f.read()


def popout():
    p.show()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initial
        self.setWindowTitle("Password Manager")
        self.setMinimumSize(WIN_SIZE, WIN_SIZE)
        self.setStyleSheet(" background-color: #fff; ")

        # central widget
        self.centralwidget = QStackedWidget()
        self.setCentralWidget(self.centralwidget)
        self.main_window = QWidget(self)

        # Creating Layouts
        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        middleLayout = QVBoxLayout()

        # Layouts alignment and spacing
        topLayout.setAlignment(Qt.AlignCenter)
        outerLayout.setAlignment(Qt.AlignCenter)
        middleLayout.setAlignment(Qt.AlignCenter)
        middleLayout.setSpacing(30)

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
        self.main_window.setLayout(outerLayout)
        self.centralwidget.addWidget(self.main_window)

    def connect_user(self, user, password):
        panel = userPanelWidget(user, password)
        self.centralwidget.addWidget(panel)
        self.centralwidget.setCurrentWidget(panel)

    def signed(self):
        popout()
        self.centralwidget.setCurrentWidget(self.main_window)
        self.centralwidget.removeWidget(self.signup_widget)

    # switch between widgets
    def back_sign(self):
        self.centralwidget.setCurrentWidget(self.main_window)
        self.centralwidget.removeWidget(self.signup_widget)

    def back_login(self):
        self.centralwidget.setCurrentWidget(self.main_window)
        self.centralwidget.removeWidget(self.login_widget)

    def signupView(self):
        self.signup_widget = signUpWidget(self)
        self.signup_widget.cancelBtn.clicked.connect(self.back_sign)
        self.centralwidget.addWidget(self.signup_widget)
        self.centralwidget.setCurrentWidget(self.signup_widget)

    def loginView(self):
        self.login_widget = logInWidget(self)
        self.login_widget.cancelBtn.clicked.connect(self.back_login)
        self.centralwidget.addWidget(self.login_widget)
        self.centralwidget.setCurrentWidget(self.login_widget)

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
        self.parent = parent
        self.setMinimumSize(WIN_SIZE, WIN_SIZE)
        # create layouts
        outerLayout = QVBoxLayout()
        topLayout = QVBoxLayout()
        formLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        # layouts alignment
        topLayout.setAlignment(Qt.AlignCenter)
        formLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.setAlignment(Qt.AlignCenter)
        outerLayout.setAlignment(Qt.AlignCenter)

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
        # outerLayout.addSpacing(100)
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
        self.errorLabel.setText("Invalid credentials")

    def isValid(self, user):
        if self.name.text() == "" or self.password.text() == "":
            self.invalidCredentials()
            return False
        else:
            if not handleUser.userExists(user):
                handleUser.createUserFiles(user)
                return True
            else:
                self.errorUserExists(user)
                return False

    def _initializeProfileCreation(self, user):
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
        except:
            handleUser.del_user(user)
            print("Signup error occured")

    def _submitForm(self):
        user = self.name.text()
        if self.isValid(user):
            self._initializeProfileCreation(user)


class logInWidget(QWidget):
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
        # outerLayout.addSpacing(100)
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

    def isValid(self):
        if self.name.text() == "" or self.password.text() == "":
            return False
        return True

    def invalidCredentials(self):
        self.errorLabel.setText("Invalid credentials")

    def _initializeLogin(self):
        pass

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


class popoutWidget(QDialog):
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


class userPanelWidget(QWidget):
    def __init__(self, user, password):
        super(userPanelWidget, self).__init__()
        self.emptyData = False

        self.outerlayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.labelLayout = QHBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.toolsLayout = QHBoxLayout()
        self.tableLayout = QVBoxLayout()

        self.outerlayout.setAlignment(Qt.AlignCenter)
        self.headerLayout.setAlignment(Qt.AlignLeft)

        self.userLabel = QLabel("User: ")
        self.userLabel.setObjectName("userLabel")
        self.userLabel.setStyleSheet(css)
        self.userNameLabel = QLabel("")
        self.userNameLabel.setObjectName("userNameLabel")
        self.userNameLabel.setStyleSheet(css)

        self._doubleCheck(user, password)
        self._createTable()
        self._createInputData()
        self._createTools()

        self.headerLayout.addWidget(self.userLabel)
        self.headerLayout.addWidget(self.userNameLabel)

        self.outerlayout.addLayout(self.headerLayout)
        self.outerlayout.addLayout(self.labelLayout)
        self.outerlayout.addLayout(self.inputLayout)
        self.outerlayout.addLayout(self.toolsLayout)
        self.tableLayout.addWidget(self.tableWidget)
        self.outerlayout.addLayout(self.tableLayout)
        self.setLayout(self.outerlayout)

    def _doubleCheck(self, user, password):
        isValid = handleUser.compare_passwords(user, password)
        if isValid:
            self.user = user
            self.user_password = password
            self.userNameLabel.setText(user)
        else:
            self.close()

    def _createTools(self):
        self.unlockEditBtn = QPushButton("Edit")
        self.unlockEditBtn.clicked.connect(self._switchTableLock)
        self.applyBtn = QPushButton("Apply")
        self.cancelBtn = QPushButton("Cancel")

        self.randomPasswordBtn = QPushButton("Generate password")
        self.randomPasswordBtn.clicked.connect(self._generatePassword)
        self.generatedPassword = QLineEdit()
        self.generatedPassword.setReadOnly(True)

        self.toolsLayout.addWidget(self.unlockEditBtn)
        self.toolsLayout.addWidget(self.applyBtn)
        self.toolsLayout.addWidget(self.cancelBtn)
        self.toolsLayout.addWidget(self.randomPasswordBtn)

    def _createInputData(self):
        self.inputNameLabel = QLabel("Name:")
        self.inputNameLabel.setFixedSize(90, 20)
        self.inputNameLabel.setObjectName("in")
        self.inputNameLabel.setStyleSheet(css)
        self.inputLoginLabel = QLabel("Login:")
        self.inputPasswordLabel = QLabel("Password:")
        self.inputUrlLabel = QLabel("Url:")
        self.inputNoteLabel = QLabel("Note:")
        self.addRowBtn = QPushButton("Add")

        self.inputName = QLineEdit()
        self.inputLogin = QLineEdit()
        self.inputPassword = QLineEdit()
        self.inputUrl = QLineEdit()
        self.inputNote = QLineEdit()

        self.labelLayout.addWidget(self.inputNameLabel)
        self.labelLayout.addWidget(self.inputLoginLabel)
        self.labelLayout.addWidget(self.inputPasswordLabel)
        self.labelLayout.addWidget(self.inputUrlLabel)
        self.labelLayout.addWidget(self.inputNoteLabel)
        self.labelLayout.addWidget(self.addRowBtn)

        self.inputLayout.addWidget(self.inputName)
        self.inputLayout.addWidget(self.inputLogin)
        self.inputLayout.addWidget(self.inputPassword)
        self.inputLayout.addWidget(self.inputUrl)
        self.inputLayout.addWidget(self.inputNote)

    def _getUserData(self):
        data = handleUser.read_data(self.user, self.user_password)
        if data is False:
            self.emptyData = True
            return False

    def _createTable(self):
        self.tableWidget = QTableWidget()
        self._getUserData()

    def _generatePassword(self):
        random_password = handleUser.generate_random_password()
        self.generatedPassword.setText(random_password)

    def _switchTableLock(self):
        pass


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
