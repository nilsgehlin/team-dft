

def setup_functionality(app, ui):
    login_page_setup(app, ui)


def login_page_setup(app, ui):
    ui.page_login_button_login.clicked.connect(lambda: login(app, ui))


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
