from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import Qt
from reportGeneration.Report import Report

# SETUP FUNCTIONS #


def setup_functionality(app, ui):
    home_page_setup(app, ui)
    view_only_page_setup(app, ui)
    diagnose_page_setup(app, ui)
    patient_page_setup(app, ui)
    report_page_setup(app, ui)
    locked_page_setup(ui)


def home_page_setup(app, ui):
    add_errands(app, ui)
    ui.ui_rad.page_rad_home_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_home_button_lock_screen.clicked.connect(lambda: show_lock_screen_popup(ui))
    # ui.ui_rad.page_rad_home_button_view_profile.clicked.connect(lambda: change_page(ui, )) # TODO add profile page
    ui.ui_rad.page_rad_home_button_proceed.clicked.connect(lambda: go_to_patient_page(app, ui)) # TODO
    ui.ui_rad.page_rad_home_patient_information.itemClicked.connect(lambda: select_item(ui)) # TODO
    ui.ui_rad.page_rad_home_patient_information.itemDoubleClicked.connect(lambda: go_to_patient_page(app, ui)) # TODO


def patient_page_setup(app, ui):
    ui.ui_rad.page_rad_patient_page_button_back.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_home))
    ui.ui_rad.page_rad_patient_page_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_patient_page_button_diagnose_patient.clicked.connect(lambda: go_to_diagnose_page(app, ui))
    ui.ui_rad.page_rad_patient_page_button_lock_screen.clicked.connect(lambda: lock_screen(ui)) # TODO
    ui.ui_rad.page_rad_patient_page_button_view_scan.clicked.connect(lambda: go_to_view_only_page(app, ui))


def view_only_page_setup(app, ui):
    ui.ui_rad.page_rad_view_only_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_view_only_button_back.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_patient_page))
    ui.ui_rad.page_rad_view_only_button_diagnose.clicked.connect(lambda: go_to_diagnose_page(app, ui))
    ui.ui_rad.page_rad_view_only_button_hide_link_windows.clicked.connect(lambda: change_link(app, ui, ui.ui_rad.page_rad_view_only_button_hide_link_windows,
                                                                                              ui.ui_rad.page_rad_view_only_2d_view, ui.ui_rad.page_rad_view_only_3d_view))
    # ui.ui_rad.page_rad_view_only_button_2d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_3d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_hide_3d.clicked.connect(lambda: )# TODO Connect button with image functionality


def diagnose_page_setup(app, ui):
    ui.ui_rad.page_rad_diagnose_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_diagnose_button_back.clicked.connect(lambda: go_back_from_diagnose_page(app, ui))
    ui.ui_rad.page_rad_diagnose_button_preview_report.clicked.connect(lambda: go_to_report_page(app, ui))
    ui.ui_rad.page_rad_diagnose_button_link_windows.clicked.connect(lambda: change_link(app, ui, ui.ui_rad.page_rad_diagnose_button_link_windows,
                                                                                              ui.ui_rad.page_rad_diagnose_2d_view, ui.ui_rad.page_rad_diagnose_3d_view))
    # ui.ui_rad.page_rad_diagnose_button_2d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_2d_zoom_in.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_2d_zoom_out.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_3d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_hide_3d.clicked.connect(lambda: )# TODO Connect button with image functionality
    ui.ui_rad.page_rad_diagnose_button_add_annotation.clicked.connect(lambda: add_annotation(app, ui))
    ui.ui_rad.page_rad_diagnose_button_add_impression.clicked.connect(lambda: add_impression(app, ui))


def report_page_setup(app, ui):
    ui.ui_rad.page_rad_report_report_preview = Report(ui.ui_rad.page_rad_report_report_preview_frame)
    ui.ui_rad.page_rad_report_report_preview_frame_grid.addWidget(ui.ui_rad.page_rad_report_report_preview, 0, 0, 1, 1)

    ui.ui_rad.page_rad_report_button_back.clicked.connect(lambda: change_page(ui, ui.ui_rad.page_rad_diagnose, False))
    ui.ui_rad.page_rad_report_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_report_button_send_report.clicked.connect(lambda: show_send_report_popup(app, ui))
    # ui.ui_rad.page_rad_report_button_surgeon_view.clicked.connect(lambda: )# TODO connect to surgeon view
    # ui.ui_rad.page_rad_report_button_fullscreen.clicked.connect(lambda:)# TODO fullscreen
    # ui.ui_rad.page_rad_report_button_zoom_in.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_report_button_zoom_out.clicked.connect(lambda: )# TODO Connect button with image functionality


def locked_page_setup(ui):
    ui.ui_rad.page_rad_locked_button_login.clicked.connect(lambda: login(ui))


# GO TO FUNCTIONS #


def go_back_from_diagnose_page(app, ui):
    print("WARNING! ALL CHANGES WILL BE DISCARDED") # TODO Popup or something
    annotations = app.pat_dict[app.current_pat_id].errands[app.current_errand_id].annotations
    for annot in annotations:
        if not annot.reviewed:
            annotations.remove(annot)

    if ui.prev_page is ui.ui_rad.page_rad_view_only:
        go_to_view_only_page(app, ui)
    elif ui.prev_page is ui.ui_rad.page_rad_patient_page:
        go_to_patient_page(app, ui)
    else:
        change_page(ui, ui.prev_page)


def go_to_patient_page(app, ui):
    for pat in app.pat_dict.values():
        for errand in pat.errands.values():
            for annot in errand.annotations:
                if not annot.reviewed:
                    print("Annotation not reviewed")
            for impr in errand.impressions:
                if not impr.reviewed:
                    print("Impression not reviewed")
    app.current_pat_id = ui.ui_rad.page_rad_home_patient_information.currentItem().text(0)
    app.current_errand_id = ui.ui_rad.page_rad_home_patient_information.currentItem().text(5)

    ui.ui_rad.page_rad_patient_page_button_diagnose_patient.setEnabled(not is_patient_diagnosed(app))

    # ui.ui_rad.page_rad_patient_page_patient_info # TODO add patient information
    # ui.ui_rad.page_rad_patient_page_doctors_orders  # TODO add doctors orders information
    # ui.ui_rad.page_rad_patient_page_scan_info  # TODO add scan information

    change_page(ui, ui.ui_rad.page_rad_patient_page)


def go_to_view_only_page(app, ui):
    ui.ui_rad.page_rad_view_only_2d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_view_only_2d_view_frame)
    ui.ui_rad.page_rad_view_only_2d_view_frame_grid.addWidget(ui.ui_rad.page_rad_view_only_2d_view, 0, 0, 1, 1)

    ui.ui_rad.page_rad_view_only_3d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_view_only_3d_view_frame)
    ui.ui_rad.page_rad_view_only_3d_view_frame_grid.addWidget(ui.ui_rad.page_rad_view_only_3d_view, 0, 0, 1, 1)

    app.visEngine.SetDirectory(app.pat_dict[app.current_pat_id].errands[app.current_errand_id].data_dir)
    app.visEngine.SetupImageUI(ui.ui_rad.page_rad_view_only_2d_view)
    app.visEngine.SetupVolumeUI(ui.ui_rad.page_rad_view_only_3d_view)

    ui.ui_rad.page_rad_view_only_button_diagnose.setEnabled(not is_patient_diagnosed(app))

    # ui.ui_rad.page_rad_view_only_radiology_report # TODO add radiology report here (if available)

    change_page(ui, ui.ui_rad.page_rad_view_only)


def go_to_diagnose_page(app, ui):
    ui.ui_rad.page_rad_diagnose_2d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_diagnose_2d_view_frame)
    ui.ui_rad.page_rad_diagnose_2d_view_frame_grid.addWidget(ui.ui_rad.page_rad_diagnose_2d_view, 0, 0, 1, 1)

    ui.ui_rad.page_rad_diagnose_3d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_diagnose_3d_view_frame)
    ui.ui_rad.page_rad_diagnose_3d_view_frame_grid.addWidget(ui.ui_rad.page_rad_diagnose_3d_view, 0, 0, 1, 1)

    app.visEngine.SetDirectory(app.pat_dict[app.current_pat_id].errands[app.current_errand_id].data_dir)
    app.visEngine.SetupImageUI(ui.ui_rad.page_rad_diagnose_2d_view)
    app.visEngine.SetupVolumeUI(ui.ui_rad.page_rad_diagnose_3d_view)

    ui.ui_rad.page_rad_diagnose_insert_impression.setPlainText("")
    ui.ui_rad.page_rad_diagnose_insert_locations.setPlainText("")
    ui.ui_rad.page_rad_diagnose_insert_findings.setPlainText("")
    ui.ui_rad.page_rad_diagnose_tab.setCurrentIndex(0)

    change_page(ui, ui.ui_rad.page_rad_diagnose)


def go_to_report_page(app, ui):
    ui.ui_rad.page_rad_report_2d_image = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_report_2d_image_frame)
    ui.ui_rad.page_rad_report_2d_image_frame_grid.addWidget(ui.ui_rad.page_rad_report_2d_image, 0, 0, 1, 1)

    app.visEngine.SetDirectory(app.pat_dict[app.current_pat_id].errands[app.current_errand_id].data_dir)
    app.visEngine.SetupImageUI(ui.ui_rad.page_rad_report_2d_image)

    ui.ui_rad.page_rad_report_report_preview.load_report(template_name="radiologist",
                                                             patient=app.pat_dict[app.current_pat_id],
                                                             order_id=app.current_errand_id,
                                                             vtk_widget_2d=ui.ui_rad.page_rad_report_2d_image,
                                                             vtk_widget_3d=None)

    change_page(ui, ui.ui_rad.page_rad_report, False)


# HELP FUNCTIONS #
def add_impression(app, ui):
    if ui.ui_rad.page_rad_diagnose_insert_impression.toPlainText() != "":
        app.pat_dict[app.current_pat_id].errands[app.current_errand_id].add_impression(app.rad_dict[app.current_rad_id].get_signature(),
                                                                                       ui.ui_rad.page_rad_diagnose_insert_impression.toPlainText()) # TODO Add doctor title
        ui.ui_rad.page_rad_diagnose_insert_impression.setPlainText("")
        ui.ui_rad.page_rad_diagnose_button_preview_report.setFocus()
    else:
        print("No impression inserted")


def add_annotation(app, ui):
    annotation = app.visEngine.annotationStore
    if annotation is not None:
        if ui.ui_rad.page_rad_diagnose_insert_locations.toPlainText() != "":
            if ui.ui_rad.page_rad_diagnose_insert_findings.toPlainText() != "":
                annotation.SetLocation(ui.ui_rad.page_rad_diagnose_insert_locations.toPlainText())
                annotation.SetFinding(ui.ui_rad.page_rad_diagnose_insert_findings.toPlainText())
                app.pat_dict[app.current_pat_id].errands[app.current_errand_id].add_annotation(annotation)

                app.visEngine.annotationStore = None
                ui.ui_rad.page_rad_diagnose_insert_locations.setPlainText("")
                ui.ui_rad.page_rad_diagnose_insert_findings.setPlainText("")
                ui.ui_rad.page_rad_diagnose_insert_locations.setFocus()
            else:
                print("No findings inserted")
        else:
            print("No location inserted")
    else:
        print("No Segmentation available")


def change_link(app, ui, button, master_widget, slave_widget):
    deactivate_str = "Deactivate\n2D-3D Link"
    activate_str = "Activate\n2D-3D Link"
    if button.text() == deactivate_str:
        app.visEngine.UnlinkWindows(master_widget)
        button.setText(activate_str)
    elif button.text() == activate_str:
        app.visEngine.LinkWindows(master_widget, slave_widget)
        button.setText(deactivate_str)


def is_patient_diagnosed(app):
    return app.pat_dict[app.current_pat_id].errands[app.current_errand_id].status == "Complete"


def add_errands(app, ui):
    ui.ui_rad.page_rad_home_patient_information.clear()
    for pat in app.pat_dict.values():
        for errand in pat.errands.values():
            root_item = QTreeWidgetItem([pat.id, pat.sex, errand.date, errand.scan, errand.status, errand.order_id])
            ui.ui_rad.page_rad_home_patient_information.addTopLevelItem(root_item)
    ui.ui_rad.page_rad_home_patient_information.sortItems(2, Qt.DescendingOrder)


def change_page(ui, new_page, change_prev_page=True):
    if change_prev_page:
        ui.prev_page = ui.stacked_rad.currentWidget()
    ui.stacked_rad.setCurrentWidget(new_page)


def logout(app, ui):
    for pat in app.pat_dict.values():
        for errand in pat.errands.values():
            for annot in errand.annotations:
                if not annot.reviewed:
                    errand.annotations.remove(annot)
            for impr in errand.impressions:
                if not impr.reviewed:
                    errand.impressions.remove(impr)

    ui.prev_page = None
    ui.current_rad_id = None
    ui.stacked_rad.setCurrentWidget(ui.ui_rad.page_rad_home)
    ui.stacked_main.setCurrentWidget(ui.page_login)


def show_logout_popup(app, ui):
    msg = QMessageBox()
    msg.setWindowTitle("Logout")
    msg.setText("Are you sure you want to logout?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes|msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    for pat in app.pat_dict.values():
        for errand in pat.errands.values():
            for annot in errand.annotations:
                if not annot.reviewed:
                    msg.setText("Are you sure you want to logout?\nAll changes will be discarded")
                    break
            for impr in errand.impressions:
                if not impr.reviewed:
                    msg.setText("Are you sure you want to logout?\nAll changes will be discarded")
                    break

    ret = msg.exec_()
    if ret == msg.Yes:
        logout(app, ui)


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


def show_send_report_popup(app, ui):
    msg = QMessageBox()
    msg.setWindowTitle("Send Report")
    msg.setText("Are you sure you want to send the report?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes | msg.No)
    msg.setDefaultButton(msg.Yes)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
        for annot in errand.annotations:
            annot.reviewed = True
        for impr in errand.impressions:
            impr.reviewed = True
        errand.status = "Complete"

        app.current_pat_id = None
        app.current_errand_id = None
        add_errands(app, ui)  # Update errands list
        change_page(ui, ui.ui_rad.page_rad_home)


def select_item(ui):
    ui.ui_rad.page_rad_home_button_proceed.setEnabled(True)


def login(ui):
    password = ui.ui_rad.page_rad_locked_insert_password.text()
    ui.ui_rad.page_rad_locked_insert_password.clear()
    if password in ["rad", "", "0000"]:
        ui.ui_rad.page_rad_incorrect_password.clear()
        change_page(ui, ui.prev_page, False)
    else:
        ui.ui_rad.page_rad_incorrect_password.setText("Incorrect password!")


def lock_screen(ui):
    change_page(ui, ui.ui_rad.page_rad_locked)


