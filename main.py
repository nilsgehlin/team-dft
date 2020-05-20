import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import os, sys
path = os.path.join("UI")
sys.path.insert(0, path)
from ui import Ui
import main_window_functionality as f_mw
import pat_functionality as f_pat
import rad_functionality as f_rad
import sur_functionality as f_sur
from patient import Patient, Errand

import os, sys
path = os.path.join("visualizationEngine")
sys.path.insert(0, path)
from visualizationEngine.VisualizationEngine import VisualizationEngine
from visualizationEngine.annotation.annotation import Annotation

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
        jane_smith = Patient("Jane", "Smith", 26, "F")

        jane_errand_1 = Errand("2020-01-01", "Complete", "CT", "GP", "TASK??", os.path.join("sample_dicom", "chestDICOM"))
        jane_errand_2 = Errand("2020-03-03", "Pending", "MRI", "Hospital", "TASK??", os.path.join("sample_dicom", "chestDICOM"))
        jane_smith.add_errand(jane_errand_1)
        jane_smith.add_errand(jane_errand_2)

        # Dummy annotations until we can create annotations in the software
        jane_errand_1.add_annotation(Annotation("Brain Parenchyma", "T2 hyperintense white matter lesions", (255, 0, 0)))
        jane_errand_1.add_annotation(Annotation("Skull", "Huge fracture", (0, 255, 0)))
        jane_errand_2.add_annotation(Annotation("Shoulder", "Tare", (0, 255, 0)))


        mark_johnson = Patient("Mark", "Johnson", 48, "M")
        mark_errand_1 = Errand("2019-12-12", "Complete", "CT", "CT clinic", "TASK??", os.path.join("sample_dicom", "chestDICOM"))
        mark_johnson.add_errand(mark_errand_1)

        pat_dict = {jane_smith.id: jane_smith, mark_johnson.id: mark_johnson}
        return pat_dict



if __name__ == "__main__":
    Qapp = QtWidgets.QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(Qapp.exec_())