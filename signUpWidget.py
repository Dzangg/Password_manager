from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import handleUser

# GLOBAL VARIABLES & FUNCTIONS

WIN_SIZE = 500

with open("resources/css/styles.css", 'r') as f:
    css = f.read()


class signUpWidget(QWidget):
    '''
    A class to represent signup layout
        Parameters:
            QWidget : widget

        Functions:

            _signupForm()

            handleInputsChange()

            errorUserExists()

            _invalidCredentials()

            _isValid()

            _initializeProfile()

            _submitForm()

    '''

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
        outerLayout.addLayout(bottomLayout)
        self.setLayout(outerLayout)

    # signup form creation
    def _signupForm(self):
        self.errorLabel = QLabel("")
        self.infoLabel = QLabel("Create Profile")
        self.labelName = QLabel("Name:")
        self.labelPassword = QLabel("Password:")
        self.name = QLineEdit()
        self.password = QLineEdit()

        self.name.setObjectName("input")
        self.name.setStyleSheet(css)
        self.password.setObjectName("input")
        self.password.setStyleSheet(css)
        self.name.textChanged.connect(self.handleInputsChange)
        self.password.setEchoMode(QLineEdit.Password)

        self.acceptBtn = QPushButton("Ok")
        self.cancelBtn = QPushButton("Cancel")

        self.name.setFixedSize(200, 20)
        self.password.setFixedSize(200, 20)
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

    # switch error warning label text
    def handleInputsChange(self):
        if self.errorLabel.text() != "":
            self.errorLabel.setText("")

    # user exists error
    def errorUserExists(self, value):
        self.errorLabel.setText("User {} already exists!".format(value))

    # invalid credentials error
    def _invalidCredentials(self):
        self.errorLabel.setText("Invalid credentials")

    # is user signup valid
    def _isValid(self, user):
        if self.name.text() == "" or self.password.text() == "":
            self._invalidCredentials()
            return False
        else:
            if not handleUser.userExists(user):
                handleUser.createUserFiles(user)
                return True
            else:
                self.errorUserExists(user)
                return False

    # user profile creation
    def _initializeProfile(self, user):
        password = self.password.text()
        try:
            key_one = handleUser.create_firstKey()
            key_two = handleUser.create_secondKey(password)
            encrypted_first_key = handleUser.encrypt_firstKey(key_one, key_two)
            salt = handleUser.generateRandomSalt()
            hashed_password = handleUser.hash_password(password.encode(), salt)
            handleUser.write_firstKey(user, encrypted_first_key)
            handleUser.write_info(user, hashed_password, salt)
            self.parent.signed()
        except:
            handleUser.del_user(user)
            print("Signup error occured")

    # submit form
    def _submitForm(self):
        user = self.name.text()
        if self._isValid(user):
            self._initializeProfile(user)
