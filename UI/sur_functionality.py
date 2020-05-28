from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import Qt
from reportGeneration.Report import Report
from PyQt5.QtGui import QPixmap
import os

def setup_functionality(app, ui):
    home_page_setup(app, ui)
    patient_errand_page_setup(app, ui)
    view_edit_page_setup(app, ui)
    # diagnose_page_setup(ui)
    # patient_page_setup(ui)
    # report_page_setup(ui)
    # locked_page_setup(ui)

## SETUP FUNCTIONS ##

def home_page_setup(app, ui):
    add_errands(app, ui)
    ui.ui_sur.page_sur_home_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_sur.page_sur_home_button_colleagues.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_my_profile))
    ui.ui_sur.page_sur_home_button_proceed.clicked.connect(lambda: go_to_patient_errand_page(app, ui)) # TODO
    ui.ui_sur.page_sur_home_treatment_list.itemClicked.connect(lambda: ui.ui_sur.page_sur_home_button_proceed.setEnabled(True)) # TODO
    ui.ui_sur.page_sur_home_treatment_list.itemDoubleClicked.connect(
        lambda: go_to_patient_errand_page(app, ui)) # TODO


def patient_errand_page_setup(app, ui):
    ui.ui_sur.page_sur_patient_errand_report = Report(ui.ui_sur.page_sur_patient_errand_report_frame, show_segmentation_on_click=False)
    ui.ui_sur.page_sur_patient_errand_report_frame_grid.addWidget(ui.ui_sur.page_sur_patient_errand_report, 0, 0, 1, 1)

    ui.ui_sur.page_sur_patient_errand_button_back.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_home))
    ui.ui_sur.page_sur_patient_errand_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    # ui.ui_sur.page_sur_patient_errand_button_download.clicked.connect(lambda: pass) # TODO Not sure if we need this atm
    # ui.ui_sur.page_sur_patient_errand_button_share.clicked.connect(lambda: pass) # TODO Not sure if we need this atm
    ui.ui_sur.page_sur_patient_errand_button_view.clicked.connect(lambda: go_to_view_edit_page(app, ui))
    ui.ui_sur.page_sur_patient_errand_errand_list.itemClicked.connect(
        lambda: change_report(app, ui.ui_sur.page_sur_patient_errand_errand_list, ui.ui_sur.page_sur_patient_errand_report))
    ui.ui_sur.page_sur_patient_errand_errand_list.itemDoubleClicked.connect(
        lambda: go_to_view_edit_page(app, ui))


def view_edit_page_setup(app, ui):
    ui.ui_sur.page_sur_view_edit_report = Report(ui.ui_sur.page_sur_view_edit_report_frame)
    ui.ui_sur.page_sur_view_edit_report_frame_grid.addWidget(ui.ui_sur.page_sur_view_edit_report, 0, 0, 1, 1)

    ui.ui_sur.page_sur_view_edit_button_back.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_patient_errand))
    ui.ui_sur.page_sur_view_edit_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    # ui.ui_sur.page_sur_view_edit_button_preview_report.clicked.connect(lambda: ) # TODO Is this one needed here?

    ui.ui_sur.page_sur_view_edit_button_link_windows.clicked.connect(
        lambda: change_link(app, ui, ui.ui_sur.page_sur_view_edit_button_link_windows,
                            ui.ui_sur.page_sur_view_edit_2d_view, ui.ui_sur.page_sur_view_edit_3d_view))

    # 2D image options
    ui.ui_sur.page_sur_view_edit_2d_slider_color_window.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_2d_slider_color_level.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))


## GO TO FUNCTIONS ##

def go_to_patient_errand_page(app, ui):
    current_item = ui.ui_sur.page_sur_home_treatment_list.currentItem()
    if current_item.parent() is None:
        app.current_pat_id = current_item.text(2)
        errands_list = list(app.pat_dict[app.current_pat_id].errands.values())
        app.current_errand_id = None if not errands_list else errands_list[0].order_id
    else:
        app.current_pat_id = current_item.parent().text(2)
        app.current_errand_id = current_item.text(7)

    ui.ui_sur.page_sur_patient_errand_errand_list.clear()
    patient = app.pat_dict[app.current_pat_id]
    for errand in patient.errands.values():
        root_item = QTreeWidgetItem([errand.order_id, errand.date, errand.scan, errand.clinic, errand.status])
        ui.ui_sur.page_sur_patient_errand_errand_list.addTopLevelItem(root_item)
        if app.current_errand_id is not None and app.current_errand_id == errand.order_id:
            ui.ui_sur.page_sur_patient_errand_errand_list.setCurrentItem(root_item)

    ui.ui_sur.page_sur_patient_errand_errand_list.sortItems(1, Qt.DescendingOrder)

    if app.current_errand_id is None:
        ui.ui_sur.page_sur_patient_errand_button_view.setEnabled(False)
        ui.ui_sur.page_sur_patient_errand_report.setText("Select one of " + patient.first_name + "'s complete scans to see the radiology report")
    else:
        ui.ui_sur.page_sur_patient_errand_button_view.setEnabled(True)
        errand = patient.errands[app.current_errand_id]
        if errand.status.lower() == "complete":
            ui.ui_sur.page_sur_patient_errand_report.load_report(template_name="radiologist",
                                                            patient=app.pat_dict[app.current_pat_id],
                                                            order_id=app.current_errand_id)
        else:
            ui.ui_sur.page_sur_patient_errand_report.setText("No radiology report available for this scan")

    add_patient_profile(app, ui)

    change_page(ui, ui.ui_sur.page_sur_patient_errand)


def go_to_view_edit_page(app, ui):
    ui.ui_sur.page_sur_view_edit_2d_view = QVTKRenderWindowInteractor(ui.ui_sur.page_sur_view_edit_2d_view_frame)
    ui.ui_sur.page_sur_view_edit_2d_view_frame_grid.addWidget(ui.ui_sur.page_sur_view_edit_2d_view, 0, 0, 1, 1)

    ui.ui_sur.page_sur_view_edit_3d_view = QVTKRenderWindowInteractor(ui.ui_sur.page_sur_view_edit_3d_view_frame)
    ui.ui_sur.page_sur_view_edit_3d_view_frame_grid.addWidget(ui.ui_sur.page_sur_view_edit_3d_view, 0, 0, 1, 1)

    app.current_errand_id = ui.ui_sur.page_sur_patient_errand_errand_list.currentItem().text(0)

    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    app.visEngine.SetDirectory(errand.data_dir)
    app.visEngine.SetupImageUI(ui.ui_sur.page_sur_view_edit_2d_view)
    app.visEngine.SetupVolumeUI(ui.ui_sur.page_sur_view_edit_3d_view)

    if errand.status.lower() == "complete":
        ui.ui_sur.page_sur_view_edit_report.load_report(template_name="radiologist",
                                                        patient=app.pat_dict[app.current_pat_id],
                                                        order_id=app.current_errand_id,
                                                        vtk_widget_2d=ui.ui_sur.page_sur_view_edit_2d_view,
                                                        vtk_widget_3d=ui.ui_sur.page_sur_view_edit_3d_view,
                                                        vis_engine=app.visEngine)
    else:
        ui.ui_sur.page_sur_view_edit_report.setText("No Radiology Report Available")

    change_page(ui, ui.ui_sur.page_sur_view_edit)


# HELP FUNCTIONS #

def change_link(app, ui, button, master_widget, slave_widget):
    deactivate_str = "Deactivate\n2D-3D Link"
    activate_str = "Activate\n2D-3D Link"
    if button.text() == deactivate_str:
        app.visEngine.UnlinkWindows(master_widget)
        button.setText(activate_str)
    elif button.text() == activate_str:
        app.visEngine.LinkWindows(master_widget, [slave_widget])
        button.setText(deactivate_str)


def add_errands(app, ui):
    ui.ui_sur.page_sur_home_treatment_list.clear()
    for pat in app.pat_dict.values():
        root_item = QTreeWidgetItem([pat.last_name, pat.first_name, pat.id, pat.sex])
        for errand in pat.errands.values():
            child_item = QTreeWidgetItem([None, None, None, None, errand.date, errand.scan, errand.status, errand.order_id])
            root_item.addChild(child_item)
        ui.ui_sur.page_sur_home_treatment_list.addTopLevelItem(root_item)
    ui.ui_sur.page_sur_home_treatment_list.sortItems(4, Qt.DescendingOrder)


#
# def locked_page_setup(ui):
#     ui.ui_rad.page_rad_locked_button_login.clicked.connect(lambda: login(ui))
#
#
def change_page(ui, new_page, change_prev_page=True):
    if change_prev_page:
        ui.prev_page = ui.stacked_sur.currentWidget()
    ui.stacked_sur.setCurrentWidget(new_page)


def logout(ui):
    ui.current_sur_id = None
    ui.prev_page = None
    ui.stacked_sur.setCurrentWidget(ui.ui_sur.page_sur_home)
    ui.stacked_main.setCurrentWidget(ui.page_login)


def show_logout_popup(ui):
    msg = QMessageBox()
    msg.setWindowTitle("Logout")
    msg.setText("Are you sure you want to logout?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes|msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        logout(ui)


def change_image_color(app, ui, widget):
    color_window = ui.ui_sur.page_sur_view_edit_2d_slider_color_window.value()
    color_level = ui.ui_sur.page_sur_view_edit_2d_slider_color_level.value()
    app.visEngine.SetImageColor(widget, color_window, color_level)


def change_report(app, tree_widget, report_widget):
    app.current_errand_id = tree_widget.currentItem().text(0)
    if app.pat_dict[app.current_pat_id].errands[app.current_errand_id].status.lower() == "complete":
        report_widget.load_report(template_name="patient", patient=app.pat_dict[app.current_pat_id],
                                  order_id=app.current_errand_id)
    else:
        report_widget.setText("No radiology report available for this scan")
    pass


def add_patient_profile(app, ui):
    patient = app.pat_dict[app.current_pat_id]
    ui.ui_sur.page_sur_patient_errand_label_patients_scans.setText(patient.first_name + "'s Scans")
    ui.ui_sur.page_sur_patient_errand_label_patients_profile.setText(patient.first_name + "'s Profile")
    ui.ui_sur.page_sur_patient_errand_label_name.setText(patient.first_name + " " + patient.last_name)
    ui.ui_sur.page_sur_patient_errand_label_age.setText(str(patient.age) + " years old")
    ui.ui_sur.page_sur_patient_errand_label_phone_number.setText("+1 415 201 4987")
    ui.ui_sur.page_sur_patient_errand_label_address.setText("72 Sunshine St\nSan Francisco, CA 94114, USA")
    ui.ui_sur.page_sur_patient_errand_label_email.setText(patient.first_name.lower() + "." + patient.last_name.lower() + "@gmail.com")
    pixmap = QPixmap(os.path.join("databases", "patient_database", patient.first_name.lower() + "_" + patient.last_name.lower() + ".png"))
    if pixmap.isNull():
        ui.ui_sur.page_sur_patient_errand_label_profile_picture.setText("No profile picture available")
    else:
        ui.ui_sur.page_sur_patient_errand_label_profile_picture.setPixmap(pixmap)


# def show_lock_screen_popup(ui):
#     msg = QMessageBox()
#     msg.setWindowTitle("Lock Screen")
#     msg.setText("Are you sure you want to lock the screen?")
#     msg.setIcon(msg.Question)
#
#     msg.setStandardButtons(msg.Yes | msg.No)
#     msg.setDefaultButton(msg.No)
#     msg.setEscapeButton(msg.No)
#
#     ret = msg.exec_()
#     if ret == msg.Yes:
#         lock_screen(ui)
#
#
# def send_report(ui):
#     # TODO add functionality regarding sending the report here
#     change_page(ui, ui.ui_rad.page_rad_home)
#
#
# def show_send_report_popup(ui):
#     msg = QMessageBox()
#     msg.setWindowTitle("Send Report")
#     msg.setText("Are you sure you want to send the report?")
#     msg.setIcon(msg.Question)
#
#     msg.setStandardButtons(msg.Yes | msg.No)
#     msg.setDefaultButton(msg.No)
#     msg.setEscapeButton(msg.No)
#
#     ret = msg.exec_()
#     if ret == msg.Yes:
#         send_report(ui)


# def select_item(ui):
#     ui.ui_sur.page_sur_home_button_proceed.setEnabled(True)


# def login(ui):
#     password = ui.ui_rad.page_rad_locked_insert_password.text()
#     ui.ui_rad.page_rad_locked_insert_password.clear()
#     if password in ["rad", ""]:
#         ui.ui_rad.page_rad_incorrect_password.clear()
#         change_page(ui, ui.prev_page, False)
#     else:
#         ui.ui_rad.page_rad_incorrect_password.setText("Incorrect password!")
#
#
# def lock_screen(ui):
#     change_page(ui, ui.ui_rad.page_rad_locked)
