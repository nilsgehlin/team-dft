

class Patient(object):
    def __init__(self, id):
        self.id = id
        self.password = id
        self.errands = {"0": Errand("0", "2020-01-01", "Complete", "CT", "GP", "TASK??"), "1": Errand("1", "2020-03-03", "Pending", "MRI", "Hospital", "TASK??")}


class Errand(object):
    def __init__(self, order_id, date, status, scan, clinic, task):
        self.order_id = order_id
        self.date = date
        self.status = status
        self.scan = scan
        self.clinic = clinic
        self.task = task
        self.data_2d = None
        self.data_3d = None
        self.report = None


class Scan(object):
    def __init__(self):
        pass