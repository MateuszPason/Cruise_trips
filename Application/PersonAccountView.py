from PyQt5.QtCore import QSize, QCoreApplication, Qt
import DatabaseConnection
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QSizePolicy, QSpacerItem, QGridLayout
import LoadDataToComboBox
from CheckUserInputs import CheckNewPortObjectDetails, CheckNewTripDetails, CheckDetailsTripToBook
import AddPortObjectToDatabase
import SuccessfulNewEntryInDatabaseInfo


class ClientAccountView(QDialog):
    """All details that client can see on the interface"""
    def __init__(self, email):
        super(ClientAccountView, self).__init__()
        self.ui = loadUi("Resources/interfaces/client_panel.ui", self)
        self.show()
        self.open_trips_button.clicked.connect(self.open_all_trips)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)
        self.menu_trip_button.clicked.connect(lambda: self.trip_booking(email))

    def open_all_trips(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Trips_page)
        get_number_of_trips_to_load = 'SELECT COUNT(*) FROM trips'
        DatabaseConnection.cursor.execute(get_number_of_trips_to_load)
        number_of_trips, = DatabaseConnection.cursor.fetchone()

        get_trips_details = 'SELECT * FROM trips'
        DatabaseConnection.cursor.execute(get_trips_details)
        trip_details = DatabaseConnection.cursor.fetchall()
        for i in range(number_of_trips):
            trip_name = trip_details[i][1]
            trip_price = str(trip_details[i][2])
            trip_country = trip_details[i][3]
            trip_city = trip_details[i][4]
            trip_start = str(trip_details[i][5])
            trip_end = str(trip_details[i][6])
            trip_ship = trip_details[i][7]
            self.create_new_widget(i, 0, trip_name, trip_price, trip_country, trip_city, trip_start, trip_end,
                                   trip_ship)

    def back_to_first_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.Welcome_page)

    def create_new_widget(self, row, column, trip_name, trip_price, trip_country, trip_city, trip_start, trip_end,
                          trip_ship):

        self.single_trip = QFrame(self.ui.scrollAreaWidgetContents)
        self.single_trip.setObjectName(u"single_trip")
        self.single_trip.setMinimumSize(QSize(0, 125))
        self.single_trip.setMaximumSize(QSize(16777215, 125))
        self.single_trip.setStyleSheet(u"")
        self.single_trip.setFrameShape(QFrame.StyledPanel)
        self.single_trip.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.ui.single_trip)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.name_label = QLabel(self.single_trip)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setText(QCoreApplication.translate("Dialog", 'Name: ' + trip_name, None))
        self.gridLayout_2.addWidget(self.name_label, 0, 0, 1, 1)

        self.price_label = QLabel(self.single_trip)
        self.price_label.setObjectName(u"price_label")
        self.price_label.setAlignment(Qt.AlignRight)
        self.price_label.setText(QCoreApplication.translate("Dialog", 'Price: ' + trip_price, None))
        self.gridLayout_2.addWidget(self.price_label, 0, 3, 1, 1)

        self.country_label = QLabel(self.single_trip)
        self.country_label.setObjectName(u"country_label")
        self.country_label.setText(QCoreApplication.translate("Dialog", 'Sail out of: ' + trip_country, None))
        self.gridLayout_2.addWidget(self.country_label, 1, 0, 1, 1)

        self.city_label = QLabel(self.single_trip)
        self.city_label.setObjectName(u"city_label")
        self.city_label.setText(QCoreApplication.translate("Dialog", trip_city, None))
        self.gridLayout_2.addWidget(self.city_label, 1, 1, 1, 1)

        self.start_label = QLabel(self.single_trip)
        self.start_label.setObjectName(u"start_label")
        self.start_label.setText(QCoreApplication.translate("Dialog", 'Date: ' + trip_start[0:10], None))
        self.gridLayout_2.addWidget(self.start_label, 1, 2, 1, 1)

        self.end_label = QLabel(self.single_trip)
        self.end_label.setObjectName(u"end_label")
        self.end_label.setText(QCoreApplication.translate("Dialog", trip_end[0:10], None))
        self.gridLayout_2.addWidget(self.end_label, 1, 3, 1, 1)

        self.ship_label = QLabel(self.single_trip)
        self.ship_label.setObjectName(u"ship_label")
        self.ship_label.setText(QCoreApplication.translate("Dialog", 'Ship: ' + trip_ship, None))
        self.gridLayout_2.addWidget(self.ship_label, 2, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.single_trip, row, column, 1, 1)

    def trip_booking(self, email):
        self.ui.stackedWidget.setCurrentWidget(self.Choose_trip_page)
        LoadDataToComboBox.load_trips(self.trip_combobox)

        get_number_of_available_trips = 'SELECT COUNT(*) FROM trips'
        DatabaseConnection.cursor.execute(get_number_of_available_trips)
        number_of_available_trips, = DatabaseConnection.cursor.fetchone()
        if number_of_available_trips == 0:
            self.ui.stackedWidget.setCurrentWidget(self.Choose_trip_page)
            self.trip_name_error_label.setText('No trips available')
        else:
            self.load_trips_on_change()

        self.trip_combobox.currentTextChanged.connect(self.load_trips_on_change)
        self.book_button.clicked.connect(lambda: self.check_details_of_trip_to_book(email))

    def load_trips_on_change(self):
        trip_name = self.trip_combobox.currentText()
        get_ship_name_assigned_to_trip = 'SELECT onboard FROM trips WHERE name = :given_trip_name'
        DatabaseConnection.cursor.execute(get_ship_name_assigned_to_trip, given_trip_name=trip_name)
        ship_name_assigned_to_trip, = DatabaseConnection.cursor.fetchone()
        get_ship_id_assigned_to_trip = 'SELECT ship_id FROM ships WHERE ship_name = :given_ship_name'
        DatabaseConnection.cursor.execute(get_ship_id_assigned_to_trip, given_ship_name=ship_name_assigned_to_trip)
        ship_id_assigned_to_trip, = DatabaseConnection.cursor.fetchone()

        get_number_of_available_ship_cabins = "SELECT COUNT(*) FROM ship_cabins WHERE room_type IS NOT NULL AND" \
                                              " reserved = 'F' AND ship_id = :given_ship_id"
        DatabaseConnection.cursor.execute(get_number_of_available_ship_cabins, given_ship_id=ship_id_assigned_to_trip)
        number_of_available_ship_cabins, = DatabaseConnection.cursor.fetchone()

        get_available_ship_cabins_for_trip = "SELECT room_number, room_type, guests, sq_m, balcony_sq_m FROM" \
                                             " ship_cabins WHERE" \
                                             " room_type IS NOT NULL AND reserved = 'F' AND ship_id = :given_ship_id"
        DatabaseConnection.cursor.execute(get_available_ship_cabins_for_trip, given_ship_id=ship_id_assigned_to_trip)
        available_ship_cabins_for_trip = DatabaseConnection.cursor.fetchall()
        self.cabin_combobox.clear()
        for i in range(number_of_available_ship_cabins):
            room_number = available_ship_cabins_for_trip[i][0]
            cabin_type = available_ship_cabins_for_trip[i][1]
            cabin_guest = available_ship_cabins_for_trip[i][2]
            cabin_sq_m = available_ship_cabins_for_trip[i][3]
            cabin_balcony_sq_m = available_ship_cabins_for_trip[i][4]
            self.cabin_combobox.addItem(str('Cabin type: ') + cabin_type +
                                        str(' Guests: ') + str(cabin_guest)
                                        + str(' Square meters: ') + str(cabin_sq_m) + str(' Balcony square meters: ')
                                        + str(cabin_balcony_sq_m) + str(' Room number:  ') + room_number)

    def check_details_of_trip_to_book(self, email):
        check_trip_to_book = CheckDetailsTripToBook()
        trip_name = self.trip_combobox.currentText()
        trip_name_check = check_trip_to_book.check_trip_name(trip_name, self.trip_name_error_label)
        cabin = self.cabin_combobox.currentText()
        cabin_check = check_trip_to_book.check_room_to_book(cabin, self.cabin_error_label)
        room_number = cabin[-3:].strip()

        if trip_name_check and cabin_check:
            AddPortObjectToDatabase.NewBookedTrip(email, trip_name, room_number)
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
        elif account_type == 'PM':
            PMAccountOptions(email)


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
        self.assign_port_manager_button.clicked.connect(self.new_pm_to_port_configuration)
        self.new_pm_slot.clicked.connect(self.new_pm_slot_to_database)

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
        if port_city == '':
            self.error_ship_label.setText('Add port')
        else:
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
        self.load_ship_capacity_on_change()
        self.ship_id_comboBox.currentIndexChanged.connect(self.load_ship_capacity_on_change)
        self.add_new_cabin_button.clicked.connect(self.check_all_ship_cabin_details)

    def load_ship_capacity_on_change(self):
        ship_name = self.ship_id_comboBox.currentText()
        get_free_ship_cabins = 'SELECT COUNT(*) FROM ship_cabins JOIN ships USING(ship_id) ' \
                               'WHERE ship_name = :given_name AND guests IS NULL'
        DatabaseConnection.cursor.execute(get_free_ship_cabins, given_name=ship_name)
        free_ship_cabins, = DatabaseConnection.cursor.fetchone()
        self.available_cabins_number_label.setText('New cabins: ' + str(free_ship_cabins))

        # Loading room numbers that you can still edit
        get_rooms_to_edit = 'SELECT room_number FROM ship_cabins JOIN ships USING (ship_id)' \
                            'WHERE ship_name = :given_name AND guests IS NULL'
        self.room_number_comboBox.clear()
        DatabaseConnection.cursor.execute(get_rooms_to_edit, given_name=ship_name)
        for i in DatabaseConnection.cursor.fetchall():
            self.room_number_comboBox.addItem(str(i[0]))

    def check_all_ship_cabin_details(self):
        ship_name = self.ship_id_comboBox.currentText()
        room_number = self.room_number_comboBox.currentText()
        room_type = self.room_type_comboBox.currentText()
        number_of_guests = self.guests_spinBox.value()
        sq_m_cabin = self.cabin_meters_spinBox.value()
        sq_m_balcony = self.balcony_meters_spinBox.value()
        if room_type == 'Inside':
            sq_m_balcony = 0
        if ship_name == '':
            self.available_cabins_number_label.setStyleSheet("color: red")
            self.available_cabins_number_label.setText('Add ships')
        elif room_number == '':
            self.available_cabins_number_label.setStyleSheet("color: red")
            self.available_cabins_number_label.setText('All of the rooms were assigned')
        else:
            self.close()
            AddPortObjectToDatabase.NewShipCabinToDatabase(ship_name, room_number, room_type, number_of_guests,
                                                           sq_m_cabin, sq_m_balcony)

    def new_pm_to_port_configuration(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Assign_port_manger)
        add_available_pms_to_combobox = "SELECT email FROM employees WHERE SUBSTR(employee_register_key, 1, 2) = " \
                                        "'PM' AND port_id IS NULL AND email IS NOT NULL"
        self.port_managers_comboBox.clear()
        DatabaseConnection.cursor.execute(add_available_pms_to_combobox)
        for i in DatabaseConnection.cursor.fetchall():
            self.port_managers_comboBox.addItem(str(i[0]))

        add_available_ports_to_combobox = "SELECT port_id FROM ports MINUS SELECT port_id FROM employees"
        self.ports_comboBox.clear()
        DatabaseConnection.cursor.execute(add_available_ports_to_combobox)
        for i in DatabaseConnection.cursor.fetchall():
            self.ports_comboBox.addItem(str(i[0]))

        self.assign_button.clicked.connect(self.check_all_port_manager_details)

    def check_all_port_manager_details(self):
        if self.port_managers_comboBox.currentText() == '':
            self.port_manager_error_label.setText('Hire port manager')
        elif self.ports_comboBox.currentText() == '':
            self.port_error_label.setText('Add port')
        else:
            self.port_manager_error_label.setText('')
            self.port_error_label.setText('')
            port_manager = self.port_managers_comboBox.currentText()
            port_number = self.ports_comboBox.currentText()
            assign_pm_to_port = "UPDATE employees SET port_id = :given_port_number WHERE email = :given_manager"
            DatabaseConnection.cursor.execute(assign_pm_to_port, (port_number, port_manager))
            DatabaseConnection.connection.commit()
            self.close()
            SuccessfulNewEntryInDatabaseInfo.SuccessfulManagerAssign()

    def new_pm_slot_to_database(self):
        DatabaseConnection.cursor.execute('SELECT pm_slot_number.nextval FROM dual')
        pm_number_using_sequence, = DatabaseConnection.cursor.fetchone()
        pm_code = 'PM' + str(pm_number_using_sequence)
        DatabaseConnection.cursor.execute('SELECT employees_id.nextval FROM dual')
        employee_id, = DatabaseConnection.cursor.fetchone()

        insert_new_slot_for_pm = 'INSERT INTO employees (employee_id, employee_register_key) VALUES (:1, :2)'
        DatabaseConnection.cursor.execute(insert_new_slot_for_pm, (employee_id, pm_code))
        DatabaseConnection.connection.commit()
        self.pm_slot_info.setText('Slot added')

    def back_to_first_page(self):
        """Open interface that user can see at the beginning"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)


class PMAccountOptions(QDialog):
    """All details that port manager can see on the interface"""
    def __init__(self, email):
        super(PMAccountOptions, self).__init__()
        self.ui = loadUi("Resources/interfaces/pm_panel.ui", self)
        self.show()
        check_if_user_assigned = "SELECT port_id FROM employees WHERE email = :account_email"
        DatabaseConnection.cursor.execute(check_if_user_assigned, account_email=email)
        assigned_port, = DatabaseConnection.cursor.fetchone()
        if assigned_port is None:
            self.port_info_button.setEnabled(False)
            self.organize_trip_button.setEnabled(False)
            self.ui.stackedWidget.setCurrentWidget(self.No_port_assigned_info)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.Welcome_page)
        self.port_info_button.clicked.connect(lambda: self.load_port_details(assigned_port))
        self.organize_trip_button.clicked.connect(lambda: self.organize_new_trip(assigned_port))

    def load_port_details(self, port_number):
        self.ui.stackedWidget.setCurrentWidget(self.Info_about_assigned_port)
        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)
        get_port_details = "SELECT * FROM ports WHERE port_id = :given_port_id"
        DatabaseConnection.cursor.execute(get_port_details, given_port_id=port_number)
        port_details = DatabaseConnection.cursor.fetchone()
        get_country_name = "SELECT country_name FROM countries WHERE country_iso = :given_iso"
        DatabaseConnection.cursor.execute(get_country_name, given_iso=port_details[1])
        country_name, = DatabaseConnection.cursor.fetchone()
        self.port_id_label.setText('Port id: ' + str(port_details[0]))
        self.port_country_label.setText('Country: ' + country_name)
        self.port_city_label.setText('City: ' + str(port_details[2]))
        self.port_capacity_label.setText('Maximum capacity: ' + str(port_details[3]))

    def organize_new_trip(self, port_number):
        self.ui.stackedWidget.setCurrentWidget(self.New_trip)

        # Need this solution for a moment, because if user switch widgets from organize trip to another and then
        # again to organize trip he can add multiple trips with the same details, which means user violates constraints
        self.port_info_button.setEnabled(False)
        self.emp_title_back_to_first_page.setEnabled(False)

        self.emp_title_back_to_first_page.clicked.connect(self.back_to_first_page)
        LoadDataToComboBox.load_ships_available_for_trip(self.onboard_combobox, port_number)
        self.add_trip_button.clicked.connect(lambda: self.check_trip_details(port_number))

    def check_trip_details(self, port_number):
        check_trip_details = CheckNewTripDetails()
        trip_name = self.name_edit.text()
        trip_price = self.price_spinbox.value()
        trip_name_check = check_trip_details.check_trip_name(trip_name, self.name_error_label)
        ship_name_for_trip = self.onboard_combobox.currentText()
        ship_names_check = check_trip_details.check_for_existing_ship_in_port(ship_name_for_trip,
                                                                              self.onboard_error_label)
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()
        dates_check = check_trip_details.check_if_date_is_valid(start_date, end_date, self.date_error_label)
        if trip_name_check and ship_names_check and dates_check:
            self.close()
            AddPortObjectToDatabase.NewTripToDatabase(trip_name, trip_price, ship_name_for_trip,
                                                      start_date.toString("dd/MM/yyyy"), end_date.toString("dd/MM/yyyy")
                                                      , port_number)

    def back_to_first_page(self):
        """Open interface that user can see at the beginning"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.Welcome_page)
