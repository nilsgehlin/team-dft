import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_main import Ui_main_window as Ui_main
from ui_pat import Ui_stacked_pat as Ui_pat


class Application(Ui_main):
    def __init__(self):
        super(Ui_main, self).__init__()
        self.main_window = QtWidgets.QMainWindow()
        self.setupUi(self.main_window)
        self.stacked_pat = Ui_pat()
        self.stacked_pat.setupUi(self.stacked_pat_temp)
        self.stacked_main.setCurrentWidget(self.page_login)
        self.setup_functionality()

    def run(self):
        self.main_window.show()

    def setup_functionality(self):
        self.button_login.clicked.connect(self.login)
        # self.login_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home_page))
        # self.home_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.login_page))

    # def my_clicked(self, widget):
    #     self.stackedWidget.setCurrentWidget(widget)

    def login(self):
        user_type = self.combo_box_login.currentText()
        if user_type == "Patient":
            self.stacked_main.setCurrentWidget(self.page_pat)
        if user_type == "Radiologist":
            self.stacked_main.setCurrentWidget(self.page_rad)
        if user_type == "Doctor":
            self.stacked_main.setCurrentWidget(self.page_doc)


if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())