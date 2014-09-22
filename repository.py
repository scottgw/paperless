from archive_token import ArchiveToken
from archive import Archive
from document_db import DocumentDB
from document import Document
from repo_file import RepoFile

"""
A repository holds and searches all documents.
"""
class Repository:
    def __init__(self, dir):
        import os
        import os.path
        index_dir_name = 'index'
        archive_file_name = 'documents'
        self.dir = dir

        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

        self.index = DocumentDB(os.path.join(dir, index_dir_name))
        self.index.setup()

        self.archive = Archive(os.path.join(dir, archive_file_name))

        self.doc_map = {}

    def file_path(self, repofile):
        return self.archive.token_path(repofile.token)

    """
    Adds a document consisting of the arguments as data and returns it.
    The filenames should be strings, they will be stored in the document
    as the appropriate references (not strings).
    """
    def add_document(self, sender, recipient, date, keywords, files):
        assert isinstance(keywords, unicode)

        doc = self._create_document(sender, recipient, date, keywords, files)
        self.index.add(doc)

        return doc

    def remove_file(self, doc, file):
        doc.remove_file(file)
        self.index.update_doc(doc)
        self.archive.remove_file(file)

    def remove_document(self, doc):
        self.archive.remove_document(doc)
        self.index.remove(doc)

    def has_document_uuid(self, uuid):
        return self.index.has_uuid(uuid)

    def search_keywords(self, keywords):
        matches = self.index.search_keywords(keywords)
        docs = []

        for match in matches:
            doc = Document()
            for key in match.keys():
                setattr(doc, key, match[key])
            docs.append(doc)

        return docs

    """
    Creates a document consisting of the arguments, and enters
    the files into the archive.
    """
    def _create_document(self, sender, recipient, date, keywords, files):
        doc = Document()

        self.archive.add_document(doc)
        
        def create_repo_file(filename):
            import os.path
            token = ArchiveToken(filename, doc.uuid)
            file_type = os.path.splitext(filename)
            return RepoFile(token, file_type)

        for file in files:
            repo_file = create_repo_file(file)

            doc.add_file(repo_file)
            self.archive.add_file(file, repo_file.token)

        doc.sender = sender
        doc.recipient = recipient
        doc.date = date
        doc.keywords = keywords

        return doc
