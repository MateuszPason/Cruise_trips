from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import loginOrRegisterForm


class SuccessfulRegister(QDialog):
    def __init__(self):
        super(SuccessfulRegister, self).__init__()
        self.ui = loadUi("Resources/interfaces/successful_register.ui", self)
        self.show()
        self.login_button.clicked.connect(self.to_main_window)

    def to_main_window(self):
        self.close()
        loginOrRegisterForm.OpeningWindow()

