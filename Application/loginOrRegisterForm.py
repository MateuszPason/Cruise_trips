from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import whoWantToRegister
import whoWantToLogin


class OpeningWindow(QDialog):
    def __init__(self):
        super(OpeningWindow, self).__init__()
        self.ui = loadUi("Resources/interfaces/log_in_or_reg.ui", self)
        self.show()
        self.register_button.clicked.connect(self.open_new_person_register_form)
        self.login_button.clicked.connect(self.open_new_person_login_form)

    def open_new_person_register_form(self):
        self.close()
        whoWantToRegister.RegisterNewClientOrEmployee()

    def open_new_person_login_form(self):
        self.close()
        whoWantToLogin.LoginClientOrEmployee()




