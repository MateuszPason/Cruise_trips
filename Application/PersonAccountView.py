import DatabaseConnection
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import GlobalFunctions
from CheckUserInputs import CheckNewPortDetails
import AddPortObjectToDatabase


class ClientAccountView(QDialog):
    def __init__(self, email):
        super(ClientAccountView, self).__init__()
        self.ui = loadUi("Resources/interfaces/client_logged_account.ui", self)
        self.show()
        get_client_details = 'SELECT first_name FROM clients WHERE email = :email'
        DatabaseConnection.cursor.execute(get_client_details, email=email)
        for row in DatabaseConnection.cursor:
            self.client_name.setText(row[0])
        self.log_out_client_button.clicked.connect(self.log_out_client)

    def log_out_client(self):
        self.close()


class WhichEmployeeAccountView(QDialog):
    def __init__(self, email):
        super(WhichEmployeeAccountView, self).__init__()
        get_account_type = 'SELECT SUBSTR(employee_register_key, 1, 2) FROM employees WHERE email = :given_email'
        DatabaseConnection.cursor.execute(get_account_type, given_email=email)
        account_type, = DatabaseConnection.cursor.fetchone()
        if account_type is None:
            CEOAccountView()


class CEOAccountView(QDialog):
    def __init__(self):
        super(CEOAccountView, self).__init__()
        self.ui = loadUi("Resources/interfaces/ceo_panel.ui", self)
        self.show()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)
        self.new_port_button.clicked.connect(self.open_port_configuration)

    def open_port_configuration(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Port_configuration)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)

        GlobalFunctions.load_countries_list(self.country_comboBox)
        self.port_add_button.clicked.connect(self.check_all_port_details)

    def check_all_port_details(self):
        port_details = CheckNewPortDetails()
        port_country = self.country_comboBox.currentText()
        port_city = port_details.check_city(self.city_lineEdit.text(), self.city_label_error)
        port_capacity = self.capacity_spinBox.value()
        if port_city and port_capacity:
            AddPortObjectToDatabase.NewPortToDatabase(port_country, port_city, port_capacity)
            print('Success')

    def back_to_first_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)
