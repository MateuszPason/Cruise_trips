from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLabel
import DatabaseConnection
import PersonAccountView


class ClientLogin(QDialog):
    def __init__(self):
        super(ClientLogin, self).__init__()
        self.ui = loadUi("Resources/interfaces/client_login_form.ui", self)
        self.show()
        self.login_button.clicked.connect(self.check_for_client_account)

    def check_for_client_account(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        look_for_client = 'SELECT * FROM clients WHERE email = :2 AND password = :3'
        DatabaseConnection.cursor.execute(look_for_client, (email, password))
        if len(DatabaseConnection.cursor.fetchall()) > 0:
            self.close()
            PersonAccountView.ClientAccountView(email)
        else:
            self.wrong_credentials_info.setText('No such user')


class EmployeeLogin(QDialog):
    def __init__(self):
        super(EmployeeLogin, self).__init__()
        self.ui = loadUi("Resources/interfaces/employee_login_form.ui", self)
        self.show()
        self.login_button.clicked.connect(self.check_for_employee_account)

    def check_for_employee_account(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        look_for_employee = 'SELECT * FROM employees WHERE email = :2 AND password = :3'
        DatabaseConnection.cursor.execute(look_for_employee, (email, password))
        if len(DatabaseConnection.cursor.fetchall()) > 0:
            self.close()
            PersonAccountView.WhichEmployeeAccountView(email)
        else:
            self.wrong_credentials_info.setText('No such user')
