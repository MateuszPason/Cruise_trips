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


class CheckNewPortDetails:
    def check_city(self, city, set_error_city_label):
        city.strip()
        if len(city) == 0:
            set_error_city_label.setText('Enter valid city')
            return False
        set_error_city_label.setText('')
        return city
