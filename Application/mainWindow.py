import loginOrRegisterForm
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
mainWindow = loginOrRegisterForm.OpeningWindow()
mainWindow.show()
app.exec_()
