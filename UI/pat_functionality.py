from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
import os
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from reportGeneration.Report import Report
import UI.patient
import visualizationEngine.annotation.Annotation


# SETUP FUNCTIONS #


def setup_functionality(app, ui):
    home_page_setup(app, ui)
    errand_page_setup(app, ui)
    my_profile_page_setup(ui)
    image_status_page_setup(app, ui)
    view_scan_page_setup(app, ui)


def home_page_setup(app, ui):
    add_errands(app, ui)

    ui.ui_pat.page_pat_home_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_home_button_my_profile.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_my_profile))
    ui.ui_pat.page_pat_home_button_proceed.clicked.connect(lambda: go_to_errand_page(app, ui))
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemClicked.connect(lambda: ui.ui_pat.page_pat_home_button_proceed.setEnabled(True))
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemDoubleClicked.connect(
        lambda: go_to_errand_page(app, ui))


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


def view_scan_page_setup(app, ui):
    ui.ui_pat.page_pat_view_scan_rad_annotations = Report(ui.ui_pat.page_pat_view_scan_rad_annotations_frame)
    ui.ui_pat.page_pat_view_scan_rad_annotations_frame_grid.addWidget(ui.ui_pat.page_pat_view_scan_rad_annotations, 0, 0, 1, 1)

    ui.ui_pat.page_pat_view_scan_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_view_scan_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_errand))

    # ui.ui_pat.page_pat_view_scan_button_next_note.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_next_slice.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_play_pause.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_previous_note.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_previous_slice.clicked.connect()# TODO Connect button with image functionality

    ui.ui_pat.page_pat_view_scan_button_link_windows.clicked.connect(lambda: change_link(app, ui, ui.ui_pat.page_pat_view_scan_button_link_windows,
                                                                                         ui.ui_pat.page_pat_view_scan_2d_view, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_3d_bone_view.clicked.connect(lambda: app.visEngine.SetTissue(ui.ui_pat.page_pat_view_scan_3d_view, "BONE"))
    # ui.ui_pat.page_pat_view_scan_button_3d_fullscreen.clicked.connect()# TODO Connect button with image functionality
    ui.ui_pat.page_pat_view_scan_button_3d_tissue_view.clicked.connect(lambda: app.visEngine.SetTissue(ui.ui_pat.page_pat_view_scan_3d_view, "SOFT"))
    # ui.ui_pat.page_pat_view_scan_button_down.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_left.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_right.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_up.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_zoom_in.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_zoom_out.clicked.connect()# TODO Connect button with image functionality


# GO TO FUNCTIONS #


def go_to_errand_page(app, ui):
    app.current_errand_id = ui.ui_pat.page_pat_home_treeWidget_treatment_list.currentItem().text(2)
    ui.ui_pat.page_pat_errand_treeWidget_errand_list.clear()
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    root_item = QTreeWidgetItem([errand.task, errand.date, errand.scan, errand.status, errand.clinic])
    ui.ui_pat.page_pat_errand_treeWidget_errand_list.addTopLevelItem(root_item)
    ui.ui_pat.page_pat_errand_button_view.setEnabled(True if errand.status == "Complete" else False)

    # ui.ui_pat.page_pat_errand_report # TODO show radiology report here

    change_page(ui, ui.ui_pat.page_pat_errand)


def go_to_view_scan_page(app, ui):
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    if app.visEngine._dir is not errand.data_dir:
        ui.ui_pat.page_pat_view_scan_2d_view = QVTKRenderWindowInteractor(ui.ui_pat.page_pat_view_scan_2d_view_frame)
        ui.ui_pat.page_pat_view_scan_2d_view_frame_grid.addWidget(ui.ui_pat.page_pat_view_scan_2d_view, 0, 0, 1, 1)

        ui.ui_pat.page_pat_view_scan_3d_view = QVTKRenderWindowInteractor(ui.ui_pat.page_pat_view_scan_3d_view_frame)
        ui.ui_pat.page_pat_view_scan_3d_view_frame_grid.addWidget(ui.ui_pat.page_pat_view_scan_3d_view, 0, 0, 1, 1)

        app.visEngine.SetDirectory(errand.data_dir)
        app.visEngine.SetupImageUI(ui.ui_pat.page_pat_view_scan_2d_view)
        app.visEngine.SetupVolumeUI(ui.ui_pat.page_pat_view_scan_3d_view)

        ui.ui_pat.page_pat_view_scan_button_link_windows.setText("Activate\n2D-3D Link")

    ui.ui_pat.page_pat_view_scan_rad_annotations.load_report(template_name="radiologist",
                                                             patient=app.pat_dict[app.current_pat_id],
                                                             order_id=app.current_errand_id,
                                                             vtk_widget_2d=ui.ui_pat.page_pat_view_scan_2d_view,
                                                             vtk_widget_3d=ui.ui_pat.page_pat_view_scan_3d_view)
    change_page(ui, ui.ui_pat.page_pat_view_scan)


# HELP FUNCTIONS #


def add_errands(app, ui):
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.clear()
    for errand in app.pat_dict[app.current_pat_id].errands.values():
        root_item = QTreeWidgetItem([app.current_pat_id, errand.date, errand.order_id, errand.status])
        ui.ui_pat.page_pat_home_treeWidget_treatment_list.addTopLevelItem(root_item)


def change_link(app, ui, button, master_widget, slave_widget):
    deactivate_str = "Deactivate\n2D-3D Link"
    activate_str = "Activate\n2D-3D Link"
    if button.text() == deactivate_str:
        app.visEngine.UnlinkWindows(master_widget)
        button.setText(activate_str)
    elif button.text() == activate_str:
        app.visEngine.LinkWindows(master_widget, slave_widget)
        button.setText(deactivate_str)


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


