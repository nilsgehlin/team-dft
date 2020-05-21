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
        self.visEngine = None

        self.pat_dict = self.import_patient_data()
        self.rad_dict = {}
        self.sur_dict = {}

        self.current_pat_id = None
        self.current_errand_id = None
        self.current_theme_button_pressed = self.ui.menu_bar_theme_button_night_mode

        self.setup_functionality()

    def run(self):
        self.main_window.show()
        f_mw.set_style_sheet(self.ui, "ManjaroMix.qss")  # "ManjaroMix.qss", "Aqua.qss"

    def setup_functionality(self):
        f_mw.setup_functionality(self, self.ui)

    def init_pat(self):
        self.visEngine = VisualizationEngine()
        f_pat.setup_functionality(self, self.ui)

    def init_rad(self):
        self.visEngine = VisualizationEngine()
        f_rad.setup_functionality(self, self.ui)

    def init_sur(self):
        self.visEngine = VisualizationEngine()
        f_sur.setup_functionality(self, self.ui)

    def import_patient_data(self):
        pat_dict = {}
        dir = "database"
        for file in os.listdir(dir):
            with open(os.path.join(dir, file)) as json_file:
                data = json.load(json_file)
                patient = Patient.fromJson(data)
                pat_dict[patient.id] = patient
        return pat_dict

    def export_patient_data(self):
        dir = "export_database"
        for patient in self.pat_dict.values():
            filename = patient.first_name + "_" + patient.last_name + ".json"
            with open(os.path.join(dir, filename), 'w') as outfile:
                json.dump(patient.toJson(), outfile, indent=4)


if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())