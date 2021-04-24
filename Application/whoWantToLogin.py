import PersonLogin
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class LoginClientOrEmployee(QDialog):
    def __init__(self):
        super(LoginClientOrEmployee, self).__init__()
        self.ui = loadUi("Resources/interfaces/choose_who_login.ui", self)
        self.show()
        self.client_button.clicked.connect(self.client_login)
        self.employee_button.clicked.connect(self.employee_login)

    def client_login(self):
        self.close()
        PersonLogin.ClientLogin()

    def employee_login(self):
        self.close()
        PersonLogin.EmployeeLogin()
