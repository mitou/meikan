from pykintone import model

class Person(model.kintoneModel):
    def __init__(self):
        super(Person, self).__init__()
        self.name = ''
        self.note = ''
        self.tags = ''


class Output(model.kintoneModel):
    def __init__(self):
        super(Output, self).__init__()
        self.html = ''
