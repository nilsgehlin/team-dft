from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtPrintSupport import QPrintDialog

import jinja2
import os
import webbrowser

template_dir = "templates"
if __name__ == "reportGeneration.Report":
    template_dir = os.path.join("UI", "reportGeneration", template_dir)


class Report(QTextBrowser):
    def __init__(self, parent_widget, show_segmentation_on_click=True):
        super().__init__(parent_widget)
        self.setReadOnly(True)
        self.patient = None
        self.errand = None
        self.show_segmentation_on_click = show_segmentation_on_click
        self.template_name = None
        self.vtk_widget_2d = None
        self.vtk_widget_3d = None
        self.setOpenLinks(False)
        if show_segmentation_on_click:
            print("TRUE")
            self.anchorClicked.connect(self.on_annotation_clicked)

    def update(self):
        file_loader = jinja2.FileSystemLoader(template_dir)
        env = jinja2.Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        template = env.get_template(self.template_name + ".html")
        output = template.render(errand=self.errand, patient=self.patient)
        self.setHtml(output)

    def load_report(self, template_name, patient, order_id, vtk_widget_2d=None, vtk_widget_3d=None, vis_engine=None, user=None):
        self.patient = patient
        self.errand = patient.errands[order_id]
        self.template_name = template_name
        self.vtk_widget_2d = vtk_widget_2d
        self.vtk_widget_3d = vtk_widget_3d
        self.vis_engine = vis_engine
        self.update()
        # with open(os.path.join(template_dir, self.template_name + ".css")) as style_sheet_file:
        #     self.setStyleSheet(style_sheet_file.read())


    # def on_annotation_clicked(self, url_input):
    #     #     annotation_id = url_input.toString()
    #     #     annotation_clicked = self.errand.get_annotation(annotation_id)
    #     #     if self.show_wiki_on_click:
    #     #         search_term = annotation_clicked.GetLocation().replace(" ", "+")
    #     #         search_url = "https://en.wikipedia.org/w/index.php?cirrusUserTesting" \
    #     #                      "=glent_m0&search={}&title=Special%3ASearch&go=Go&ns0=1".format(search_term)
    #     #         webbrowser.open(search_url)

    # Callback function for annotation click on the report
    def on_annotation_clicked(self, url_input):
        annotation_id = url_input.toString()
        annotation_clicked = self.errand.get_annotation(annotation_id)

        # If the user is a patient, no need to toggle annotations
        if self.template_name == "patient":
            self.vis_engine.GoToAnnotation(self.vtk_widget_2d, annotation_clicked)
            if self.vtk_widget_3d is not None: self.vis_engine.GoToAnnotation(self.vtk_widget_3d, annotation_clicked)
        # Else toggle the annotations
        else:
            if self.vis_engine.HasAnnotation(self.vtk_widget_2d, annotation_clicked):
                self.vis_engine.RemoveAnnotations(self.vtk_widget_2d, [annotation_clicked])
                if self.vtk_widget_3d is not None: self.vis_engine.RemoveAnnotations(self.vtk_widget_3d, [annotation_clicked])
            else:
                self.vis_engine.AddSegmentations(self.vtk_widget_2d, [annotation_clicked])
                self.vis_engine.AddMeasurements(self.vtk_widget_2d, [annotation_clicked])
                self.vis_engine.GoToAnnotation(self.vtk_widget_2d, annotation_clicked)
                if self.vtk_widget_3d is not None:
                    self.vis_engine.AddSegmentations(self.vtk_widget_3d, [annotation_clicked])
                    self.vis_engine.GoToAnnotation(self.vtk_widget_3d, annotation_clicked)



    def save_to_pdf(self, filename):
        dialog = QPrintDialog()
        self.document().print_(dialog.printer())



# if __name__ == "__main__":
#     import sys
#
#     class Examination:
#         def __init__(self, patient, modality):
#             self.patient = patient
#             self.modality = modality
#             self.annotations = []
#
#         def add_annotation(self, annotation):
#             self.annotations += [annotation]
#
#         def get_annotation(self, annot_id):
#             for annot in self.annotations:
#                 if annot.annot_id == annot_id:
#                     return annot
#             return None
#
#     class Patient:
#         def __init__(self, first_name, last_name, age):
#             self.first_name = first_name
#             self.last_name = last_name
#             self.age = age
#
#     class Annotation:
#         def __init__(self, annot_id, location, finding, color):
#             self.location = location
#             self.finding = finding
#             self.color = color
#             self.annot_id = annot_id
#
#         def __str__(self):
#             return "Location: {}\n" \
#                    "Finding: {}\n" \
#                    "Annotation ID: {}".format(self.location, self.finding, self.annot_id)
#
#     class Window(QWidget):
#         def __init__(self):
#             super().__init__()
#
#             self.title = "PyQt5 Plain TextEdit"
#             self.top = 200
#             self.left = 500
#             self.width = 400
#             self.height = 300
#
#             self.InitWindow()
#
#         def InitWindow(self):
#             self.setWindowIcon(QtGui.QIcon("icon.png"))
#             self.setWindowTitle(self.title)
#             self.setGeometry(self.left, self.top, self.width, self.height)
#
#             vbox = QVBoxLayout()
#
#             patient = Patient("Nils", "Gehlin", 26)
#             exam = Examination(patient, "CT")
#             exam.add_annotation(Annotation(1, "Brain Parenchyma", "T2 hyperintense white matter lesions", (255, 0, 0)))
#             exam.add_annotation(Annotation(2, "Skull", "Huge fracture", (0, 255, 0)))
#             self.report = Report("radiologist", exam)
#             vbox.addWidget(self.report)
#             self.setLayout(vbox)
#             self.show()
#
#         def keyPressEvent(self, event):
#             print(event)
#             # Press S to save as pdf
#             if event.key() == 83:
#                 self.report.save_to_pdf("test_pdf.pdf")
#
#             # Press N to add a new dummy annotation dynamically
#             if event.key() == 78:
#                 self.report.examination.add_annotation(Annotation(3, "Heart", "Blown up", (0, 0, 255)))
#                 print(self.report.examination.annotations[-1])
#                 self.report.update()
#
#
#     App = QApplication(sys.argv)
#     window = Window()
#     sys.exit(App.exec())