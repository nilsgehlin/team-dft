import os
from visualizationEngine.annotation.Annotation import Annotation, AnnotationList


#########################
##### Doctor Class ######
#########################
class Doctor(object):
    next_id = 0

    def __init__(self, first_name, last_name, age, sex, title, profession, clinic, department):
        self.id = str(Doctor.next_id).zfill(4)
        Doctor.next_id += 1
        self.password = self.id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.title = title
        self.profession = profession
        self.clinic = clinic
        self.department = department
        self.signature = None

    def __str__(self):
        print("ID: {}\n"
              "Password: {}\n"
              "Name: {} {} {}\n"
              "Age: {}\n"
              "Sex: {}".format(self.id, self.password, self.title, self.first_name, self.last_name, self.age, self.sex))

    def get_signature(self):
        if self.signature is not None:
            return self.signature
        else:
            return "{}. {}, {}, {}".format(self.title, self.last_name, self.department, self.clinic)


    # Serializes the important class items to a JSON compatible dictionary
    def toJson(self):
        doctor_json = dict(id=self.id, password=self.password, first_name=self.first_name, last_name=self.last_name,
                           age=self.age, sex=self.sex, title=self.title, profession=self.profession, clinic=self.clinic,
                           department=self.department)
        return doctor_json

    # Deserializes the items needed to instantiate the class from JSON dictionary
    @staticmethod
    def fromJson(data):
        return Doctor(data['first_name'], data['last_name'], data['age'], data['sex'], data['title'], data['profession'],
                      data['clinic'], data['department'])