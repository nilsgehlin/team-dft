from PyQt5.QtWidgets import QMessageBox

def setup_functionality(ui):
    home_page_setup(ui)
    errand_page_setup(ui)
    my_profile_page_setup(ui)
    image_status_page_setup(ui)
    view_scan_page_setup(ui)


def home_page_setup(ui):
    ui.ui_pat.page_pat_home_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_home_button_my_profile.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_my_profile))
    ui.ui_pat.page_pat_home_button_proceed.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_errand)) # TODO
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemClicked.connect(lambda: select_item(ui)) # TODO
    ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemDoubleClicked.connect(
        lambda: change_page(ui, ui.ui_pat.page_pat_errand)) # TODO


def errand_page_setup(ui):
    ui.ui_pat.page_pat_errand_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_errand_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))
    ui.ui_pat.page_pat_errand_button_view_status.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_image_status)) # TODO
    # ui.ui_pat.page_pat_errand_button_share.clicked.connect() # TODO
    # ui.ui_pat.page_pat_errand_button_download.clicked.connect() # TODO
    ui.ui_pat.page_pat_errand_button_view.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_view_scan))


def my_profile_page_setup(ui):
    # ui.ui_pat.page_pat_my_profile_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_my_profile_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))


def image_status_page_setup(ui):
    ui.ui_pat.page_pat_image_status_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_image_status_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_errand))
    # ui.ui_pat.page_pat_image_status_button_request_notification.clicked.connect() # TODO


def view_scan_page_setup(ui):
    ui.ui_pat.page_pat_view_scan_button_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_view_scan_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_errand))

    # ui.ui_pat.page_pat_view_scan_button_next_note.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_next_slice.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_play_pause.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_previous_note.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_previous_slice.clicked.connect()# TODO Connect button with image functionality
    #
    # ui.ui_pat.page_pat_view_scan_button_3d_bone_view.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_3d_fullscreen.clicked.connect()# TODO Connect button with image functionality
    # ui.ui_pat.page_pat_view_scan_button_3d_tissue_view.clicked.connect()# TODO Connect button with image functionality
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
    ui.stacked_pat.setCurrentWidget(ui.ui_pat.page_pat_home)
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


def select_item(ui):
    ui.ui_pat.page_pat_home_button_proceed.setEnabled(True)


