from pykintone import model

class Person(model.kintoneModel):
    def __init__(self):
        super(Person, self).__init__()
        self.name = ''
        self.note = ''
        self.tags = ''

    def from_tuple(self, args):
        (self.name, self.note, self.tags, self.record_id, self.rivision) = args
        return self

    def to_tuple(self):
        return (self.name, self.note, self.tags, self.record_id, self.revision)

class Output(model.kintoneModel):
    def __init__(self):
        super(Output, self).__init__()
        self.html = ''
