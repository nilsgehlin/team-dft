import os


class Patient(object):
    next_id = 0

    def __init__(self, first_name, last_name, age, sex="N/A"):
        self.id = str(Patient.next_id).zfill(4)
        Patient.next_id += 1
        self.password = self.id
        self.errands = {}
        # self.errands = {"0": Errand("0", "2020-01-01", "Complete", "CT", "GP", "TASK??", os.path.join("sample_dicom", "chestDICOM")),
        #                 "1": Errand("1", "2020-03-03", "Pending", "MRI", "Hospital", "TASK??")}
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex

    def add_errand(self, id, date, status, scan, clinic, task, dir=None):
        self.errands[str(id)] = Errand(str(id), date, status, scan, clinic, task, dir)

    def add_errand(self, errand):
        errand.order_id = str(len(self.errands))
        self.errands[errand.order_id] = errand

    def __str__(self):
        print("ID: {}\n"
              "Password: {}\n"
              "Errand ID's: {}\n"
              "Name: {} {}\n"
              "Age: {}\n"
              "Sex: {}".format(self.id, self.password, [errand.order_id for errand in self.errands.values()],
                               self.first_name, self.last_name, self.age, self.sex))



class Errand(object):
    def __init__(self, date, status, scan, clinic, task, dir=None):
        self.order_id = None
        self.date = date
        self.status = status
        self.scan = scan
        self.clinic = clinic
        self.task = task
        self.data_dir = dir
        self.report = None
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations += [annotation]

    def get_annotation(self, annot_id):
        for annot in self.annotations:
            if annot.annot_id == annot_id:
                return annot


class Scan(object):
    def __init__(self):
        pass