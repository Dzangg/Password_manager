import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import handleUser
import signUpWidget
import logInWidget
import popoutWidget
import userPanelWidget

# GLOBAL VARIABLES & FUNCTIONS

WIN_SIZE = 500

with open("resources/css/styles.css", 'r') as f:
    css = f.read()


def popout():
    p.show()


class Window(QMainWindow):
    '''
    A class to represent main window

        Parameters:
            QMainWindow : widget

        Functions:

            connect_user()

            signed()

            back_sign()

            back_login()

            signupView()

            loginView()

            _createLabel()

            _createButtons()

    '''

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

    # on user log in
    def connect_user(self, user, password):
        panel = userPanelWidget.userPanelWidget(user, password, self)
        self.centralwidget.addWidget(panel)
        self.centralwidget.setCurrentWidget(panel)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(640, 480)

    # on user created
    def signed(self):
        popout()
        self.centralwidget.setCurrentWidget(self.main_window)
        self.centralwidget.removeWidget(self.signup_widget)

    # switch between widgets
    def back_sign(self):
        self.centralwidget.setCurrentWidget(self.main_window)
        self.centralwidget.removeWidget(self.signup_widget)

    # switch between widgets
    def back_login(self):
        self.centralwidget.setCurrentWidget(self.main_window)
        self.centralwidget.removeWidget(self.login_widget)

    # change layout to signup layout
    def signupView(self):
        self.signup_widget = signUpWidget.signUpWidget(self)
        self.signup_widget.cancelBtn.clicked.connect(self.back_sign)
        self.centralwidget.addWidget(self.signup_widget)
        self.centralwidget.setCurrentWidget(self.signup_widget)

    # change layout to login layout
    def loginView(self):
        self.login_widget = logInWidget.logInWidget(self)
        self.login_widget.cancelBtn.clicked.connect(self.back_login)
        self.centralwidget.addWidget(self.login_widget)
        self.centralwidget.setCurrentWidget(self.login_widget)

    # create Main label
    def _createLabel(self):
        self.label = QLabel("Password Manager")
        self.label.setObjectName("mainLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(300, 200)
        self.label.setStyleSheet(css)

    # create buttons
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

    def copyToClipboard(self, value):
        clipboard = app.clipboard()
        clipboard.setText(value)


if __name__ == "__main__":
    print(signUpWidget.signUpWidget.__doc__)
    print(logInWidget.logInWidget.__doc__)
    handleUser.initializeDirectory()
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowIcon(QIcon("resources/icon.png"))
    window.show()
    p = popoutWidget.popoutWidget()
    sys.exit(app.exec_())
