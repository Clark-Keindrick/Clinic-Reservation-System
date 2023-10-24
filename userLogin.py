from PyQt6.QtWidgets import (QLineEdit, QAbstractButton, QDialog)
from ADMINLOGIN import Ui_LoginForm
import sys
from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtCore import Qt, QPoint
import psycopg2
import psycopg2.extras


class Login_Window(QDialog, Ui_LoginForm):
    def __init__(self):
        super(Login_Window, self).__init__()
        self.setupUi(self)

        hostname = 'localhost'
        database = 'llmdci'
        username = 'postgres'
        pword = '123456'
        port_id = 5432

        self.password = list()
        self.Uname = list()

        conn = None

        try:
            with psycopg2.connect(
                    host=hostname,
                    dbname=database,
                    user=username,
                    password=pword,
                    port=port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute('SELECT * FROM ADMIN_STAFF WHERE DEACTIVATE = 0')
                    for record in cur.fetchall():
                        self.Uname.append(record['admin_uname'])
                        self.password.append(record['admin_pass'])

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

        self.loginbtn.clicked.connect(self.verify)
        self.Xbtn.setProperty("class", "exitbtn")
        self.Xbtn.clicked.connect(self.exit)

        self.hide = QIcon('eye.png')
        self.showPassAction = QAction(self.hide, 'Show password', self)
        self.Passlbl.addAction(
            self.showPassAction, QLineEdit.ActionPosition.TrailingPosition)

        showPass = self.Passlbl.findChild(QAbstractButton)
        showPass.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        showPass.pressed.connect(lambda: self.showPassword(True))
        showPass.released.connect(lambda: self.showPassword(False))

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.position().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())

    def mouseReleaseEvent(self, event):
        self.oldPos = event.position().toPoint()

    def showPassword(self, show):
        self.Passlbl.setEchoMode(
            QLineEdit.EchoMode.Normal if show else QLineEdit.EchoMode.Password)

    def verify(self):
        if self.Userlbl.text().strip() in self.Uname and self.Passlbl.text() in self.password:
            self.accept()

        else:
            self.invalidLBL.setText("Account is Invalid!")
            self.invalidLBL.setStyleSheet("font-family: MS shell dlg 2; color: red;")

    def exit(self):
        sys.exit()


