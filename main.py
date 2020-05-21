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
from doctor import Doctor

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

        self.pat_dict = self.import_data("patient_database", Patient)
        self.rad_dict = self.import_data("radiologist_database", Doctor)
        self.sur_dict = self.import_data("surgeon_database", Doctor)

        self.export_data("patient_database", self.pat_dict)
        self.export_data("radiologist_database", self.rad_dict)
        self.export_data("surgeon_database", self.sur_dict)

        self.current_pat_id = None
        self.current_errand_id = None
        self.current_rad_id = None
        self.current_sur_id = None
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

    def import_data(self, dir_, class_):
        dict_ = {}
        dir_ = os.path.join("databases", dir_)
        for file in os.listdir(dir_):
            with open(os.path.join(dir_, file)) as json_file:
                data = json.load(json_file)
                object_ = class_.fromJson(data)
                dict_[object_.id] = object_
        return dict_

    def export_data(self, dir_, dict_):
        dir_ = os.path.join("databases", dir_ + "_export")
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        for object_ in dict_.values():
            filename = object_.first_name + "_" + object_.last_name + ".json"
            with open(os.path.join(dir_, filename), 'w') as outfile:
                json.dump(object_.toJson(), outfile, indent=4)


if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())