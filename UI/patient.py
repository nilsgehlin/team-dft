import os
from visualizationEngine.annotation.Annotation import Annotation, AnnotationList

#########################
##### Patient Class #####
#########################
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

    
    # Serializes the important class items to a JSON compatible dictionary
    def toJson(self):
        errands_json = []
        for _, errand in self.errands.items():
            errands_json.append(errand.toJson())

        patient_json = dict(id =  self.id, 
                     password = self.password,
                     first_name = self.first_name,
                     last_name = self.last_name,
                     age = self.age,
                     sex = self.sex,
                     errands = errands_json
                     )
        return patient_json

        
    # Deserializes the items needed to instantiate the class from JSON dictionary
    @staticmethod
    def fromJson(data):
        patient = Patient(data['first_name'], data['last_name'], data['age'], data['sex'])

        errands_data = data['errands']
        for errand_data in errands_data:
            patient.add_errand(Errand.fromJson(errand_data))

        return patient


########################
##### Errand Class #####
########################
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
        self.annotations = AnnotationList()
        self.temp_annotations = AnnotationList()
        self.impressions = []
        self.temp_impressions = []

    def add_annotation(self, annotation):
        self.annotations += [annotation]

    def get_annotation(self, annot_id):
        return self.annotations.GetAnnotationFromID(annot_id)

    def add_impression(self, *args):
        if len(args) == 1:
            print(args)
            self.impressions += [args[0]]
        elif len(args) == 2:
            print(args)
            self.impressions += [Impression(args[0], args[1])]
    

    # Serializes the important class items to JSON compatible dictionary
    def toJson(self):
        annots_json = []
        for annot in self.annotations:
            annots_json.append(annot.toJson())

        imprs_json = []
        for impr in self.impressions:
            imprs_json.append(impr.toJson())

        errand_json = dict(order_id =  self.order_id, 
                     date = self.date,
                     status = self.status,
                     scan = self.scan,
                     clinic = self.clinic,
                     task = self.task,
                     data_dir = self.data_dir,
                     report = self.report,
                     annotations = annots_json,
                     impressions = imprs_json
                     )
        return errand_json


    # Deserializes the items needed to instantiate the class from JSON dictionary
    @staticmethod
    def fromJson(data):
        errand = Errand(data['date'],data['status'],data['scan'],data['clinic'],data['task'],data['data_dir'])
        
        annots_data = data["annotations"]
        for annot_data in annots_data:
            errand.add_annotation(Annotation.fromJson(annot_data))

        imprs_data = data["impressions"]
        for impr_data in imprs_data:
            errand.add_impression(Impression.fromJson(impr_data))

        return errand


class Impression(object):
    def __init__(self, doctor, impression):
        self.doctor = doctor
        self.impression = impression
        self.reviewed = False

    def GetDoctor(self):
        return self.doctor

    def GetImpression(self):
        return self.impression

    def SetDoctor(self, doctor):
        self.doctor = doctor

    def SetImpression(self, impression):
        self.impression = impression

    def toJson(self):
        json = dict(doctor=self.GetDoctor(), impression=self.GetImpression())
        return json

    # Deserializes an annotation from Json
    @staticmethod
    def fromJson(data):
        impr = Impression(data['doctor'], data['impression'])
        impr.reviewed = True
        return impr



######################
##### Scan Class #####
######################
class Scan(object):
    def __init__(self):
        pass