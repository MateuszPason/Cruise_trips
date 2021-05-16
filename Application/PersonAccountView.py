import DatabaseConnection
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import LoadDataToComboBox
from CheckUserInputs import CheckNewPortObjectDetails
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
            CEOAccountOptions()


class CEOAccountOptions(QDialog):
    """All details that CEO can see on the interface"""
    def __init__(self):
        super(CEOAccountOptions, self).__init__()
        self.ui = loadUi("Resources/interfaces/ceo_panel.ui", self)
        self.show()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)
        self.new_port_button.clicked.connect(self.open_new_port_configuration)
        self.configure_port_button.clicked.connect(self.update_port_configuration)
        self.new_ship_button.clicked.connect(self.open_new_ship_configuration)
        self.new_ship_cabin_button.clicked.connect(self.new_cabin_configuration)

    def open_new_port_configuration(self):
        """Opens widget with form for new port. After button is clicked, starts to check all ports details"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.New_port_configuration)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)

        LoadDataToComboBox.load_countries_list(self.country_comboBox)
        self.port_add_button.clicked.connect(self.check_all_port_details)

    def check_all_port_details(self):
        """Check if user entered valid port details and/or didn't violate primary key"""
        port_details = CheckNewPortObjectDetails()
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

    def update_port_configuration(self):
        """Load interface with port update"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.Port_configuration)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)
        LoadDataToComboBox.load_ports(self.port_comboBox)

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

    def open_new_ship_configuration(self):
        """Interface with new ship form"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.New_ship_configuration)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)

        LoadDataToComboBox.load_ports(self.port_identification_comboBox)
        self.add_new_ship_button.clicked.connect(self.check_all_ship_details)

    def check_all_ship_details(self):
        """Checks if all ship details are valid and/or don't violate constraint"""
        ship_details = CheckNewPortObjectDetails()
        ship_name = self.ship_name_edit.text()
        capacity = self.ship_capacity_spinBox.value()
        country_iso = self.port_identification_comboBox.currentText()[0:3]
        port_city = self.port_identification_comboBox.currentText()[4:]
        get_port_id = 'SELECT port_id FROM ports WHERE country_iso = :given_ctr_iso AND city = :given_city'
        DatabaseConnection.cursor.execute(get_port_id, given_ctr_iso=country_iso, given_city=port_city)
        port_id, = DatabaseConnection.cursor.fetchone()
        valid_ship_details = ship_details.check_new_ship_details(ship_name, port_id, self.ship_name_label_error,
                                                                 self.error_ship_label)
        if valid_ship_details:
            self.close()
            AddPortObjectToDatabase.NewShipToDatabase(ship_name, capacity, port_id)

    def new_cabin_configuration(self):
        self.ui.stackedWidget.setCurrentWidget(self.New_ship_cabin)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)
        LoadDataToComboBox.load_port_ids(self.ship_id_comboBox)
        self.ship_id_comboBox.currentIndexChanged.connect(self.load_ship_capacity_on_change)

    def load_ship_capacity_on_change(self):
        ship_name = self.ship_id_comboBox.currentText()
        get_free_ship_cabins = 'SELECT COUNT(*) FROM ship_cabins JOIN ships USING(ship_id) ' \
                               'WHERE ship_name = :given_name AND guests IS NULL'
        DatabaseConnection.cursor.execute(get_free_ship_cabins, given_name=ship_name)
        free_ship_cabins, = DatabaseConnection.cursor.fetchone()
        self.available_cabins_number_label.setText('New cabins: ' + str(free_ship_cabins))

        get_rooms_to_edit = 'SELECT room_number FROM ship_cabins JOIN ships USING (ship_id)' \
                            'WHERE ship_name = :given_name AND guests IS NULL'
        self.room_number_comboBox.clear()
        DatabaseConnection.cursor.execute(get_rooms_to_edit, given_name=ship_name)
        for i in DatabaseConnection.cursor.fetchall():
            self.room_number_comboBox.addItem(str(i[0]))

    def back_to_first_page(self):
        """Open interface that user can see at the beginning"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)


