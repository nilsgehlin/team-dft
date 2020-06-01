from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import Qt
from reportGeneration.Report import Report
from PyQt5.QtGui import QPixmap, QIcon
import os

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
    ui.ui_rad.page_rad_view_only_radiology_report = Report(ui.ui_rad.page_rad_view_only_radiology_report_frame)
    ui.ui_rad.page_rad_view_only_radiology_report_frame_grid.addWidget(ui.ui_rad.page_rad_view_only_radiology_report, 2, 0, 1, 1)

    ui.ui_rad.page_rad_view_only_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_view_only_button_back.clicked.connect(lambda: go_back_from_view_only_page(app, ui))
    ui.ui_rad.page_rad_view_only_button_diagnose.clicked.connect(lambda: go_to_diagnose_page(app, ui))
    ui.ui_rad.page_rad_view_only_button_link_windows.clicked.connect(lambda: change_link(app, ui, ui.ui_rad.page_rad_view_only_button_link_windows,
                                                                                              ui.ui_rad.page_rad_view_only_2d_view, ui.ui_rad.page_rad_view_only_3d_view))
    # ui.ui_rad.page_rad_view_only_button_2d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_3d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_view_only_button_hide_3d.clicked.connect(lambda: )# TODO Connect button with image functionality

    # Zooming buttons 2D
    ui.ui_rad.page_rad_view_only_button_2d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_rad.page_rad_view_only_2d_view))
    ui.ui_rad.page_rad_view_only_button_2d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_view_only_2d_view))

    ui.ui_rad.page_rad_view_only_button_2d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_rad.page_rad_view_only_2d_view))
    ui.ui_rad.page_rad_view_only_button_2d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_view_only_2d_view))

    # Zooming buttons 3D
    ui.ui_rad.page_rad_view_only_button_3d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_rad.page_rad_view_only_3d_view))
    ui.ui_rad.page_rad_view_only_button_3d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_view_only_3d_view))

    ui.ui_rad.page_rad_view_only_button_3d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_rad.page_rad_view_only_3d_view))
    ui.ui_rad.page_rad_view_only_button_3d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_view_only_3d_view))


def diagnose_page_setup(app, ui):
    ui.ui_rad.page_rad_diagnose_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_rad.page_rad_diagnose_button_back.clicked.connect(lambda: go_back_from_diagnose_page(app, ui))
    ui.ui_rad.page_rad_diagnose_button_preview_report.clicked.connect(lambda: go_to_report_page(app, ui))
    ui.ui_rad.page_rad_diagnose_button_link_windows.clicked.connect(
        lambda: change_link(app, ui, ui.ui_rad.page_rad_diagnose_button_link_windows,
                            ui.ui_rad.page_rad_diagnose_2d_view, ui.ui_rad.page_rad_diagnose_3d_view))
    # ui.ui_rad.page_rad_diagnose_button_2d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_3d_fullscreen.clicked.connect(lambda: )# TODO Connect button with image functionality
    # ui.ui_rad.page_rad_diagnose_button_hide_3d.clicked.connect(lambda: )# TODO Connect button with image functionality
    ui.ui_rad.page_rad_diagnose_button_add_annotation.clicked.connect(lambda: add_annotation(app, ui))
    ui.ui_rad.page_rad_diagnose_button_add_impression.clicked.connect(lambda: add_impression(app, ui))

    # Windows full vs split
    ui.ui_sur.page_sur_view_edit_button_2d_fullscreen.clicked.connect(
        lambda: toggle2DSplit(app, ui, ui.ui_sur.page_sur_view_edit_button_2d_fullscreen))
    ui.ui_sur.page_sur_view_edit_button_3d_fullscreen.clicked.connect(
        lambda: toggle3DSplit(app, ui, ui.ui_sur.page_sur_view_edit_button_3d_fullscreen))

    # 2D image color
    ui.ui_rad.page_rad_diagnose_2d_slider_color_window.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_rad.page_rad_diagnose_2d_view))
    ui.ui_rad.page_rad_diagnose_2d_slider_color_level.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_rad.page_rad_diagnose_2d_view))

    # Advanced options
    ui.ui_rad.page_rad_diagnose_radio_group_orientation.buttonClicked.connect(
        lambda: change_slice_orientation(app, ui, ui.ui_rad.page_rad_diagnose_radio_group_orientation,
                                         ui.ui_rad.page_rad_diagnose_2d_view))
    ui.ui_rad.page_rad_diagnose_check_group_tissue.buttonClicked.connect(
        lambda: change_volume_tissue(app, ui, ui.ui_rad.page_rad_diagnose_check_group_tissue,
                                     ui.ui_rad.page_rad_diagnose_3d_view))
    ui.ui_rad.page_rad_diagnose_check_group_link.buttonClicked.connect(
        lambda: change_link_configuration(app, ui, ui.ui_rad.page_rad_diagnose_check_group_link))
    ui.ui_rad.page_rad_diagnose_slider_transparency_volume.valueChanged.connect(
        lambda: change_volume_transparency(app, ui, ui.ui_rad.page_rad_diagnose_slider_transparency_volume,
                                           ui.ui_rad.page_rad_diagnose_3d_view))
    ui.ui_rad.page_rad_diagnose_slider_transparency_segmentation.valueChanged.connect(
        lambda: change_segmentation_transparency(app, ui, ui.ui_rad.page_rad_diagnose_slider_transparency_segmentation,
                                                 ui.ui_rad.page_rad_diagnose_3d_view))
    ui.ui_rad.page_rad_diagnose_slider_transparency_active.valueChanged.connect(
        lambda: change_segment_transparency(app, ui, ui.ui_rad.page_rad_diagnose_slider_transparency_active,
                                            ui.ui_rad.page_rad_diagnose_3d_view))

    # Zooming buttons 2D
    ui.ui_rad.page_rad_diagnose_button_2d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_rad.page_rad_diagnose_2d_view))
    ui.ui_rad.page_rad_diagnose_button_2d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_diagnose_2d_view))

    ui.ui_rad.page_rad_diagnose_button_2d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_rad.page_rad_diagnose_2d_view))
    ui.ui_rad.page_rad_diagnose_button_2d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_diagnose_2d_view))

    # Zooming buttons 3D
    ui.ui_rad.page_rad_diagnose_button_3d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_rad.page_rad_diagnose_3d_view))
    ui.ui_rad.page_rad_diagnose_button_3d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_diagnose_3d_view))

    ui.ui_rad.page_rad_diagnose_button_3d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_rad.page_rad_diagnose_3d_view))
    ui.ui_rad.page_rad_diagnose_button_3d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_rad.page_rad_diagnose_3d_view))


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

def go_back_from_view_only_page(app, ui):
    unlink_views(app, ui)
    change_page(ui, ui.ui_rad.page_rad_patient_page)


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
    app.current_errand_id = ui.ui_rad.page_rad_home_patient_information.currentItem().text(7)

    ui.ui_rad.page_rad_patient_page_button_diagnose_patient.setEnabled(not is_patient_diagnosed(app))

    # ui.ui_rad.page_rad_patient_page_patient_info # TODO add patient information
    # ui.ui_rad.page_rad_patient_page_doctors_orders  # TODO add doctors orders information
    # ui.ui_rad.page_rad_patient_page_scan_info  # TODO add scan information

    change_page(ui, ui.ui_rad.page_rad_patient_page)
    unlink_views(app, ui)


def go_to_view_only_page(app, ui):
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]

    if app.visEngine.GetDirectory() is not errand.data_dir or not isinstance(ui.ui_rad.page_rad_view_only_2d_view, QVTKRenderWindowInteractor):
        ui.ui_rad.page_rad_view_only_2d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_view_only_2d_view_frame)
        ui.ui_rad.page_rad_view_only_2d_view_frame_grid.addWidget(ui.ui_rad.page_rad_view_only_2d_view, 0, 0, 4, 1)

        ui.ui_rad.page_rad_view_only_3d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_view_only_3d_view_frame)
        ui.ui_rad.page_rad_view_only_3d_view_frame_grid.addWidget(ui.ui_rad.page_rad_view_only_3d_view, 0, 0, 4, 1)

        app.visEngine.SetDirectory(app.pat_dict[app.current_pat_id].errands[app.current_errand_id].data_dir)
        app.visEngine.SetupImageUI(ui.ui_rad.page_rad_view_only_2d_view)
        app.visEngine.SetupVolumeUI(ui.ui_rad.page_rad_view_only_3d_view)

        if errand.status.lower() == "complete":
            ui.ui_rad.page_rad_view_only_radiology_report.load_report(template_name="radiologist",
                                                             patient=app.pat_dict[app.current_pat_id],
                                                             order_id=app.current_errand_id,
                                                                      vtk_widget_2d=ui.ui_rad.page_rad_view_only_2d_view,
                                                                      vtk_widget_3d=ui.ui_rad.page_rad_view_only_3d_view,
                                                                      vis_engine=app.visEngine)
        else:
            ui.ui_rad.page_rad_view_only_radiology_report.setText("No radiology report available for this scan")

    ui.ui_rad.page_rad_view_only_button_diagnose.setEnabled(not is_patient_diagnosed(app))
    change_page(ui, ui.ui_rad.page_rad_view_only)
    unlink_views(app, ui)


def go_to_diagnose_page(app, ui):

    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    if app.visEngine.GetDirectory() is not errand.data_dir or not isinstance(ui.ui_rad.page_rad_diagnose_2d_view,
                                                                             QVTKRenderWindowInteractor):
        ui.ui_rad.page_rad_diagnose_2d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_diagnose_2d_view_frame)
        ui.ui_rad.page_rad_diagnose_2d_view_frame_grid.addWidget(ui.ui_rad.page_rad_diagnose_2d_view, 0, 0, 4, 3)

        ui.ui_rad.page_rad_diagnose_3d_view = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_diagnose_3d_view_frame)
        ui.ui_rad.page_rad_diagnose_3d_view_frame_grid.addWidget(ui.ui_rad.page_rad_diagnose_3d_view, 0, 1, 4, 1)

        app.visEngine.SetDirectory(app.pat_dict[app.current_pat_id].errands[app.current_errand_id].data_dir)
        app.visEngine.SetupImageUI(ui.ui_rad.page_rad_diagnose_2d_view)
        app.visEngine.SetupVolumeUI(ui.ui_rad.page_rad_diagnose_3d_view)

    ui.ui_rad.page_rad_diagnose_insert_impression.setPlainText("")
    ui.ui_rad.page_rad_diagnose_insert_locations.setPlainText("")
    ui.ui_rad.page_rad_diagnose_insert_findings.setPlainText("")
    ui.ui_rad.page_rad_diagnose_tab.setCurrentIndex(0)

    change_page(ui, ui.ui_rad.page_rad_diagnose)
    unlink_views(app, ui)


def go_to_report_page(app, ui):
    ui.ui_rad.page_rad_report_2d_image = QVTKRenderWindowInteractor(ui.ui_rad.page_rad_report_2d_image_frame)
    ui.ui_rad.page_rad_report_2d_image_frame_grid.addWidget(ui.ui_rad.page_rad_report_2d_image, 0, 0, 1, 1)

    app.visEngine.SetDirectory(app.pat_dict[app.current_pat_id].errands[app.current_errand_id].data_dir)
    app.visEngine.SetupImageUI(ui.ui_rad.page_rad_report_2d_image)

    ui.ui_rad.page_rad_report_report_preview.load_report(template_name="radiologist",
                                                             patient=app.pat_dict[app.current_pat_id],
                                                             order_id=app.current_errand_id,
                                                             vtk_widget_2d=ui.ui_rad.page_rad_report_2d_image,
                                                             vtk_widget_3d=None, vis_engine=app.visEngine)

    change_page(ui, ui.ui_rad.page_rad_report, False)


# HELP FUNCTIONS #

def unlink_views(app, ui):
    if isinstance(ui.ui_rad.page_rad_view_only_2d_view, QVTKRenderWindowInteractor):
        if app.visEngine.LinkedAsMaster(ui.ui_rad.page_rad_view_only_2d_view):
            print("view linked as")
            change_link(app, ui, ui.ui_rad.page_rad_view_only_button_link_windows,
                        ui.ui_rad.page_rad_view_only_2d_view, force="Deactivate\n2D-3D Link")
    if isinstance(ui.ui_rad.page_rad_diagnose_2d_view, QVTKRenderWindowInteractor):
        if app.visEngine.LinkedAsMaster(ui.ui_rad.page_rad_diagnose_2d_view):
            print("diag linked as")
            change_link(app, ui, ui.ui_rad.page_rad_diagnose_button_link_windows,
                        ui.ui_rad.page_rad_diagnose_2d_view, force="Deactivate\n2D-3D Link")

def add_impression(app, ui):
    if ui.ui_rad.page_rad_diagnose_insert_impression.toPlainText() != "":
        app.pat_dict[app.current_pat_id].errands[app.current_errand_id].add_impression(app.rad_dict[app.current_rad_id].get_signature(),
                                                                                       ui.ui_rad.page_rad_diagnose_insert_impression.toPlainText()) # TODO Add doctor title
        ui.ui_rad.page_rad_diagnose_insert_impression.setPlainText("")
        ui.ui_rad.page_rad_diagnose_button_preview_report.setFocus()
    else:
        print("No impression inserted")


def add_annotation(app, ui):
    annotation = app.visEngine.GetActiveAnnotation()
    if annotation is not None:
        if ui.ui_rad.page_rad_diagnose_insert_locations.toPlainText() != "":
            if ui.ui_rad.page_rad_diagnose_insert_findings.toPlainText() != "":
                annotation.SetLocation(ui.ui_rad.page_rad_diagnose_insert_locations.toPlainText())
                annotation.SetFinding(ui.ui_rad.page_rad_diagnose_insert_findings.toPlainText())
                app.pat_dict[app.current_pat_id].errands[app.current_errand_id].add_annotation(annotation)

                app.visEngine.ClearActiveAnnotation()
                ui.ui_rad.page_rad_diagnose_insert_locations.setPlainText("")
                ui.ui_rad.page_rad_diagnose_insert_findings.setPlainText("")
                ui.ui_rad.page_rad_diagnose_insert_locations.setFocus()
            else:
                print("No findings inserted")
        else:
            print("No location inserted")
    else:
        print("No Segmentation available")


def change_link(app, ui, button, master_widget, slave_widget=None, force=None):
    deactivate_str = "Deactivate\n2D-3D Link"
    activate_str = "Activate\n2D-3D Link"
    if force is not None:
        button.setText(force)
    if button.text() == deactivate_str:
        app.visEngine.UnlinkWindows(master_widget)
        button.setText(activate_str)
        button.setIcon(QIcon(os.path.join("UI", "icons", "unlink.png")))
    elif button.text() == activate_str:
        app.visEngine.LinkWindows(master_widget, [slave_widget])
        button.setText(deactivate_str)
        button.setIcon(QIcon(os.path.join("UI", "icons", "link.png")))


def is_patient_diagnosed(app):
    return app.pat_dict[app.current_pat_id].errands[app.current_errand_id].status == "Complete"


def add_errands(app, ui):
    ui.ui_rad.page_rad_home_patient_information.clear()
    for pat in app.pat_dict.values():
        for errand in pat.errands.values():
            root_item = QTreeWidgetItem([pat.id, pat.first_name, pat.last_name, pat.sex, errand.date, errand.scan, errand.status, errand.order_id])
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

    unlink_views(app, ui)

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


# Changes the 2D window slice orientation to AXIAL, SAGITALL or CORONAL
def change_slice_orientation(app, ui, group, widget):
    ui.status_bar.showMessage("Changing slice orientation, please wait...")
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    current_annots = []
    current_measurs =  []
    # Save the current annotations
    for annot in errand.annotations:
        if app.visEngine.HasSegmentation(widget, annot): 
            current_annots += [annot]
        if app.visEngine.HasMeasurement(widget,annot): 
            current_measurs += [annot]
    # Clear link if window is actively a master link
    slaves = None
    if app.visEngine.LinkedAsMaster(widget):
        slaves = app.visEngine.GetLinkSlaves()
        app.visEngine.UnlinkWindows(widget)
    # Recreate windows with new orientation
    app.visEngine.SetupImageUI(widget, group.checkedButton().text())
    app.visEngine.AddSegmentations(widget, current_annots)
    app.visEngine.AddMeasurements(widget, current_measurs)
    # Recreate slaves
    if slaves is not None:
        app.visEngine.LinkWindows(widget, slaves)
    ui.status_bar.clearMessage()


# Changes the active tissue in a 3D volume
def change_volume_tissue(app, ui, group, widget):
    if group.checkedButton() is None:
        app.visEngine.SetTissue(widget, [])
    elif group.checkedButton().text() == "ALL":
        for button in group.buttons():
            if button.text() != "ALL": button.setChecked(False)
        app.visEngine.SetTissue(widget, ["ALL"])
    else:
        ui.ui_rad.checkBox_All.setChecked(False)
        tissues = []
        for button in group.buttons():
            if button.isChecked():
                tissues += [button.text()]
        app.visEngine.SetTissue(widget, tissues)


def change_volume_transparency(app, ui, slider, widget):
    val = slider.value()
    val = round(val/100, 2)
    app.visEngine.SetTransparency(widget, val)


def change_segmentation_transparency(app, ui, slider, widget):
    val = slider.value()
    val = round(val/100, 2)
    app.visEngine.SetAllSegmentationTransparency(widget, val)


def change_segment_transparency(app, ui, slider, widget):
    val = slider.value()
    val = round(val/100, 2)
    annot = app.visEngine.GetActiveAnnotation()
    if annot is not None:
        app.visEngine.SetSegmentationTransparency(widget, [annot], val)

# Change how linked slice appears on the 3D window
def change_link_configuration(app, ui, group):
    show_slice = group.buttons()[0].isChecked()
    crop_3d = not group.buttons()[1].isChecked()
    app.visEngine.ConfigureVolumeCuttingPlane(showSlice=show_slice, crop3D=crop_3d)


# Changes the 2D image 'greyscale'
def change_image_color(app, ui, widget):
    color_window = ui.ui_rad.page_rad_diagnose_2d_slider_color_window.value()
    color_level = ui.ui_rad.page_rad_diagnose_2d_slider_color_level.value()
    app.visEngine.SetImageColor(widget, color_window, color_level)


# Focus the windows on the next annotation on the report
def go_to_next_annot(app, ui, widget_2d, widget_3d):
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    annots = errand.annotations
    if not annots: return
    active_annot = app.visEngine.GetActiveAnnotation()
    if active_annot is None:
        next_annot_idx = 0
    else:
        next_annot_idx = annots.index(active_annot) + 1
        if len(annots) == next_annot_idx: next_annot_idx = 0
    next_annot = annots[next_annot_idx]
    if widget_2d is not None:
        app.visEngine.RemoveAllAnnotations(widget_2d)
        app.visEngine.AddSegmentations(widget_2d, [next_annot])
        app.visEngine.AddMeasurements(widget_2d, [next_annot])
        app.visEngine.GoToAnnotation(widget_2d, next_annot)
    if widget_3d is not None:
        app.visEngine.RemoveAllAnnotations(widget_3d)
        app.visEngine.AddSegmentations(widget_3d, [next_annot])
        app.visEngine.GoToAnnotation(widget_3d, next_annot)
    measurement = app.visEngine.GetSliceMeasurement(widget_2d, next_annot)
    ui.status_bar.showMessage("Active finding: " + next_annot.GetLocation() + ", volume: " + str(measurement) + " mm3")


# Focus the windows on the previous annotation on the report
def go_to_previous_annot(app, ui, widget_2d, widget_3d):
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    annots = errand.annotations
    if not annots: return
    active_annot = app.visEngine.GetActiveAnnotation()
    if active_annot is None:
        prev_annot_idx = len(annots) - 1
    else:
        prev_annot_idx = annots.index(active_annot) - 1
        if prev_annot_idx < 0: prev_annot_idx = len(annots) - 1
    next_annot = annots[prev_annot_idx]
    if widget_2d is not None:
        app.visEngine.RemoveAllAnnotations(widget_2d)
        app.visEngine.AddSegmentations(widget_2d, [next_annot])
        app.visEngine.AddMeasurements(widget_2d, [next_annot])
        app.visEngine.GoToAnnotation(widget_2d, next_annot)
    if widget_3d is not None:
        app.visEngine.RemoveAllAnnotations(widget_3d)
        app.visEngine.AddSegmentations(widget_3d, [next_annot])
        app.visEngine.GoToAnnotation(widget_3d, next_annot)
    measurement = app.visEngine.GetSliceMeasurement(widget_2d, next_annot)
    ui.status_bar.showMessage("Active finding: " + next_annot.GetLocation() + ", volume: " + str(measurement) + " mm3")


# Offer zoom functionality to the widgets
def start_zoom_in(app, ui, widget):
    app.visEngine.StartZoomIn(widget)

def start_zoom_out(app, ui, widget):
    app.visEngine.StartZoomOut(widget)

def stop_zoom(app, ui, widget):
    app.visEngine.StopZoom(widget)


# Offer slice maneuvering functionality to 2D widgets
def change_image_slice(app, ui, widget, dir_):
    app.visEngine.StartSliceChange(widget, dir_)

def stop_image_slice(app, ui, widget):
    app.visEngine.StopSliceChange(widget)


# Animate the 2D window slices
def toggle_animation(app, ui, button, widget):
    pause_str = "Pause Slices"
    play_str = "Play Slices"
    if button.text() == pause_str:
        button.setText(play_str)
        button.setIcon(QIcon("UI\icons\\play.png"))
        button.setToolTip("Play slice animation ")
    elif button.text() == play_str:
        button.setText(pause_str)
        button.setIcon(QIcon("UI\icons\\pause.png"))
        button.setToolTip("Pause slice animation")
    app.visEngine.ToggleSliceAnnimation(widget)


# Toggle advanced setting on the app
def toggleSettings(app, ui, button):
    hide_str = "Hide Advanced Tools"
    show_str = "Show Advanced Tools"
    if button.text() == hide_str:
        button.setText(show_str)
        ui.ui_rad.page_rad_diagnose_tools.hide()
        button.setToolTip("Show advanced functionality for image manipulation")
    elif button.text() == show_str:
        button.setText(hide_str)
        ui.ui_rad.page_rad_diagnose_tools.show()
        button.setToolTip("Hide advanced functionality for image manipulation")


# Toggle 3D view spilt screen
def toggle3DSplit(app, ui, button):
    full_str = "3D Full Screen"
    half_str = "Split Screen"
    if button.text() == half_str:
        button.setText(full_str)
        button.setIcon(QIcon("UI\icons\\full_screen.png"))
        button.setToolTip("Expand 3D view")
        ui.ui_rad.page_rad_diagnose_2d_view_frame.show()
        ui.ui_rad.page_rad_diagnose_2d_slider_color_window.show()
        ui.ui_rad.page_rad_diagnose_2d_slider_color_level.show()
    elif button.text() == full_str:
        button.setText(half_str)
        button.setIcon(QIcon("UI\icons\\restore.png"))
        button.setToolTip("Return to split view")
        ui.ui_rad.page_rad_diagnose_2d_view_frame.hide()
        ui.ui_rad.page_rad_diagnose_2d_slider_color_window.hide()
        ui.ui_rad.page_rad_diagnose_2d_slider_color_level.hide()


# Toggle 2D view spilt screen
def toggle2DSplit(app, ui, button):
    full_str = "2D Full Screen"
    half_str = "Split Screen"
    if button.text() == half_str:
        button.setText(full_str)
        button.setIcon(QIcon("UI\icons\\full_screen.png"))
        button.setToolTip("Expand 2D view")
        ui.ui_rad.page_rad_diagnose_3d_view_frame.show()
    elif button.text() == full_str:
        button.setText(half_str)
        button.setIcon(QIcon("UI\icons\\restore.png"))
        button.setToolTip("Return to split view")
        ui.ui_rad.page_rad_diagnose_3d_view_frame.hide()


# Reset the camera on the views
def resetView(app, ui, widget):
    [w, l] = app.visEngine.ResetWidgetCamera(widget)
    if w: ui.ui_rad.page_rad_diagnose_2d_slider_color_window.setValue(w)
    if l: ui.ui_rad.page_rad_diagnose_2d_slider_color_level.setValue(l)

