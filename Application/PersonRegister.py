from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import AddSomebodyToDatabase
import GlobalFunctions
from CheckUserInputs import CheckRegisterDetails


class NewClient(QDialog):
    def __init__(self):
        super(NewClient, self).__init__()
        self.ui = loadUi("Resources/interfaces/client_register_form.ui", self)
        self.show()

        GlobalFunctions.load_countries_list(self.country_comboBox)
        self.create_account_button.clicked.connect(self.check_all_client_details)

    def check_all_client_details(self):
        details_check = CheckRegisterDetails()
        email = details_check.check_email(self.email_edit.text(), self.email_label_error)
        first_name = details_check.check_first_name(self.first_name_edit.text(), self.first_name_label_error)
        last_name = details_check.check_last_name(self.last_name_edit.text(), self.last_name_label_error)
        phone_number = details_check.check_phone(self.phone_edit.text().strip(), self.phone_number_label_error)
        password = details_check.check_password(self.password_edit.text().strip(), self.re_password_edit.text().strip(),
                                                self.password_label_error, self.re_password_label_error)
        sex = details_check.check_sex(self.male_radio, self.female_radio)
        country = details_check.check_country(self.country_comboBox)
        if email and first_name and last_name and password and country and phone_number:
            AddSomebodyToDatabase.AddClient(email, first_name, last_name, password, sex, country, phone_number)
            self.close()
        else:
            print('Wrong data')


class NewEmployee(QDialog):
    def __init__(self):
        super(NewEmployee, self).__init__()
        self.ui = loadUi("Resources/interfaces/employee_register_form.ui", self)
        self.show()

        GlobalFunctions.load_countries_list(self.country_comboBox)
        self.create_account_button.clicked.connect(self.check_all_employee_details)


    def check_all_employee_details(self):
        """Create new user if all information are valid"""
        details_check = CheckRegisterDetails()
        email = details_check.check_email(self.email_edit.text(), self.email_label_error)
        first_name = details_check.check_first_name(self.first_name_edit.text(), self.first_name_label_error)
        last_name = details_check.check_last_name(self.last_name_edit.text(), self.last_name_label_error)
        phone_number = details_check.check_phone(self.phone_edit.text(), self.phone_number_label_error)
        password = details_check.check_password(self.password_edit.text().strip(), self.re_password_edit.text().strip(),
                                                self.password_label_error, self.re_password_label_error)
        country = details_check.check_country(self.country_comboBox)
        register_key = details_check.check_employee_register_key(self.register_key_edit.text().strip(),
                                                                 self.register_key_label_error)
        if email and first_name and last_name and phone_number and password and register_key and country:
            AddSomebodyToDatabase.AddEmployee(email, first_name, last_name, phone_number, password, country,
                                              register_key)
            self.close()





