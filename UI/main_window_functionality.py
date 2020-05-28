import os

def setup_functionality(app, ui):
    login_page_setup(app, ui)
    menu_bar_setup(app, ui)


def login_page_setup(app, ui):
    ui.page_login_button_login.clicked.connect(lambda: login(app, ui))


def menu_bar_setup(app, ui):
    ui.menu_bar_theme_button_day_mode.triggered.connect(lambda: change_style_sheet(app, ui, ui.menu_bar_theme_button_day_mode, "patient_mint.qss"))
    ui.menu_bar_theme_button_night_mode.triggered.connect(lambda: change_style_sheet(app, ui, ui.menu_bar_theme_button_night_mode, "patient_mint_dark.qss"))


def change_style_sheet(app, ui, new_button, filename):
    new_button.setChecked(True)
    if app.current_theme_button_pressed is not new_button:
        app.current_theme_button_pressed.setChecked(False)
        app.current_theme_button_pressed = new_button
        set_style_sheet(ui, filename)


def set_style_sheet(ui, filename):
    with open(os.path.join("UI", "StyleSheets", filename)) as style_sheet_file:
        ui.main_window.setStyleSheet("")
        ui.main_window.setStyleSheet(style_sheet_file.read())



def login(app, ui):
    id = ui.page_login_insert_id.text()
    password = ui.page_login_insert_password.text()
    ui.page_login_insert_id.clear()
    ui.page_login_insert_password.clear()
    user_type = ui.page_login_combobox_user_type.currentText()
    if user_type == "Patient":
        if id_and_password_ok(app.pat_dict, id, password):
            app.current_pat_id = id
            app.init_pat()
            change_style_sheet(app, ui, ui.menu_bar_theme_button_day_mode, "patient_mint.qss")
            ui.stacked_main.setCurrentWidget(ui.page_pat)
    elif user_type == "Radiologist":
        if id_and_password_ok(app.rad_dict, id, password):
            app.current_rad_id = id
            app.init_rad()
            ui.stacked_main.setCurrentWidget(ui.page_rad)
    elif user_type == "Surgeon":
        print(id)
        print(password)
        if id_and_password_ok(app.sur_dict, id, password):
            print("OK")
            app.current_sur_id = id
            app.init_sur()
            ui.stacked_main.setCurrentWidget(ui.page_sur)
    else:
        print("WRONG USER ID OR PASSWORD")  # TODO Add something for wrong username and password


def id_and_password_ok(data, id, password):
    try:
        if data[id].password == password:
            return True
    except KeyError:
        return False
    return False
