

def setup_functionality(ui):
    login_page_setup(ui)


def login_page_setup(ui):
    ui.button_login.clicked.connect(lambda: login(ui))


def login(ui):
    user_type = ui.combo_box_login.currentText()
    if user_type == "Patient":
        ui.stacked_main.setCurrentWidget(ui.page_pat)
    if user_type == "Radiologist":
        ui.stacked_main.setCurrentWidget(ui.page_rad)
    if user_type == "Doctor":
        ui.stacked_main.setCurrentWidget(ui.page_sur)