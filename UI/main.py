import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui
import main_window_functionality as f_mw
import pat_functionality as f_pat
import rad_functionality as f_rad
import sur_functionality as f_sur
from patient import Patient

#TODO Patient database
#TODO Patient profile database


class Application(object):
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui(self.main_window)

        self.pat_dict = self.import_patient_data()
        self.rad_dict = {}
        self.sur_dict = {}

        self.current_pat_id = None
        self.current_errand_id = None

        self.setup_functionality()

    def run(self):
        self.main_window.show()

    def setup_functionality(self):
        f_mw.setup_functionality(self, self.ui)

    def init_pat(self):
        f_pat.setup_functionality(self, self.ui)

    def init_rad(self):
        f_rad.setup_functionality(self, self.ui)

    def init_sur(self):
        f_sur.setup_functionality(self, self.ui)


    def import_patient_data(self):
        pat_dict = {"0000": Patient("0000")}
        return pat_dict


if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())