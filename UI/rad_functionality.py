from PyQt5.QtWidgets import QMessageBox

def setup_functionality(app, ui):
    home_page_setup(ui)
    view_only_page_setup(ui)
    diagnose_page_setup(ui)
    patient_page_setup(ui)
    report_page_setup(ui)
    locked_page_setup(ui)


def home_page_setup(ui):
    ui.ui_rad.page_rad_home_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_rad.page_rad_home_button_lock_screen.clicked.connect(lambda: show_lock_screen_popup(ui))
    # ui.ui_rad.page_rad_home_button_view_profile.clicked.connect(lambda: change_page(ui, )) # TODO add profile page
    ui.ui_rad.page_rad_home_button_proceed.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_patient_page)) # TODO
    ui.ui_rad.page_rad_home_patient_information.itemClicked.connect(lambda: select_item(ui)) # TODO
    ui.ui_rad.page_rad_home_patient_information.itemDoubleClicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_patient_page)) # TODO


def view_only_page_setup(ui):
    ui.ui_rad.page_rad_view_only_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_rad.page_rad_view_only_button_back.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_patient_page))
    ui.ui_rad.page_rad_view_only_button_diagnose.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_diagnose))
    # ui.ui_rad.page_rad_view_only_button_2d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_3d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_hide_3d.clicked.connect(lambda: )# TODO Connect button with image functionality


def diagnose_page_setup(ui):
    ui.ui_rad.page_rad_diagnose_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_rad.page_rad_diagnose_button_back.clicked.connect(lambda: change_page(ui, ui.prev_page))
    ui.ui_rad.page_rad_diagnose_button_preview_report.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_report, False))
    # ui.ui_rad.page_rad_diagnose_button_2d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_2d_zoom_in.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_2d_zoom_out.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_3d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_hide_3d.clicked.connect(lambda: )# TODO Connect button with image functionality


def patient_page_setup(ui):
    ui.ui_rad.page_rad_patient_page_button_back.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_home))
    ui.ui_rad.page_rad_patient_page_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_rad.page_rad_patient_page_button_diagnose_patient.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_diagnose))
    ui.ui_rad.page_rad_patient_page_button_lock_screen.clicked.connect(lambda: lock_screen(ui)) # TODO
    ui.ui_rad.page_rad_patient_page_button_view_scan.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_view_only))


def report_page_setup(ui):
    ui.ui_rad.page_rad_report_button_back.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_diagnose, False))
    ui.ui_rad.page_rad_report_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    # ui.ui_rad.page_rad_report_button_preview_report.clicked.connect(lambda: )# TODO Remove?
    ui.ui_rad.page_rad_report_button_send_report.clicked.connect(lambda: show_send_report_popup(ui))
    # ui.ui_rad.page_rad_report_button_surgeon_view.clicked.connect(lambda: )# TODO connect to surgeon view
    # ui.ui_rad.page_rad_report_button_fullscreen.clicked.connect(lambda:)# TODO fullscreen
    # ui.ui_rad.page_rad_report_button_zoom_in.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_report_button_zoom_out.clicked.connect(lambda: )# TODO Connect button with image functionality


def locked_page_setup(ui):
    ui.ui_rad.page_rad_locked_button_login.clicked.connect(lambda: login(ui))


def change_page(ui, new_page, change_prev_page=True):
    if change_prev_page:
        ui.prev_page = ui.stacked_rad.currentWidget()
    ui.stacked_rad.setCurrentWidget(new_page)


def logout(ui):
    ui.prev_page = None
    ui.stacked_rad.setCurrentWidget(ui.ui_rad.page_rad_home)
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


def show_lock_screen_popup(ui):
    msg = QMessageBox()
    msg.setWindowTitle("Lock Screen")
    msg.setText("Are you sure you want to lock the screen?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes | msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        lock_screen(ui)


def send_report(ui):
    # TODO add functionality regarding sending the report here
    change_page(ui, ui.ui_rad.page_rad_home)


def show_send_report_popup(ui):
    msg = QMessageBox()
    msg.setWindowTitle("Send Report")
    msg.setText("Are you sure you want to send the report?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes | msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        send_report(ui)


def select_item(ui):
    ui.ui_rad.page_rad_home_button_proceed.setEnabled(True)


def login(ui):
    password = ui.ui_rad.page_rad_locked_insert_password.text()
    ui.ui_rad.page_rad_locked_insert_password.clear()
    if password in ["rad", ""]:
        ui.ui_rad.page_rad_incorrect_password.clear()
        change_page(ui, ui.prev_page, False)
    else:
        ui.ui_rad.page_rad_incorrect_password.setText("Incorrect password!")


def lock_screen(ui):
    change_page(ui, ui.ui_rad.page_rad_locked)


