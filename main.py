import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
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
        self.main_window.setWindowFlags(Qt.FramelessWindowHint)
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
        self.setMinimumSize(0, 0)

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

    def _submitForm(self):
        user = self.name.text()
        if self.isValid(user):
            self._initializeProfile(user)


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
        outerLayout.addLayout(bottomLayout)
        self.setLayout(outerLayout)

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
        self.outerlayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.labelLayout = QHBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.tableLayout = QVBoxLayout()
        self.toolsLayout = QHBoxLayout()
        self.logoutLayout = QHBoxLayout()

        self.tableWidget = QTableWidget()

        self.outerlayout.setAlignment(Qt.AlignCenter)
        self.headerLayout.setAlignment(Qt.AlignLeft)
        self.labelLayout.setAlignment(Qt.AlignLeft)
        self.inputLayout.setAlignment(Qt.AlignLeft)
        self.btnLayout.setAlignment(Qt.AlignLeft)
        self.tableLayout.setAlignment(Qt.AlignLeft)
        self.logoutLayout.setAlignment(Qt.AlignRight)

        self.userLabel = QLabel("User: ")
        self.userLabel.setObjectName("userLabel")
        self.userLabel.setStyleSheet(css)
        self.userNameLabel = QLabel("")
        self.userNameLabel.setObjectName("userNameLabel")
        self.userNameLabel.setStyleSheet(css)

        self._doubleCheck(user, password)
        self._showTable()
        self._createInputData()
        self._createTools()

        self.headerLayout.addWidget(self.userLabel)
        self.headerLayout.addWidget(self.userNameLabel)

        self.outerlayout.addLayout(self.headerLayout)
        self.outerlayout.addLayout(self.labelLayout)
        self.outerlayout.addLayout(self.inputLayout)
        self.outerlayout.addLayout(self.btnLayout)
        self.tableLayout.addWidget(self.tableWidget)
        self.outerlayout.addLayout(self.tableLayout)
        self.outerlayout.addLayout(self.toolsLayout)
        self.toolsLayout.addLayout(self.logoutLayout)

        self.setLayout(self.outerlayout)

    def _doubleCheck(self, user, password):
        isValid = handleUser.compare_passwords(user, password)
        if isValid:
            self.user = user
            self.user_password = password
            self.userNameLabel.setText(user)
        else:
            self.close()

    def _createInputData(self):
        self.inputNameLabel = QLabel("Page:")
        self.inputLoginLabel = QLabel("Login:")
        self.inputPasswordLabel = QLabel("Password:")
        self.inputUrlLabel = QLabel("Url:")
        self.inputNoteLabel = QLabel("Note:")
        self.addRowBtn = QPushButton("Add")

        self.inputNameLabel.setObjectName("label")
        self.inputNameLabel.setStyleSheet(css)
        self.inputLoginLabel.setObjectName("label")
        self.inputLoginLabel.setStyleSheet(css)
        self.inputPasswordLabel.setObjectName("label")
        self.inputPasswordLabel.setStyleSheet(css)
        self.inputUrlLabel.setObjectName("label")
        self.inputUrlLabel.setStyleSheet(css)
        self.inputNoteLabel.setObjectName("label")
        self.inputNoteLabel.setStyleSheet(css)
        self.addRowBtn.setObjectName("addRowBtn")
        self.addRowBtn.setStyleSheet(css)

        self.addRowBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.inputNameLabel.setFixedSize(130, 20)
        self.inputLoginLabel.setFixedSize(130, 20)
        self.inputPasswordLabel.setFixedSize(130, 20)
        self.inputUrlLabel.setFixedSize(130, 20)
        self.inputNoteLabel.setFixedSize(130, 20)

        self.inputName = QLineEdit()
        self.inputLogin = QLineEdit()
        self.inputPassword = QLineEdit()
        self.inputUrl = QLineEdit()
        self.inputNote = QLineEdit()

        self.inputName.setObjectName("input")
        self.inputName.setStyleSheet(css)
        self.inputLogin.setObjectName("input")
        self.inputLogin.setStyleSheet(css)
        self.inputPassword.setObjectName("input")
        self.inputPassword.setStyleSheet(css)
        self.inputUrl.setObjectName("input")
        self.inputUrl.setStyleSheet(css)
        self.inputNote.setObjectName("input")
        self.inputNote.setStyleSheet(css)

        self.inputName.setFixedSize(130, 20)
        self.inputLogin.setFixedSize(130, 20)
        self.inputPassword.setFixedSize(130, 20)
        self.inputUrl.setFixedSize(130, 20)
        self.inputNote.setFixedSize(130, 20)
        self.addRowBtn.setFixedSize(60, 40)

        self.addRowBtn.clicked.connect(self._addNewData)

        self.labelLayout.addWidget(self.inputNameLabel)
        self.labelLayout.addWidget(self.inputLoginLabel)
        self.labelLayout.addWidget(self.inputPasswordLabel)
        self.labelLayout.addWidget(self.inputUrlLabel)
        self.labelLayout.addWidget(self.inputNoteLabel)

        self.btnLayout.addWidget(self.addRowBtn)

        self.inputLayout.addWidget(self.inputName)
        self.inputLayout.addWidget(self.inputLogin)
        self.inputLayout.addWidget(self.inputPassword)
        self.inputLayout.addWidget(self.inputUrl)
        self.inputLayout.addWidget(self.inputNote)

    def _createTools(self):
        self.editBtn = QPushButton("Edit")
        self.editBtn.clicked.connect(self._switchTableEdit)
        self.applyBtn = QPushButton("Apply")
        self.cancelBtn = QPushButton("Cancel")
        self.randomPasswordBtn = QPushButton("Generate password")
        self.randomPasswordBtn.clicked.connect(self._generatePassword)
        self.deleteBtn = QPushButton("Delete row")
        self.deleteBtn.setDisabled(True)
        self.deleteBtn.clicked.connect(self._deleteSelectedRow)
        self.logoutBtn = QPushButton("Exit")
        self.logoutBtn.clicked.connect(lambda: exit())
        self.logoutBtn.setObjectName("logoutBtn")
        self.logoutBtn.setStyleSheet(css)

        self.randomPasswordBtn.setObjectName("randomPasswordBtn")
        self.randomPasswordBtn.setStyleSheet(css)
        self.editBtn.setObjectName("editBtn")
        self.editBtn.setStyleSheet(css)
        self.applyBtn.setObjectName("applyBtn")
        self.applyBtn.setStyleSheet(css)
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.setStyleSheet(css)
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setStyleSheet(css)

        self.randomPasswordBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.applyBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.logoutBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.randomPasswordBtn.setFixedSize(200, 40)
        self.editBtn.setFixedSize(60, 40)
        self.applyBtn.setFixedSize(130, 40)
        self.cancelBtn.setFixedSize(130, 40)
        self.deleteBtn.setFixedSize(130, 40)
        self.logoutBtn.setFixedSize(100, 40)

        self.applyBtn.setDisabled(True)
        self.cancelBtn.setDisabled(True)

        self.applyBtn.clicked.connect(self._applyAction)
        self.cancelBtn.clicked.connect(self._cancelAction)

        self.btnLayout.addWidget(self.deleteBtn)
        self.btnLayout.addWidget(self.randomPasswordBtn)

        self.toolsLayout.addWidget(self.editBtn)
        self.toolsLayout.addWidget(self.applyBtn)
        self.toolsLayout.addWidget(self.cancelBtn)
        self.logoutLayout.addWidget(self.logoutBtn)

    def _showTable(self):
        # get data from file
        data = handleUser.read_data(self.user, self.user_password)
        if data is False:
            return False

        # Row count
        self.tableWidget.setRowCount(len(data))

        # Column count
        self.tableWidget.setColumnCount(len(data[0]))

        # writing data to table
        self.tableWidget.setHorizontalHeaderLabels(data[0].keys())
        for i, item in enumerate(data):
            for j, (key, value) in enumerate(item.items()):
                self.tableWidget.setItem(i, j, QTableWidgetItem(value))

        # set to read only
        rows = len(data)
        columns = len(data[0])
        for i in range(rows):
            for j in range(columns):
                item = self.tableWidget.item(i, j)
                item.setFlags(item.flags() & Qt.ItemIsEnabled)
        self.tableWidget.setColumnWidth(0, 130)
        self.tableWidget.setColumnWidth(1, 130)
        self.tableWidget.setColumnWidth(2, 130)
        self.tableWidget.setColumnWidth(3, 130)
        self.tableWidget.setColumnWidth(4, 137)

    def _addNewData(self):
        data = {}
        data["Page"] = self.inputName.text()
        data["Login"] = self.inputLogin.text()
        data["Password"] = self.inputPassword.text()
        data["Url"] = self.inputUrl.text()
        data["Note"] = self.inputNote.text()

        # write data to db
        handleUser.append_data(self.user, self.user_password, data)
        self._showTable()

    def _generatePassword(self):
        random_password = handleUser.generate_random_password()
        self.inputPassword.setText(random_password)
        clipboard = app.clipboard()
        clipboard.setText(random_password)

    def _writeEditData(self):
        headers = ["Page", "Login", "Password", "Url", "Note"]
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        data = []
        for i in range(0, rows):
            temp = {}
            for j in range(0, columns):
                item = self.tableWidget.item(i, j)
                temp[headers[j]] = item.text()
            data.append(temp)

        handleUser.delete_data(self.user)
        handleUser.write_data(self.user, self.user_password, data)

    def _deleteSelectedRow(self):
        selected = self.tableWidget.selectedItems()
        if selected:
            row = selected[0].row()
            self.tableWidget.removeRow(row)

    def _applyAction(self):
        self._writeEditData()
        self._switchTableLock()

    def _cancelAction(self):
        self._showTable()
        self._switchTableLock()

    def _switchTableEdit(self):
        self.editBtn.setDisabled(True)
        self.addRowBtn.setDisabled(True)
        self.deleteBtn.setDisabled(False)
        self.applyBtn.setDisabled(False)
        self.cancelBtn.setDisabled(False)
        # unlock
        data = handleUser.read_data(self.user, self.user_password)
        rows = len(data)
        columns = len(data[0])
        for i in range(rows):
            for j in range(columns):
                item = self.tableWidget.item(i, j)
                item.setFlags(item.flags() | ~Qt.ItemIsEnabled)

    def _switchTableLock(self):
        self.editBtn.setDisabled(False)
        self.addRowBtn.setDisabled(False)
        self.deleteBtn.setDisabled(True)
        self.applyBtn.setDisabled(True)
        self.cancelBtn.setDisabled(True)

        # lock
        data = handleUser.read_data(self.user, self.user_password)
        rows = len(data)
        columns = len(data[0])
        for i in range(rows):
            for j in range(columns):
                item = self.tableWidget.item(i, j)
                item.setFlags(item.flags() & Qt.ItemIsEnabled)


if __name__ == "__main__":
    handleUser.initializeDirectory()
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowIcon(QIcon("icon.png"))
    window.show()
    p = popoutWidget()
    sys.exit(app.exec_())
