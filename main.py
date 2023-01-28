import sys

from PyQt5 import QtSvg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QMenu,
    QMenuBar,
    QToolBar,

)

WIN_SIZE = 500


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WIN_SIZE, WIN_SIZE)

        self.centralwidget = QWidget(self)
        self.centralwidget.resize(WIN_SIZE, WIN_SIZE)

        self._createStyleWindow()
        self._createMenuBar()
        # self._createToolBars()

    def _createStyleWindow(self):
        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.closeMenu)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.9)

        radius = 10
        r, g, b = 235, 231, 230
        self.centralwidget.setStyleSheet(
            """
            background:rgb({0},{1},{2});
            border-radius:{3}px;
            """.format(r, g, b, radius)
        )

    def _createMenuBar(self):
        menuBar = self.menuBar()
        exitMenu = QMenu("&Exit", self)
        minimizeMenu = QMenu("&Minimize", self)
        menuBar.addMenu(exitMenu)
        menuBar.addMenu(minimizeMenu)
        menuBar.setLayoutDirection(Qt.RightToLeft)
        self.setMenuBar(menuBar)

    def closeMenu(self, pos):
        menu = QMenu()

        exit_option = menu.addAction('Exit')

        exit_option.triggered.connect(lambda: exit())

        menu.exec_(self.mapToGlobal(pos))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.ArrowCursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
