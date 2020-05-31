from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
import os
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from reportGeneration.Report import Report

import UI.patient
import visualizationEngine.annotation.Annotation


# SETUP FUNCTIONS #


def setup_functionality(app, ui):
    home_page_setup(app, ui)
    my_profile_page_setup(ui)
    image_status_page_setup(app, ui)
    view_scan_page_setup(app, ui)


# DEPRECATED
# def home_page_setup(app, ui):
#     add_errands(app, ui)

#     ui.ui_pat.page_pat_home_logout.clicked.connect(lambda: show_logout_popup(app, ui))
#     ui.ui_pat.page_pat_home_button_my_profile.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_my_profile))
#     ui.ui_pat.page_pat_home_button_proceed.clicked.connect(lambda: go_to_errand_page(app, ui))
#     ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemClicked.connect(lambda: ui.ui_pat.page_pat_home_button_proceed.setEnabled(True))
#     ui.ui_pat.page_pat_home_treeWidget_treatment_list.itemDoubleClicked.connect(
#         lambda: go_to_errand_page(app, ui))


def home_page_setup(app, ui):
    add_errands(app, ui)
    add_profile(app, ui)

    ui.ui_pat.page_pat_home_progress_bar.hide()

    ui.ui_pat.page_pat_home_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_home_button_my_profile.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_my_profile))
    ui.ui_pat.page_pat_home_button_view_status.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_image_status)) # TODO
    # ui.ui_pat.page_pat_home_button_share.clicked.connect() # TODO
    # ui.ui_pat.page_pat_home_button_download.clicked.connect() # TODO
    ui.ui_pat.page_pat_home_button_view.clicked.connect(lambda: go_to_view_scan_page(app, ui))
    ui.ui_pat.page_pat_home_treeWidget_errand_list.itemClicked.connect(lambda: select_item(app, ui))
    ui.ui_pat.page_pat_home_treeWidget_errand_list.itemDoubleClicked.connect(
        lambda: go_to_view_scan_page(app, ui) if ui.ui_pat.page_pat_home_button_view.isEnabled() else None)


def my_profile_page_setup(ui):
    # ui.ui_pat.page_pat_my_profile_logout.clicked.connect(lambda: show_logout_popup(ui))
    ui.ui_pat.page_pat_my_profile_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))


def image_status_page_setup(app, ui):
    ui.ui_pat.page_pat_image_status_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_image_status_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))
    # ui.ui_pat.page_pat_image_status_button_request_notification.clicked.connect() # TODO


def view_scan_page_setup(app, ui):
    ui.ui_pat.page_pat_view_scan_rad_annotations = Report(ui.ui_pat.page_pat_view_scan_rad_annotations_frame)
    ui.ui_pat.page_pat_view_scan_rad_annotations_frame_grid.addWidget(ui.ui_pat.page_pat_view_scan_rad_annotations, 0, 0, 1, 1)

    ui.ui_pat.page_pat_view_scan_button_logout.clicked.connect(lambda: show_logout_popup(app, ui))
    ui.ui_pat.page_pat_view_scan_button_back.clicked.connect(lambda: change_page(ui, ui.ui_pat.page_pat_home))

    # Annotation and image navigation buttons
    ui.ui_pat.page_pat_view_scan_button_next_note.clicked.connect(
        lambda: go_to_next_annot(app, ui, ui.ui_pat.page_pat_view_scan_2d_view, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_previous_note.clicked.connect(
        lambda: go_to_previous_annot(app, ui, ui.ui_pat.page_pat_view_scan_2d_view, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_play_pause.clicked.connect(
        lambda: toggle_animation(app, ui, ui.ui_pat.page_pat_view_scan_button_play_pause, ui.ui_pat.page_pat_view_scan_2d_view))

    # Image slice buttons
    ui.ui_pat.page_pat_view_scan_button_next_slice.pressed.connect(
        lambda: change_image_slice(app, ui, ui.ui_pat.page_pat_view_scan_2d_view, 1))
    ui.ui_pat.page_pat_view_scan_button_next_slice.released.connect(
        lambda: stop_image_slice(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))
    ui.ui_pat.page_pat_view_scan_button_previous_slice.pressed.connect(
        lambda: change_image_slice(app, ui, ui.ui_pat.page_pat_view_scan_2d_view, -1))
    ui.ui_pat.page_pat_view_scan_button_previous_slice.released.connect(
        lambda: stop_image_slice(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))

    # Linking windows
    ui.ui_pat.page_pat_view_scan_button_link_windows.clicked.connect(
        lambda: change_link(app, ui, ui.ui_pat.page_pat_view_scan_button_link_windows, ui.ui_pat.page_pat_view_scan_2d_view, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_2d_fullscreen.clicked.connect(
        lambda: toggle2DSplit(app, ui, ui.ui_pat.page_pat_view_scan_button_2d_fullscreen));
    ui.ui_pat.page_pat_view_scan_button_3d_fullscreen.clicked.connect(
        lambda: toggle3DSplit(app, ui, ui.ui_pat.page_pat_view_scan_button_3d_fullscreen))

    # Zooming buttons 2D
    ui.ui_pat.page_pat_view_scan_button_2d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))
    ui.ui_pat.page_pat_view_scan_button_2d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))
    ui.ui_pat.page_pat_view_scan_button_2d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))
    ui.ui_pat.page_pat_view_scan_button_2d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))

    # Zooming buttons 3D
    ui.ui_pat.page_pat_view_scan_button_3d_zoom_in.pressed.connect(
        lambda: start_zoom_in(app, ui, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_3d_zoom_in.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_3d_zoom_out.pressed.connect(
        lambda: start_zoom_out(app, ui, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_button_3d_zoom_out.released.connect(
        lambda: stop_zoom(app, ui, ui.ui_pat.page_pat_view_scan_3d_view))

    # 2D image color buttons
    ui.ui_pat.page_pat_view_scan_2d_slider_color_window.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))
    ui.ui_pat.page_pat_view_scan_2d_slider_color_level.valueChanged.connect(
        lambda: change_image_color(app, ui, ui.ui_pat.page_pat_view_scan_2d_view))

    # Advanced options
    ui.ui_pat.page_pat_view_scan_tools.hide()
    ui.ui_pat.page_pat_view_scan_button_tools.clicked.connect(
        lambda: toggleSettings(app, ui, ui.ui_pat.page_pat_view_scan_button_tools))
    ui.ui_pat.page_pat_view_scan_radio_group_orientation.buttonClicked.connect(
        lambda: change_slice_orientation(app, ui, ui.ui_pat.page_pat_view_scan_radio_group_orientation, ui.ui_pat.page_pat_view_scan_2d_view))
    ui.ui_pat.page_pat_view_scan_check_group_tissue.buttonClicked.connect(
        lambda: change_volume_tissue(app, ui, ui.ui_pat.page_pat_view_scan_check_group_tissue, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_check_group_link.buttonClicked.connect(
        lambda: change_link_configuration(app, ui, ui.ui_pat.page_pat_view_scan_check_group_link))
    ui.ui_pat.page_pat_view_scan_slider_transparency_volume.valueChanged.connect(
        lambda: change_volume_transparency(app, ui, ui.ui_pat.page_pat_view_scan_slider_transparency_volume, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_slider_transparency_segmentation.valueChanged.connect(
        lambda: change_segmentation_transparency(app, ui, ui.ui_pat.page_pat_view_scan_slider_transparency_segmentation, ui.ui_pat.page_pat_view_scan_3d_view))
    ui.ui_pat.page_pat_view_scan_slider_transparency_active.valueChanged.connect(
        lambda: change_segment_transparency(app, ui, ui.ui_pat.page_pat_view_scan_slider_transparency_active, ui.ui_pat.page_pat_view_scan_3d_view))


# GO TO FUNCTIONS #


# DEPRECATED
# def go_to_errand_page(app, ui):
#     app.current_errand_id = ui.ui_pat.page_pat_home_treeWidget_treatment_list.currentItem().text(2)
#     ui.ui_pat.page_pat_errand_treeWidget_errand_list.clear()
#     errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
#     root_item = QTreeWidgetItem([errand.task, errand.date, errand.scan, errand.status, errand.clinic])
#     ui.ui_pat.page_pat_errand_treeWidget_errand_list.addTopLevelItem(root_item)
#     ui.ui_pat.page_pat_errand_button_view.setEnabled(True if errand.status == "Complete" else False)

#     # ui.ui_pat.page_pat_errand_report # TODO show radiology report here

#     change_page(ui, ui.ui_pat.page_pat_errand)


def go_to_view_scan_page(app, ui):
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    if app.visEngine.GetDirectory() is not errand.data_dir:
        ui.status_bar.showMessage("Loading report, please wait...")
        ui.ui_pat.page_pat_home_progress_bar.show()

        # Setup UI
        ui.ui_pat.page_pat_home_progress_bar.setValue(5)
        ui.ui_pat.page_pat_view_scan_2d_view = QVTKRenderWindowInteractor(ui.ui_pat.page_pat_view_scan_2d_view_frame)
        ui.ui_pat.page_pat_view_scan_2d_view_frame_grid.addWidget(ui.ui_pat.page_pat_view_scan_2d_view, 0, 0, 1, 1)

        ui.ui_pat.page_pat_view_scan_3d_view = QVTKRenderWindowInteractor(ui.ui_pat.page_pat_view_scan_3d_view_frame)
        ui.ui_pat.page_pat_view_scan_3d_view_frame_grid.addWidget(ui.ui_pat.page_pat_view_scan_3d_view, 0, 0, 1, 1)

        ui.ui_pat.page_pat_view_scan_button_link_windows.setText("Deactivate\n2D-3D Link")

        # Setup the engine
        ui.ui_pat.page_pat_home_progress_bar.setValue(10)
        app.visEngine.SetDirectory(errand.data_dir)
        app.visEngine.SetupImageUI(ui.ui_pat.page_pat_view_scan_2d_view, do_segmentation=False)
        app.visEngine.SetupVolumeUI(ui.ui_pat.page_pat_view_scan_3d_view)
        app.visEngine.LinkWindows(ui.ui_pat.page_pat_view_scan_2d_view, [ui.ui_pat.page_pat_view_scan_3d_view])

        # Add all annotations to the viewers
        ui.ui_pat.page_pat_home_progress_bar.setValue(30)
        app.visEngine.AddSegmentations(ui.ui_pat.page_pat_view_scan_2d_view, errand.annotations)
        ui.ui_pat.page_pat_home_progress_bar.setValue(60)
        app.visEngine.AddMeasurements(ui.ui_pat.page_pat_view_scan_2d_view, errand.annotations)
        ui.ui_pat.page_pat_home_progress_bar.setValue(90)
        app.visEngine.AddSegmentations(ui.ui_pat.page_pat_view_scan_3d_view, errand.annotations)

    ui.ui_pat.page_pat_view_scan_rad_annotations.load_report(template_name="patient",
                                                             patient=app.pat_dict[app.current_pat_id],
                                                             order_id=app.current_errand_id,
                                                             vtk_widget_2d=ui.ui_pat.page_pat_view_scan_2d_view,
                                                             vtk_widget_3d=ui.ui_pat.page_pat_view_scan_3d_view,
                                                             vis_engine=app.visEngine)
    ui.ui_pat.page_pat_home_progress_bar.setValue(100)
    ui.ui_pat.page_pat_home_progress_bar.hide()
    ui.status_bar.clearMessage()

    change_page(ui, ui.ui_pat.page_pat_view_scan)


# HELP FUNCTIONS #

def add_profile(app, ui):
    patient = app.pat_dict[app.current_pat_id]
    ui.ui_pat.page_pat_home_label_name.setText(patient.first_name + " " + patient.last_name)
    ui.ui_pat.page_pat_home_label_age.setText(str(patient.age) + " years old")
    ui.ui_pat.page_pat_home_label_social_security_number.setText("321-67-8194")
    ui.ui_pat.page_pat_home_label_phone_number.setText("+1 415 201 4987")
    ui.ui_pat.page_pat_home_label_address.setText("72 Sunshine St\nSan Francisco, CA 94114, USA")
    ui.ui_pat.page_pat_home_label_email.setText(patient.first_name.lower() + "." + patient.last_name.lower() + "@gmail.com")
    pixmap = QPixmap(os.path.join("databases", "patient_database", patient.first_name.lower() + "_" + patient.last_name.lower() + ".png"))
    if pixmap.isNull():
        ui.ui_pat.page_pat_home_label_profile_picture.setText("No profile picture available")
    else:
        ui.ui_pat.page_pat_home_label_profile_picture.setPixmap(pixmap)


def add_errands(app, ui):
    ui.ui_pat.page_pat_home_treeWidget_errand_list.clear()
    for errand in app.pat_dict[app.current_pat_id].errands.values():
        root_item = QTreeWidgetItem([errand.order_id, errand.date, errand.task, errand.scan, errand.status, errand.clinic])
        ui.ui_pat.page_pat_home_treeWidget_errand_list.addTopLevelItem(root_item)


def change_link(app, ui, button, master_widget, slave_widget):
    deactivate_str = "Deactivate\n2D-3D Link"
    activate_str = "Activate\n2D-3D Link"
    if button.text() == deactivate_str:
        app.visEngine.UnlinkWindows(master_widget)
        button.setText(activate_str)
        button.setIcon(QIcon("UI\icons\\unlink.png"))
    elif button.text() == activate_str:
        app.visEngine.LinkWindows(master_widget, [slave_widget])
        button.setText(deactivate_str)
        button.setIcon(QIcon("UI\icons\\link.png"))


def change_page(ui, new_page):
    ui.prev_page = ui.stacked_pat.currentWidget()
    ui.stacked_pat.setCurrentWidget(new_page)


def logout(ui):
    ui.prev_page = None
    ui.ui_pat.page_pat_home_button_view.setEnabled(False)
    ui.stacked_pat.setCurrentWidget(ui.ui_pat.page_pat_home)
    ui.stacked_main.setCurrentWidget(ui.page_login)


def show_logout_popup(app, ui):
    msg = QMessageBox()
    msg.setWindowTitle("Logout")
    msg.setText("Are you sure you want to logout?")
    msg.setIcon(msg.Question)

    msg.setStandardButtons(msg.Yes|msg.No)
    msg.setDefaultButton(msg.No)
    msg.setEscapeButton(msg.No)

    ret = msg.exec_()
    if ret == msg.Yes:
        app.current_pat_id = None
        logout(ui)


def select_item(app, ui):
    app.current_errand_id = ui.ui_pat.page_pat_home_treeWidget_errand_list.currentItem().text(0)
    errand = app.pat_dict[app.current_pat_id].errands[app.current_errand_id]
    ui.ui_pat.page_pat_home_button_view.setEnabled(True if errand.status == "Complete" else False)
    if errand.status == "Complete":
        ui.ui_pat.page_pat_home_label_info.setText("Double-click order or click 'View' see report")
    else:
        ui.ui_pat.page_pat_home_label_info.setText("This scan is waiting for diagnosis, please select a scan with status 'Complete'")


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
    color_window = ui.ui_pat.page_pat_view_scan_2d_slider_color_window.value()
    color_level = ui.ui_pat.page_pat_view_scan_2d_slider_color_level.value()
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
    if widget_2d is not None: app.visEngine.GoToAnnotation(widget_2d, annots[next_annot_idx])
    if widget_3d is not None: app.visEngine.GoToAnnotation(widget_3d, annots[next_annot_idx])
    app.visEngine.SetActiveAnnotation(annots[next_annot_idx])


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
    if widget_2d is not None: app.visEngine.GoToAnnotation(widget_2d, annots[prev_annot_idx])
    if widget_3d is not None: app.visEngine.GoToAnnotation(widget_3d, annots[prev_annot_idx])
    app.visEngine.SetActiveAnnotation(annots[prev_annot_idx])


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
        button.setToolTip("Play slice animation on 2D images")
    elif button.text() == play_str:
        button.setText(pause_str)
        button.setIcon(QIcon("UI\icons\\pause.png"))
        button.setToolTip("Pause slice animation on 2D images")
    app.visEngine.ToggleSliceAnnimation(widget)


# Toggle advanced setting on the app
def toggleSettings(app, ui, button):
    hide_str = "Hide Advanced Tools"
    show_str = "Show Advanced Tools"
    if button.text() == hide_str:
        button.setText(show_str)
        ui.ui_pat.page_pat_view_scan_tools.hide()
        button.setToolTip("Show advanced functionality for image manipulation")
    elif button.text() == show_str:
        button.setText(hide_str)
        ui.ui_pat.page_pat_view_scan_tools.show()
        button.setToolTip("Hide advanced functionality for image manipulation")


# Toggle 3D view spilt screen
def toggle3DSplit(app, ui, button):
    full_str = "3D Full Screen"
    half_str = "Split Screen"
    if button.text() == half_str:
        button.setText(full_str)
        button.setIcon(QIcon("UI\icons\\full_screen.png"))
        button.setToolTip("Expand 3D view")
        ui.ui_pat.page_pat_view_scan_label_2d.show()
        ui.ui_pat.page_pat_view_scan_2d_view_frame.show()
        ui.ui_pat.page_pat_view_scan_2d_slider_color_window.show()
        ui.ui_pat.page_pat_view_scan_2d_slider_color_level.show()
        ui.ui_pat.page_pat_view_scan_button_2d_zoom_in.show()
        ui.ui_pat.page_pat_view_scan_button_2d_zoom_out.show()
        ui.ui_pat.page_pat_view_scan_button_2d_fullscreen.show()
    elif button.text() == full_str:
        button.setText(half_str)
        button.setIcon(QIcon("UI\icons\\restore.png"))
        button.setToolTip("Return to split view")
        ui.ui_pat.page_pat_view_scan_label_2d.hide()
        ui.ui_pat.page_pat_view_scan_2d_view_frame.hide()
        ui.ui_pat.page_pat_view_scan_2d_slider_color_window.hide()
        ui.ui_pat.page_pat_view_scan_2d_slider_color_level.hide()
        ui.ui_pat.page_pat_view_scan_button_2d_zoom_in.hide()
        ui.ui_pat.page_pat_view_scan_button_2d_zoom_out.hide()
        ui.ui_pat.page_pat_view_scan_button_2d_fullscreen.hide()


# Toggle 2D view spilt screen
def toggle2DSplit(app, ui, button):
    full_str = "2D Full Screen"
    half_str = "Split Screen"
    if button.text() == half_str:
        button.setText(full_str)
        button.setIcon(QIcon("UI\icons\\full_screen.png"))
        button.setToolTip("Expand 2D view")
        ui.ui_pat.page_pat_view_scan_label_3d.show()
        ui.ui_pat.page_pat_view_scan_3d_view_frame.show()
        ui.ui_pat.page_pat_view_scan_button_3d_zoom_in.show()
        ui.ui_pat.page_pat_view_scan_button_3d_zoom_out.show()
        ui.ui_pat.page_pat_view_scan_button_3d_fullscreen.show()
    elif button.text() == full_str:
        button.setText(half_str)
        button.setIcon(QIcon("UI\icons\\restore.png"))
        button.setToolTip("Return to split view")
        ui.ui_pat.page_pat_view_scan_label_3d.hide()
        ui.ui_pat.page_pat_view_scan_3d_view_frame.hide()
        ui.ui_pat.page_pat_view_scan_button_3d_zoom_in.hide()
        ui.ui_pat.page_pat_view_scan_button_3d_zoom_out.hide()
        ui.ui_pat.page_pat_view_scan_button_3d_fullscreen.hide()
