import uuid

class DocType:
    pass

class BillDocType(DocType):
    pass

class Document:
    def __init__(self,
                 repo_files=set({}),
                 date=None,
                 sender=None,
                 recipient=None,
                 doctype=None,
                 keywords=u''):
        self.uuid = unicode(uuid.uuid1())
        self.repo_files = repo_files
        self.date = date
        self.sender = sender
        self.recipient = recipient
        self.doctype = doctype
        self.keywords = keywords

    def remove_file(self, file):
        self.repo_files.remove(file)

    def add_file(self, file):
        self.repo_files.add(file)
