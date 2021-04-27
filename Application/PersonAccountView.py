import DatabaseConnection
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import GlobalFunctions
from CheckUserInputs import CheckNewPortDetails
import AddPortObjectToDatabase


class ClientAccountView(QDialog):
    """All details that client can see on the interface"""
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
    """Determine which employee logged in"""
    def __init__(self, email):
        super(WhichEmployeeAccountView, self).__init__()
        get_account_type = 'SELECT SUBSTR(employee_register_key, 1, 2) FROM employees WHERE email = :given_email'
        DatabaseConnection.cursor.execute(get_account_type, given_email=email)
        account_type, = DatabaseConnection.cursor.fetchone()
        if account_type is None:
            CEOAccountView()


class CEOAccountView(QDialog):
    """All details that CEO can see on the interface"""
    def __init__(self):
        super(CEOAccountView, self).__init__()
        self.ui = loadUi("Resources/interfaces/ceo_panel.ui", self)
        self.show()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)
        self.new_port_button.clicked.connect(self.open_new_port_configuration)
        self.configure_port_button.clicked.connect(self.open_port_configuration)

    def open_new_port_configuration(self):
        """Opens widget with form for new port. After button is clicked, starts to check all ports details"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.New_port_configuration)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)

        GlobalFunctions.load_countries_list(self.country_comboBox)
        self.port_add_button.clicked.connect(self.check_all_port_details)

    def check_all_port_details(self):
        """Check if user entered valid port details and/or didn't violate primary key"""
        port_details = CheckNewPortDetails()
        port_country = self.country_comboBox.currentText()
        port_capacity = self.capacity_spinBox.value()
        get_ctr_iso = 'SELECT country_iso FROM countries WHERE country_name = :given_name'
        DatabaseConnection.cursor.execute(get_ctr_iso, given_name=port_country)
        iso, = DatabaseConnection.cursor.fetchone()
        is_unique = port_details.check_city_and_port_uniqueness(iso, self.city_lineEdit.text(), self.city_label_error,
                                                                self.error_port_label)
        if is_unique:
            self.close()
            AddPortObjectToDatabase.NewPortToDatabase(port_country, is_unique, port_capacity)

    def open_port_configuration(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Port_configuration)
        """Prevents duplicating ports in comboBox"""
        self.port_comboBox.clear()
        """Get number of rows in ports table"""
        result, = DatabaseConnection.cursor.execute("SELECT COUNT(*) FROM ports").fetchone()

        """Load all ports that user can modify"""
        port_identification = DatabaseConnection.cursor.execute('SELECT country_iso, city FROM ports').fetchall()
        for i in range(result):
            item_to_port_combobox = port_identification[i][0] + ' ' + port_identification[i][1]
            self.port_comboBox.addItem(item_to_port_combobox)

        self.change_port_details_button.clicked.connect(self.enter_updated_port_details_to_db)

    def enter_updated_port_details_to_db(self):
        """Update port details with given details, identification based on chosen value from comboBox"""
        ctr_iso = self.port_comboBox.currentText()[0:3]
        port_city = self.port_comboBox.currentText()[4:]
        new_capacity = self.port_capacity_change.value()
        statement = 'UPDATE ports SET capacity = :1 WHERE country_iso = :2 AND city = :3'
        DatabaseConnection.cursor.execute(statement, (new_capacity, ctr_iso, port_city))
        DatabaseConnection.connection.commit()
        prompt_user_info = 'Port updated, capacity set to: {}'.format(new_capacity)
        self.successful_update_label.setText(prompt_user_info)

    def back_to_first_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)


