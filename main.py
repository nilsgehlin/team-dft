import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import json

import os, sys
path = os.path.join("UI")
sys.path.insert(0, path)
from ui import Ui
import main_window_functionality as f_mw
import pat_functionality as f_pat
import rad_functionality as f_rad
import sur_functionality as f_sur
from patient import Patient, Errand

path = os.path.join("visualizationEngine")
sys.path.insert(0, path)
from visualizationEngine.VisualizationEngine import VisualizationEngine
from visualizationEngine.annotation.Annotation import Annotation

#TODO Patient database
#TODO Patient profile database


class Application(object):
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui(self.main_window)
        self.visEngine = VisualizationEngine()

        self.pat_dict = self.import_patient_data()
        self.rad_dict = {}
        self.sur_dict = {}

        self.current_pat_id = None
        self.current_errand_id = None
        self.current_theme_button_pressed = self.ui.menu_bar_theme_button_night_mode

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
        ### Now reads data from json files
        with open('database/jane_smith.json') as json_file:
            data = json.load(json_file)
            jane_smith = Patient.fromJson(data)

        with open('database/mark_johnson.json') as json_file:
            data = json.load(json_file)
            mark_johnson = Patient.fromJson(data)

        ### Can also serialize/export the patient data as example below
        # with open('database/mark_johnson.json', 'w') as outfile:
        #     json.dump(mark_johnson.toJson(), outfile, indent = 4)

        pat_dict = {jane_smith.id: jane_smith, mark_johnson.id: mark_johnson}
        return pat_dict



if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())