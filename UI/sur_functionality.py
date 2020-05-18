from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import Qt

def setup_functionality(app, ui):
    home_page_setup(app, ui)
    patient_errand_page_setup(app, ui)
    view_edit_page_setup(ui)
    # diagnose_page_setup(ui)
    # patient_page_setup(ui)
    # report_page_setup(ui)
    # locked_page_setup(ui)

## SETUP FUNCTIONS ##

def home_page_setup(app, ui):
    add_errands(app, ui)
    ui.ui_sur.page_sur_home_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_sur.page_sur_home_button_my_profile.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_my_profile))
    ui.ui_sur.page_sur_home_button_proceed.clicked.connect(lambda: go_to_patient_errand_page(app, ui)) # TODO
    ui.ui_sur.page_sur_home_treatment_list.itemClicked.connect(lambda: ui.ui_sur.page_sur_home_button_proceed.setEnabled(True)) # TODO
    ui.ui_sur.page_sur_home_treatment_list.itemDoubleClicked.connect(
        lambda: go_to_patient_errand_page(app, ui)) # TODO


def patient_errand_page_setup(app, ui):
    ui.ui_sur.page_sur_patient_errand_button_back.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_home))
    ui.ui_sur.page_sur_patient_errand_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    # ui.ui_sur.page_sur_patient_errand_button_download.clicked.connect(lambda: pass) # TODO Not sure if we need this atm
    # ui.ui_sur.page_sur_patient_errand_button_share.clicked.connect(lambda: pass) # TODO Not sure if we need this atm
    ui.ui_sur.page_sur_patient_errand_button_view.clicked.connect(lambda: go_to_view_edit_page(app, ui))
    # ui.ui_sur.page_sur_patient_errand_errand_list.itemClicked.connect(lambda: ) # TODO Add to change radiology report
    ui.ui_sur.page_sur_patient_errand_errand_list.itemDoubleClicked.connect(
        lambda: go_to_view_edit_page(app, ui)) # TODO


def view_edit_page_setup(ui):

    ui.ui_sur.page_sur_view_edit_button_back.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_patient_errand))
    ui.ui_sur.page_sur_view_edit_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    # ui.ui_sur.page_sur_view_edit_button_preview_report.clicked.connect(lambda: ) # TODO Is this one needed here?

    # 2D
    # ui.ui_sur.page_sur_view_edit_button_2d_zoom_in.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_zoom_out.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_fullscreen.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_play_paus.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_previous_note.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_previous_slice.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_next_note.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_2d_next_slice.clicked.connect(lambda: )
    #
    # # 3D
    # ui.ui_sur.page_sur_view_edit_button_3d_left.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_right.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_up.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_down.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_zoom_in.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_zoom_out.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_fullscreen.clicked.connect(lambda: )
    # ui.ui_sur.page_sur_view_edit_button_3d_hide.clicked.connect(lambda: )
    #
    # # Both
    # ui.ui_sur.page_sur_view_edit_button_3d_toggle_annotations
    # ui.ui_sur.page_sur_view_edit_button_3d_fullscreen_2
    # ui.ui_sur.page_sur_view_edit_button_3d_bone_view
    # ui.ui_sur.page_sur_view_edit_button_3d_tissue_view


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

    if app.current_errand_id is not None:
        ui.ui_sur.page_sur_patient_errand_button_view.setEnabled(True)
        # ui.ui_sur.page_sur_patient_errand_rad_report # TODO Display radiology report here
        pass

    change_page(ui, ui.ui_sur.page_sur_patient_errand)


def go_to_view_edit_page(app, ui):
    pass # HÄR ÄR DU MARTIN





## HELP FUNCTIONS ##

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
