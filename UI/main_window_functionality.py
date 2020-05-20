from qtstyles import StylePicker, Sheet
import os

def setup_functionality(app, ui):
    login_page_setup(app, ui)
    menu_bar_setup(app, ui)


def login_page_setup(app, ui):
    ui.page_login_button_login.clicked.connect(lambda: login(app, ui))


def menu_bar_setup(app, ui):
    ui.menu_bar_theme_button_day_mode.triggered.connect(lambda: change_style_sheet(app, ui, ui.menu_bar_theme_button_day_mode, "Aqua.qss"))
    ui.menu_bar_theme_button_night_mode.triggered.connect(lambda: change_style_sheet(app, ui, ui.menu_bar_theme_button_night_mode, "ManjaroMix.qss"))


def change_style_sheet(app, ui, new_button, filename):
    if app.current_theme_button_pressed is new_button:
        new_button.setChecked(True)
    else:
        app.current_theme_button_pressed.setChecked(False)
        app.current_theme_button_pressed = new_button
        set_style_sheet(ui, filename)


def set_style_sheet(ui, filename):
    sheet = Sheet(os.path.join("UI", "StyleSheets", filename))
    sheet._load_contents()
    ui.main_window.setStyleSheet(sheet._contents)


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
            ui.stacked_main.setCurrentWidget(ui.page_pat)
    elif user_type == "Radiologist":
        if id == "0000" and password == "0000":
            app.init_rad()
            ui.stacked_main.setCurrentWidget(ui.page_rad)
    elif user_type == "Surgeon":
        if id == "0000" and password == "0000":
            app.init_sur()
            ui.stacked_main.setCurrentWidget(ui.page_sur)


def id_and_password_ok(data, id, password):
    try:
        if data[id].password == password:
            return True
    except KeyError:
        return False
    return False
