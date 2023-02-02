from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import handleUser

# GLOBAL VARIABLES & FUNCTIONS

WIN_SIZE = 500

with open("resources/css/styles.css", 'r') as f:
    css = f.read()


class userPanelWidget(QWidget):
    '''
    A class to represent User panel interface.

            Parameters:
                    QWidget : widget

            Functions:

                    _doubleCHeck(user, password)

                   _showTable()

                   _createInputData()

                   _createTools()

                   _addNewData()

                   _generatePassword()

                   _writeEditData()

                   _deleteSelectedRow()

                   _applyAction()

                   _cancelAction()

                   _switchTableEdit()

                   _switchTableLock()

    '''

    def __init__(self, user, password, parent=None):
        super(userPanelWidget, self).__init__(parent)
        self.parent = parent
        # layouts creation
        self.outerlayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.labelLayout = QHBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.tableLayout = QVBoxLayout()
        self.toolsLayout = QHBoxLayout()
        self.logoutLayout = QHBoxLayout()

        # table creation
        self.tableWidget = QTableWidget()

        # layouts alignments
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

        self.headerLayout.addWidget(self.userLabel)
        self.headerLayout.addWidget(self.userNameLabel)

        # double verify user
        self._doubleCheck(user, password)
        # show user data in table
        self._showTable()
        # create input labels and buttons
        self._createInputData()
        # create tools inputs etc
        self._createTools()

        # add layouts to outer layout
        self.outerlayout.addLayout(self.headerLayout)
        self.outerlayout.addLayout(self.labelLayout)
        self.outerlayout.addLayout(self.inputLayout)
        self.outerlayout.addLayout(self.btnLayout)
        self.tableLayout.addWidget(self.tableWidget)
        self.outerlayout.addLayout(self.tableLayout)
        self.outerlayout.addLayout(self.toolsLayout)
        self.toolsLayout.addLayout(self.logoutLayout)

        self.setLayout(self.outerlayout)

    # double validation
    def _doubleCheck(self, user, password):
        isValid = handleUser.compare_passwords(user, password)
        if isValid:
            self.user = user
            self.user_password = password
            self.userNameLabel.setText(user)
        else:
            self.close()

    # create labels and buttons
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

    # create tools buttons etc
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

    # show user data on table
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

    # add row
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

    # generate random password
    def _generatePassword(self):
        random_password = handleUser.generate_random_password()
        self.inputPassword.setText(random_password)
        self.parent.copyToClipboard(random_password)

    # write edited data
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

    # on selected row deletion
    def _deleteSelectedRow(self):
        selected = self.tableWidget.selectedItems()
        if selected:
            row = selected[0].row()
            self.tableWidget.removeRow(row)

    # apply action
    def _applyAction(self):
        self._writeEditData()
        self._switchTableLock()

    # cancel action
    def _cancelAction(self):
        self._showTable()
        self._switchTableLock()

    # switch table edit style
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

    # switch table lock
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
