import whoosh.index as index
from whoosh.fields import Schema, ID, TEXT, DATETIME, STORED
import whoosh.query
from whoosh.qparser import QueryParser

def uuid_query(uuid):
     return whoosh.query.Term("uuid", uuid)

def doc_uuid_query(doc):
    return uuid_query(doc.uuid)

class DocumentDB:
    def __init__(self, location):
        assert location
        self.schema  = Schema(uuid=ID(stored=True, unique=True),
                              sender=TEXT(stored=True),
                              recipient=TEXT(stored=True),
                              keywords=TEXT(stored=True),
                              date=DATETIME(stored=True),
                              repo_files=STORED)
        self.location = location

    def setup(self):
        import os
        if not os.path.exists(self.location):
            os.mkdir(self.location)
            self.ix = index.create_in(self.location, self.schema)
        elif index.exists_in(self.location):
            self.ix = index.open_dir(self.location, schema=self.schema)
        else:
            self.ix = index.create_in(self.location, self.schema)

    def length(self):
        return self.ix.doc_count()

    def add(self, doc):
        writer = self.ix.writer()

        writer.add_document(uuid=doc.uuid,
                            sender=doc.sender,
                            recipient=doc.recipient,
                            date=doc.date,
                            keywords=doc.keywords,
                            repo_files=doc.repo_files)
        writer.commit()

    def has(self, doc):
        query = doc_uuid_query(doc)

        with self.ix.searcher() as searcher:
            results = searcher.search(query)
            return len(results) > 0

    def has_uuid(self, uuid):
        query = uuid_query(uuid)

        with self.ix.searcher() as searcher:
            results = searcher.search(query)
            return len(results) > 0

    def remove(self, doc):
        query = doc_uuid_query(doc)

        with self.ix.writer() as writer:
            writer.delete_by_query(query)

    def search_keywords(self, search_str):
        query = whoosh.query.Term('keywords', search_str)

        with self.ix.searcher() as searcher:
            results = searcher.search(query) #, groupedby=['keywords', 'uuid'])
            results = [result.fields() for result in results]

        return results
