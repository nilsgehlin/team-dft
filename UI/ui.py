import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_main_window import Ui_main_window
from pat import Ui_pat
from rad import Ui_rad
from sur import Ui_sur


class Ui(Ui_main_window):
    def __init__(self, main_window):
        super(Ui_main_window, self).__init__()
        self.main_window = main_window
        self.setupUi(main_window)

        self.ui_pat = Ui_pat()
        self.ui_pat.setupUi(self.stacked_pat)
        self.ui_rad = Ui_rad()
        self.ui_rad.setupUi(self.stacked_rad)
        self.ui_sur = Ui_sur()
        self.ui_sur.setupUi(self.stacked_sur)

        self.stacked_pat.setCurrentWidget(self.ui_pat.page_pat_home)
        self.stacked_rad.setCurrentWidget(self.ui_rad.page_rad_home)
        self.stacked_sur.setCurrentWidget(self.ui_sur.page_sur_home)
        self.stacked_main.setCurrentWidget(self.page_login)

        self.prev_page = None



if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    application = Ui(main_window)
    main_window.show()
    sys.exit(Qapp.exec_())