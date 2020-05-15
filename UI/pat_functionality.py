from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
import os
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from reportGeneration.Report import Report

def setup_functionality(app, ui):
    home_page_setup(app, ui)
    errand_page_setup(app, ui)
    my_profile_page_setup(ui)
    image_status_page_setup(app, ui)
    view_scan_page_setup(app, ui)

def add_errands(app, ui):
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.clear()
    for errand in app.pat_dict[app.current_pat_id].errands.values():
        root_item = QTreeWidgetItem([app.current_pat_id, errand.date, errand.order_id, errand.status])
        ui.ui_pat.page_pat_home_treeWidget_treatment_list.addTopLevelItem(root_item)

def home_page_setup(app, ui):
    add_errands(app, ui)

    ui.ui_pat.page_pat_home_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_home_button_my_profile.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_my_profile))
    ui.ui_pat.page_pat_home_button_proceed.clicked.connect(lambda: go_to_errand_page(app, ui))
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemClicked.connect(lambda: ui.ui_pat.page_pat_home_button_proceed.setEnabled(True))
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemDoubleClicked.connect(
        lambda: go_to_errand_page(app, ui))

def go_to_errand_page(app, ui):
    app.current_errand_id = ui.ui_pat.page_pat_home_treeWidget_treatment_list.currentItem().text(2)

    ui.ui_pat.page_pat_errand_treeWidget_errand_list.clear()
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    root_item = QTreeWidgetItem([errand.task, errand.date, errand.scan, errand.status, errand.clinic])
    ui.ui_pat.page_pat_errand_treeWidget_errand_list.addTopLevelItem(root_item)
    ui.ui_pat.page_pat_errand_button_view.setEnabled(True if errand.status == "Complete" else False)

    # ui.ui_pat.page_pat_errand_report # TODO show radiology report here

    change_page(ui, ui.ui_pat.page_pat_errand)

def errand_page_setup(app, ui):
    ui.ui_pat.page_pat_errand_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_errand_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))
    ui.ui_pat.page_pat_errand_button_view_status.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_image_status)) # TODO
    # ui.ui_pat.page_pat_errand_button_share.clicked.connect() # TODO
    # ui.ui_pat.page_pat_errand_button_download.clicked.connect() # TODO
    ui.ui_pat.page_pat_errand_button_view.clicked.connect(lambda: go_to_view_scan_page(app, ui))
    ui.ui_pat.page_pat_errand_treeWidget_errand_list.itemDoubleClicked.connect(
        lambda: go_to_view_scan_page(app, ui) if ui.ui_pat.page_pat_errand_button_view.isEnabled() else None)


def my_profile_page_setup(ui):
    # ui.ui_pat.page_pat_my_profile_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_my_profile_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))


def image_status_page_setup(app, ui):
    ui.ui_pat.page_pat_image_status_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_image_status_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_errand))
    # ui.ui_pat.page_pat_image_status_button_request_notification.clicked.connect() # TODO


def go_to_view_scan_page(app, ui):
    app.visEngine.SetDirectory(os.path.join("sample_dicom", "chestDICOM")) # TODO Add directory to the patient/errand class
    app.visEngine.SetupImageUI(ui.ui_pat.page_pat_view_scan_2d_view)
    app.visEngine.SetupVolumeUI(ui.ui_pat.page_pat_view_scan_3d_view)

    # ui.ui_pat.page_pat_view_scan_2d_view # TODO Add vtk 2d window here
    # ui.ui_pat.page_pat_view_scan_3d_view # TODO Add vtk 3d window here
    # ui.ui_pat.page_pat_view_scan_rad_annotations # TODO Radiologists annotation for selected object
    change_page(ui, ui.ui_pat.page_pat_view_scan)

class Examination:
    def __init__(self, patient, modality):
        self.patient = patient
        self.modality = modality
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations += [annotation]

    def get_annotation(self, annot_id):
        for annot in self.annotations:
            if annot.annot_id == annot_id:
                return annot
        return None

class Patient:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class Annotation:
    def __init__(self, annot_id, location, finding, color):
        self.location = location
        self.finding = finding
        self.color = color
        self.annot_id = annot_id

    def __str__(self):
        return "Location: {}\n" \
               "Finding: {}\n" \
               "Annotation ID: {}".format(self.location, self.finding, self.annot_id)



def view_scan_page_setup(app, ui):
    ui.ui_pat.page_pat_view_scan_2d_view = QVTKRenderWindowInteractor(ui.ui_pat.page_pat_view_scan_2d_view_frame)
    ui.ui_pat.page_pat_view_scan_3d_view = QVTKRenderWindowInteractor(ui.ui_pat.page_pat_view_scan_3d_view_frame)

    patient = Patient("Nils", "Gehlin", 26)
    exam = Examination(patient, "CT")
    exam.add_annotation(Annotation(1, "Brain Parenchyma", "T2 hyperintense white matter lesions", (255, 0, 0)))
    exam.add_annotation(Annotation(2, "Skull", "Huge fracture", (0, 255, 0)))

    ui.ui_pat.page_pat_view_scan_rad_annotations = Report(ui.ui_pat.page_pat_view_scan_rad_annotations_frame,
                                                          template_name="radiologist",
                                                          examination=exam)

    ui.ui_pat.page_pat_view_scan_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_view_scan_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_errand))

    # ui.ui_pat.page_pat_view_scan_button_next_note.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_next_slice.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_play_pause.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_previous_note.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_previous_slice.clicked.connect()# TODO Connect button with image functionality
    #
    ui.ui_pat.page_pat_view_scan_button_3d_bone_view.clicked.connect(lambda: app.visEngine.SetTissue(ui.ui_pat.page_pat_view_scan_3d_view, "BONE"))# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_3d_fullscreen.clicked.connect()# TODO Connect button with image functionality
    ui.ui_pat.page_pat_view_scan_button_3d_tissue_view.clicked.connect(lambda: app.visEngine.SetTissue(ui.ui_pat.page_pat_view_scan_3d_view, "SOFT"))# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_down.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_left.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_right.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_up.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_zoom_in.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_zoom_out.clicked.connect()# TODO Connect button with image functionality

def change_page(ui, new_page):
    ui.prev_page = ui.stacked_pat.currentWidget()
    ui.stacked_pat.setCurrentWidget(new_page)


def logout(ui):
    ui.prev_page = None
    ui.ui_pat.page_pat_home_button_proceed.setEnabled(False)
    ui.stacked_pat.setCurrentWidget(ui.ui_pat.page_pat_home)
    ui.stacked_main.setCurrentWidget(ui.page_login)


def show_logout_popup(app, ui):
    msg = QMessageBox()
    msg.setWindowTitle("Logout")
    msg.setText("Are you sure you want to logout?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes|msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        app.current_pat_id = None
        logout(ui)


def select_item(app, ui):
    app.current_errand_id = ui.ui_pat.page_pat_home_treeWidget_treatment_list.currentItem().text(2)
    ui.ui_pat.page_pat_home_button_proceed.setEnabled(True)


