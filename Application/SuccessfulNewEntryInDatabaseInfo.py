from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import loginOrRegisterForm
import PersonAccountView


class SuccessfulRegister(QDialog):
    """Load interface after successful register"""
    def __init__(self):
        super(SuccessfulRegister, self).__init__()
        self.ui = loadUi("Resources/interfaces/successful_register.ui", self)
        self.show()
        self.login_button.clicked.connect(self.to_main_window)

    def to_main_window(self):
        self.close()
        loginOrRegisterForm.OpeningWindow()


class SuccessfulNewPort(QDialog):
    """Load interface after successful port add"""
    def __init__(self):
        super(SuccessfulNewPort, self).__init__()
        self.ui = loadUi("Resources/interfaces/Successful_port_add.ui", self)
        self.show()
        self.go_back.clicked.connect(self.to_ceo_panel)

    def to_ceo_panel(self):
        self.close()
        PersonAccountView.CEOAccountOptions()


class SuccessfulNewShip(QDialog):
    """Load interface after successful ship add"""
    def __init__(self):
        super(SuccessfulNewShip, self).__init__()
        self.ui = loadUi("Resources/interfaces/Successful_ship_add.ui", self)
        self.show()
        self.ship_added_button.clicked.connect(self.to_ceo_panel)

    def to_ceo_panel(self):
        self.close()
        PersonAccountView.CEOAccountOptions()