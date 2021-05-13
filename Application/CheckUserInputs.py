import DatabaseConnection
import re


class CheckRegisterDetails:
    def check_email(self, email, set_error_email_label):
        """If search finds match then return a corresponding match object. Return none if there is no match.
        check if the email will be unique in database"""
        email_rules = "^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"
        checked_mail = re.search(email_rules, email)
        if checked_mail is None:
            set_error_email_label.setText('Enter valid e-email')
            return False
        look_for_email = 'SELECT * FROM employees WHERE email = :given_email'
        DatabaseConnection.cursor.execute(look_for_email, given_email=email)
        if len(DatabaseConnection.cursor.fetchall()) > 0:
            set_error_email_label.setText('There is user with such email')
            return False
        set_error_email_label.setText('')
        return email

    def check_first_name(self, first_name, set_error_first_name_label):
        first_name.strip()
        if len(first_name) == 0:
            set_error_first_name_label.setText('Enter your first name')
            return False
        set_error_first_name_label.setText('')
        return first_name

    def check_last_name(self, last_name, set_error_last_name_label):
        last_name.strip()
        if len(last_name) == 0:
            set_error_last_name_label.setText('Enter your last name')
            return False
        set_error_last_name_label.setText('')
        return last_name

    def check_password(self, password, repeated_password, set_error_password_label, set_error_re_password_label):
        if not password:
            set_error_password_label.setText('Enter your password')
            set_error_re_password_label.setText('')
            return False
        if password and not repeated_password:
            set_error_re_password_label.setText('Type your password again')
            set_error_password_label.setText('')
            return False
        if password != repeated_password:
            set_error_re_password_label.setText('Passwords do not match')
        if password == repeated_password:
            set_error_password_label.setText('')
            set_error_re_password_label.setText('')
            return password

    def check_sex(self, male, female):
        if male.isChecked():
            return 'Male'
        if female.isChecked():
            return 'Female'

    def check_country(self, country_comboBox):
        return str(country_comboBox.currentText())

    def check_phone(self, phone_number, set_error_number_label):
        if len(phone_number) != 9:
            set_error_number_label.setText('Enter valid phone number')
            return False
        set_error_number_label.setText('')
        return phone_number

    def check_employee_register_key(self, register_key, set_error_register_key_label):
        """check if register key is 4 characters long,
         key exists in database and user isn't trying to update previously used key"""
        check_if_register_key_exists = 'SELECT * FROM employees WHERE employee_register_key = :given_register_key'
        DatabaseConnection.cursor.execute(check_if_register_key_exists, given_register_key=register_key)
        is_number_of_register_keys_equal_zero = len(DatabaseConnection.cursor.fetchall())
        check_if_updatable = 'SELECT * FROM employees WHERE' \
                             ' employee_register_key = :given_register_key AND email IS NULL'
        DatabaseConnection.cursor.execute(check_if_updatable, given_register_key=register_key)
        how_many_updatable_rows = len(DatabaseConnection.cursor.fetchall())
        if len(register_key) != 4:
            set_error_register_key_label.setText('Enter valid register key')
            return False
        if is_number_of_register_keys_equal_zero == 0:
            set_error_register_key_label.setText('Wrong register key')
            return False
        if how_many_updatable_rows == 0:
            set_error_register_key_label.setText('You can\'t use this key')
            return False
        set_error_register_key_label.setText('')
        return register_key


class CheckNewPortObjectDetails:
    def check_city_and_port_uniqueness(self, country_iso, city, set_error_city_label, set_error_port_label):
        city.strip()
        if len(city) == 0:
            set_error_city_label.setText('Enter valid city')
            return False
        set_error_city_label.setText('')
        statement = 'SELECT * FROM ports WHERE country_iso = :given_ctr_iso AND city = :given_city'
        DatabaseConnection.cursor.execute(statement, given_ctr_iso=country_iso, given_city=city)
        if len(DatabaseConnection.cursor.fetchall()) > 0:
            set_error_port_label.setText('There is such port')
            return False
        set_error_port_label.setText('')
        return city

    def check_new_ship_details(self, ship_name, port_id, set_error_ship_name_label, set_error_ship_label):
        ship_name.strip()
        if len(ship_name) == 0:
            set_error_ship_name_label.setText('Enter ship name')
            return False
        set_error_ship_name_label.setText('')
        statement = 'SELECT * FROM ships WHERE ship_name = :given_ship_name AND home_port_id = :given_port'
        DatabaseConnection.cursor.execute(statement, given_ship_name=ship_name, given_port=port_id)
        if len(DatabaseConnection.cursor.fetchall()) > 0:
            set_error_ship_label.setText('There is such ship')
            return False
        set_error_ship_label.setText('')
        return True
