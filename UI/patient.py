import os


class Patient(object):
    def __init__(self, id, first_name, last_name, age, sex):
        self.id = id
        self.password = str(id).zfill(4)
        self.errands = {}
        # self.errands = {"0": Errand("0", "2020-01-01", "Complete", "CT", "GP", "TASK??", os.path.join("sample_dicom", "chestDICOM")),
        #                 "1": Errand("1", "2020-03-03", "Pending", "MRI", "Hospital", "TASK??")}
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex

    def add_errand(self, id, date, status, scan, clinic, task, dir=None):
        self.errands[str(id)] = Errand(str(id), date, status, scan, clinic, task, dir)


class Errand(object):
    def __init__(self, order_id, date, status, scan, clinic, task, dir=None):
        self.order_id = order_id
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