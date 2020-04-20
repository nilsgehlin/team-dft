import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui
import main_window_functionality as f_mw
import pat_functionality as f_pat
import rad_functionality as f_rad
import doc_functionality as f_doc

#TODO Patient database
#TODO Patient profile database


class Application(object):
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui(self.main_window)
        self.setup_functionality()

    def run(self):
        self.main_window.show()

    def setup_functionality(self):
        f_mw.setup_functionality(self.ui)
        f_pat.setup_functionality(self.ui)
        f_rad.setup_functionality(self.ui)


if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())