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
        self.login_button.clicked.connect(self.to_ceo_panel)

    def to_ceo_panel(self):
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


class SuccessfulNewShipCabin(QDialog):
    """Load interface after successful ship cabin add"""
    def __init__(self):
        super(SuccessfulNewShipCabin, self).__init__()
        self.ui = loadUi("Resources/interfaces/Successful_ship_cabin_add.ui", self)
        self.show()
        self.go_back.clicked.connect(self.to_ceo_panel)

    def to_ceo_panel(self):
        self.close()
        PersonAccountView.CEOAccountOptions()


class SuccessfulManagerAssign(QDialog):
    """Load interface after successful port manager assign to specific port"""
    def __init__(self):
        super(SuccessfulManagerAssign, self).__init__()
        self.ui = loadUi("Resources/interfaces/Successful_pm_assign.ui", self)
        self.show()
        self.go_back.clicked.connect(self.to_ceo_panel)

    def to_ceo_panel(self):
        self.close()
        PersonAccountView.CEOAccountOptions()


class SuccessfulNewTrip(QDialog):
    """Load interface after successful trip add"""
    def __init__(self, email):
        super(SuccessfulNewTrip, self).__init__()
        self.ui = loadUi("Resources/interfaces/Successful_trip_add.ui", self)
        self.show()
        self.go_back.clicked.connect(lambda: self.to_pm_panel(email))

    def to_pm_panel(self, email):
        self.close()
        PersonAccountView.PMAccountOptions(email)


class SuccessfulBookedTtrip(QDialog):
    """Load interface after successful trip booking"""
    def __init__(self, email):
        super(SuccessfulBookedTtrip, self).__init__()
        self.ui = loadUi("Resources/interfaces/Successful_trip_booked.ui", self)
        self.show()
        self.go_back.clicked.connect(lambda: self.to_client_panel(email))

    def to_client_panel(self, email):
        self.close()
        PersonAccountView.ClientAccountView(email)
