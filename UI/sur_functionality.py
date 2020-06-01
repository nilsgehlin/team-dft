from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import Qt
from reportGeneration.Report import Report
from PyQt5.QtGui import QPixmap, QIcon
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
    ui.ui_sur.page_sur_home_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_sur.page_sur_home_button_colleagues.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_my_profile))
    ui.ui_sur.page_sur_home_button_proceed.clicked.connect(lambda: go_to_patient_errand_page(app, ui)) # TODO
    ui.ui_sur.page_sur_home_treatment_list.itemClicked.connect(lambda: ui.ui_sur.page_sur_home_button_proceed.setEnabled(True)) # TODO
    ui.ui_sur.page_sur_home_treatment_list.itemDoubleClicked.connect(
        lambda: go_to_patient_errand_page(app, ui)) # TODO


def patient_errand_page_setup(app, ui):
    ui.ui_sur.page_sur_patient_errand_progress_bar.hide()
    ui.ui_sur.page_sur_patient_errand_button_download.hide()

    ui.ui_sur.page_sur_patient_errand_report = Report(ui.ui_sur.page_sur_patient_errand_report_frame, show_segmentation_on_click=False)
    ui.ui_sur.page_sur_patient_errand_report_frame_grid.addWidget(ui.ui_sur.page_sur_patient_errand_report, 0, 0, 1, 1)

    ui.ui_sur.page_sur_patient_errand_button_back.clicked.connect(lambda: go_back_from_patient_errand_page(app, ui))
    ui.ui_sur.page_sur_patient_errand_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    # ui.ui_sur.page_sur_patient_errand_button_download.clicked.connect(lambda: pass) # TODO Not sure if we need this atm
    ui.ui_sur.page_sur_patient_errand_button_view.clicked.connect(lambda: go_to_view_edit_page(app, ui))
    ui.ui_sur.page_sur_patient_errand_errand_list.itemClicked.connect(
        lambda: change_report(app, ui.ui_sur.page_sur_patient_errand_errand_list, ui.ui_sur.page_sur_patient_errand_report))
    ui.ui_sur.page_sur_patient_errand_errand_list.itemDoubleClicked.connect(
        lambda: go_to_view_edit_page(app, ui))


def view_edit_page_setup(app, ui):
    ui.ui_sur.page_sur_view_edit_report = Report(ui.ui_sur.page_sur_view_edit_report_frame)
    ui.ui_sur.page_sur_view_edit_report_frame_grid.addWidget(ui.ui_sur.page_sur_view_edit_report, 0, 0, 1, 1)

    # ui.ui_sur.page_sur_view_edit_2d_view = None

    ui.ui_sur.page_sur_view_edit_button_back.clicked.connect(lambda: change_page(ui, ui.ui_sur.page_sur_patient_errand))
    ui.ui_sur.page_sur_view_edit_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    # ui.ui_sur.page_sur_view_edit_button_save_report.clicked.connect(lambda: ) # TODO Is this one needed here?

    ui.ui_sur.page_sur_view_edit_button_add_note.clicked.connect(lambda: add_note(app, ui))
    ui.ui_sur.page_sur_view_edit_button_add_impression.clicked.connect(lambda: add_impression(app, ui))

    # Annotation and image navigation buttons
    ui.ui_sur.page_sur_view_edit_button_2d_next_note.clicked.connect(
        lambda: go_to_next_annot(app, ui, ui.ui_sur.page_sur_view_edit_2d_view, ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_previous_note.clicked.connect(
        lambda: go_to_previous_annot(app, ui, ui.ui_sur.page_sur_view_edit_2d_view, ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_play_pause.clicked.connect(
        lambda: toggle_animation(app, ui, ui.ui_sur.page_sur_view_edit_button_2d_play_pause, ui.ui_sur.page_sur_view_edit_2d_view))

    # Image slice buttons
    ui.ui_sur.page_sur_view_edit_button_2d_next_slice.pressed.connect(
        lambda: change_image_slice(app, ui, ui.ui_sur.page_sur_view_edit_2d_view, 1))
    ui.ui_sur.page_sur_view_edit_button_2d_next_slice.released.connect(
        lambda: stop_image_slice(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_previous_slice.pressed.connect(
        lambda: change_image_slice(app, ui, ui.ui_sur.page_sur_view_edit_2d_view, -1))
    ui.ui_sur.page_sur_view_edit_button_2d_previous_slice.released.connect(
        lambda: stop_image_slice(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))

    # Windows
    ui.ui_sur.page_sur_view_edit_button_link_windows.clicked.connect(
        lambda: change_link(app, ui, ui.ui_sur.page_sur_view_edit_button_link_windows,
                            ui.ui_sur.page_sur_view_edit_2d_view, ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_fullscreen.clicked.connect(
        lambda: toggle2DSplit(app, ui, ui.ui_sur.page_sur_view_edit_button_2d_fullscreen));
    ui.ui_sur.page_sur_view_edit_button_3d_fullscreen.clicked.connect(
        lambda: toggle3DSplit(app, ui, ui.ui_sur.page_sur_view_edit_button_3d_fullscreen))
    # ui.ui_sur.page_sur_view_edit_button_2d_reset.clicked.connect(
    #     lambda: resetView(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    # ui.ui_sur.page_sur_view_edit_button_3d_reset.clicked.connect(
    #     lambda: resetView(app, ui, ui.ui_sur.page_sur_view_edit_3d_view))

    # Zooming buttons 2D
    ui.ui_sur.page_sur_view_edit_button_2d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_button_2d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))

    # Zooming buttons 3D
    ui.ui_sur.page_sur_view_edit_button_3d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_button_3d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_button_3d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_button_3d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_sur.page_sur_view_edit_3d_view))

    # 2D image color buttons
    ui.ui_sur.page_sur_view_edit_2d_slider_color_window.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_2d_slider_color_level.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_sur.page_sur_view_edit_2d_view))

    # Advanced options
    ui.ui_sur.page_sur_view_edit_tools.hide()
    ui.ui_sur.page_sur_view_edit_button_tools.clicked.connect(
        lambda: toggleSettings(app, ui, ui.ui_sur.page_sur_view_edit_button_tools))
    ui.ui_sur.page_sur_view_edit_radio_group_orientation.buttonClicked.connect(
        lambda: change_slice_orientation(app, ui, ui.ui_sur.page_sur_view_edit_radio_group_orientation,
                                         ui.ui_sur.page_sur_view_edit_2d_view))
    ui.ui_sur.page_sur_view_edit_check_group_tissue.buttonClicked.connect(
        lambda: change_volume_tissue(app, ui, ui.ui_sur.page_sur_view_edit_check_group_tissue,
                                     ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_check_group_link.buttonClicked.connect(
        lambda: change_link_configuration(app, ui, ui.ui_sur.page_sur_view_edit_check_group_link))
    ui.ui_sur.page_sur_view_edit_slider_transparency_volume.valueChanged.connect(
        lambda: change_volume_transparency(app, ui, ui.ui_sur.page_sur_view_edit_slider_transparency_volume,
                                           ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_slider_transparency_segmentation.valueChanged.connect(
        lambda: change_segmentation_transparency(app, ui, ui.ui_sur.page_sur_view_edit_slider_transparency_segmentation,
                                                 ui.ui_sur.page_sur_view_edit_3d_view))
    ui.ui_sur.page_sur_view_edit_slider_transparency_active.valueChanged.connect(
        lambda: change_segment_transparency(app, ui, ui.ui_sur.page_sur_view_edit_slider_transparency_active,
                                            ui.ui_sur.page_sur_view_edit_3d_view))


## GO TO FUNCTIONS ##
def go_back_from_patient_errand_page(app, ui):
    change_page(ui, ui.ui_sur.page_sur_home)
    unlink_views(app, ui)

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
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    if app.visEngine.GetDirectory() is not errand.data_dir or not isinstance(ui.ui_sur.page_sur_view_edit_2d_view,
                                                                             QVTKRenderWindowInteractor):
        ui.status_bar.showMessage("Loading report, please wait...")
        ui.ui_sur.page_sur_patient_errand_progress_bar.show()

        # Setup UI
        ui.ui_sur.page_sur_patient_errand_progress_bar.setValue(5)
        ui.ui_sur.page_sur_view_edit_2d_view = QVTKRenderWindowInteractor(ui.ui_sur.page_sur_view_edit_2d_view_frame)
        ui.ui_sur.page_sur_view_edit_2d_view_frame_grid.addWidget(ui.ui_sur.page_sur_view_edit_2d_view, 1, 0, 1, 4)

        ui.ui_sur.page_sur_view_edit_3d_view = QVTKRenderWindowInteractor(ui.ui_sur.page_sur_view_edit_3d_view_frame)
        ui.ui_sur.page_sur_view_edit_3d_view_frame_grid.addWidget(ui.ui_sur.page_sur_view_edit_3d_view, 1, 0, 1, 4)

        app.current_errand_id = ui.ui_sur.page_sur_patient_errand_errand_list.currentItem().text(0)


    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    app.visEngine.SetDirectory(errand.data_dir)
    app.visEngine.SetupImageUI(ui.ui_sur.page_sur_view_edit_2d_view)
    app.visEngine.SetupVolumeUI(ui.ui_sur.page_sur_view_edit_3d_view)

    # Load all annotations to the viewers and then remove them, for optimization on click
    app.visEngine.AddSegmentations(ui.ui_sur.page_sur_view_edit_2d_view, errand.annotations)
    ui.ui_sur.page_sur_patient_errand_progress_bar.setValue(25)
    app.visEngine.AddMeasurements(ui.ui_sur.page_sur_view_edit_2d_view, errand.annotations)
    ui.ui_sur.page_sur_patient_errand_progress_bar.setValue(50)
    app.visEngine.AddSegmentations(ui.ui_sur.page_sur_view_edit_3d_view, errand.annotations)
    ui.ui_sur.page_sur_patient_errand_progress_bar.setValue(75)
    app.visEngine.RemoveAllAnnotations(ui.ui_sur.page_sur_view_edit_2d_view)
    app.visEngine.RemoveAllAnnotations(ui.ui_sur.page_sur_view_edit_3d_view)
    ui.ui_sur.page_sur_patient_errand_progress_bar.setValue(90)

    # Reset the views
    resetView(app, ui, ui.ui_sur.page_sur_view_edit_2d_view)
    resetView(app, ui, ui.ui_sur.page_sur_view_edit_3d_view)


    if errand.status.lower() == "complete":
        ui.ui_sur.page_sur_view_edit_report.load_report(template_name="radiologist",
                                                        patient=app.pat_dict[app.current_pat_id],
                                                        order_id=app.current_errand_id,
                                                        vtk_widget_2d=ui.ui_sur.page_sur_view_edit_2d_view,
                                                        vtk_widget_3d=ui.ui_sur.page_sur_view_edit_3d_view,
                                                        vis_engine=app.visEngine,
                                                        status_bar= ui.status_bar)
    else:
        ui.ui_sur.page_sur_view_edit_report.setText("No Radiology Report Available")

    ui.ui_sur.page_sur_patient_errand_progress_bar.setValue(100)
    ui.ui_sur.page_sur_patient_errand_progress_bar.hide()
    change_page(ui, ui.ui_sur.page_sur_view_edit)


# HELP FUNCTIONS #
def add_impression(app, ui):
    if ui.ui_sur.page_sur_view_edit_insert_impression.toPlainText() != "":
        app.pat_dict[app.current_pat_id].errands[app.current_errand_id].add_impression(app.sur_dict[app.current_sur_id].get_signature(),
                                                                                       ui.ui_sur.page_sur_view_edit_insert_impression.toPlainText()) # TODO Add doctor title
        ui.ui_sur.page_sur_view_edit_insert_impression.setPlainText("")
        ui.ui_sur.page_sur_view_edit_report.update()
    else:
        ui.status_bar.showMessage("Could not add empty impression")


def add_note(app, ui):
    annotation = app.visEngine.GetActiveAnnotation()
    if annotation is not None:
        if ui.ui_sur.page_sur_view_edit_insert_note.toPlainText() != "" \
                or ui.ui_sur.page_sur_view_edit_insert_link.toPlainText() !="":
            if ui.ui_sur.page_sur_view_edit_insert_note.toPlainText() != "":
                annotation.AddNote(ui.ui_sur.page_sur_view_edit_insert_note.toPlainText())
            if ui.ui_sur.page_sur_view_edit_insert_link.toPlainText() != "":
                annotation.AddWebLink(ui.ui_sur.page_sur_view_edit_insert_link.toPlainText())

            ui.ui_sur.page_sur_view_edit_insert_note.setPlainText("")
            ui.ui_sur.page_sur_view_edit_insert_link.setPlainText("")
            ui.ui_sur.page_sur_view_edit_report.update()
        else:
            ui.status_bar.showMessage("Could not add empty link or note")
    else:
        ui.status_bar.showMessage("No active finding, please select a finding to add notes")


def unlink_views(app, ui):
    if isinstance(ui.ui_sur.page_sur_view_edit_2d_view, QVTKRenderWindowInteractor):
        print("UNLINK")
        change_link(app, ui, ui.ui_sur.page_sur_view_edit_button_link_windows,
                    ui.ui_sur.page_sur_view_edit_2d_view, force="Deactivate\n2D-3D Link")

def change_link(app, ui, button, master_widget, slave_widget=None, force=None):
    if force is not None:
        button.setText(force)
    deactivate_str = "Deactivate\n2D-3D Link"
    activate_str = "Activate\n2D-3D Link"
    print(button.text())
    if button.text() == deactivate_str:
        app.visEngine.UnlinkWindows(master_widget)
        button.setText(activate_str)
        button.setIcon(QIcon(os.path.join("UI", "icons", "unlink.png")))
    elif button.text() == activate_str:
        app.visEngine.LinkWindows(master_widget, [slave_widget])
        button.setText(deactivate_str)
        button.setIcon(QIcon(os.path.join("UI", "icons", "link.png")))


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
    ui.status_bar.clearMessage()
    if change_prev_page:
        ui.prev_page = ui.stacked_sur.currentWidget()
    ui.stacked_sur.setCurrentWidget(new_page)


def logout(app, ui):
    unlink_views(app, ui)
    ui.current_sur_id = None
    ui.prev_page = None
    ui.stacked_sur.setCurrentWidget(ui.ui_sur.page_sur_home)
    ui.stacked_main.setCurrentWidget(ui.page_login)


def show_logout_popup(app, ui):
    print("LOGOUT")
    msg = QMessageBox()
    msg.setWindowTitle("Logout")
    msg.setText("Are you sure you want to logout?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes|msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        logout(app, ui)


# Changes the 2D image 'greyscale'
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


# Changes the 2D window slice orientation to AXIAL, SAGITALL or CORONAL
def change_slice_orientation(app, ui, group, widget):
    ui.status_bar.showMessage("Changing slice orientation, please wait...")
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    # Save the current annotations
    current_annots = []
    current_measurs =  []
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
    if group.checkedButton().text() == "ALL":
        for button in group.buttons():
            if button.text() != "ALL": button.setChecked(False)
        app.visEngine.SetTissue(widget, ["ALL"])
    else:
        ui.ui_pat.checkBox_All.setChecked(False)
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
def change_image_color(app,ui,widget):
    color_window = ui.ui_sur.page_sur_view_edit_2d_slider_color_window.value()
    color_level = ui.ui_sur.page_sur_view_edit_2d_slider_color_level.value()
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
        ui.ui_sur.page_sur_view_edit_tools.hide()
        button.setToolTip("Show advanced functionality for image manipulation")
    elif button.text() == show_str:
        button.setText(hide_str)
        ui.ui_sur.page_sur_view_edit_tools.show()
        button.setToolTip("Hide advanced functionality for image manipulation")


# Toggle 3D view spilt screen
def toggle3DSplit(app, ui, button):
    full_str = "3D Full Screen"
    half_str = "Split Screen"
    if button.text() == half_str:
        button.setText(full_str)
        button.setIcon(QIcon("UI\icons\\full_screen.png"))
        button.setToolTip("Expand 3D view")
        ui.ui_sur.page_sur_view_edit_2d_view_frame.show()
        ui.ui_sur.page_sur_view_edit_2d_slider_color_window.show()
        ui.ui_sur.page_sur_view_edit_2d_slider_color_level.show()
    elif button.text() == full_str:
        button.setText(half_str)
        button.setIcon(QIcon("UI\icons\\restore.png"))
        button.setToolTip("Return to split view")
        ui.ui_sur.page_sur_view_edit_2d_view_frame.hide()
        ui.ui_sur.page_sur_view_edit_2d_slider_color_window.hide()
        ui.ui_sur.page_sur_view_edit_2d_slider_color_level.hide()


# Toggle 2D view spilt screen
def toggle2DSplit(app, ui, button):
    full_str = "2D Full Screen"
    half_str = "Split Screen"
    if button.text() == half_str:
        button.setText(full_str)
        button.setIcon(QIcon("UI\icons\\full_screen.png"))
        button.setToolTip("Expand 2D view")
        ui.ui_sur.page_sur_view_edit_3d_view_frame.show()
    elif button.text() == full_str:
        button.setText(half_str)
        button.setIcon(QIcon("UI\icons\\restore.png"))
        button.setToolTip("Return to split view")
        ui.ui_sur.page_sur_view_edit_3d_view_frame.hide()


# Reset the camera on the views
def resetView(app, ui, widget):
    [w, l] = app.visEngine.ResetWidgetCamera(widget)
    if w: ui.ui_sur.page_sur_view_edit_2d_slider_color_window.setValue(w)
    if l: ui.ui_sur.page_sur_view_edit_2d_slider_color_level.setValue(l)