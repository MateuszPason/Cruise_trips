from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import PersonRegister


class RegisterNewClientOrEmployee(QDialog):
    def __init__(self):
        super(RegisterNewClientOrEmployee, self).__init__()
        self.ui = loadUi("Resources/interfaces/choose_account_type.ui", self)
        self.show()
        self.client_button.clicked.connect(self.new_client_account)
        self.employee_button.clicked.connect(self.new_employee_account)

    def new_client_account(self):
        self.close()
        PersonRegister.NewClient()

    def new_employee_account(self):
        self.close()
        PersonRegister.NewEmployee()
