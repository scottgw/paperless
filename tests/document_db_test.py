import os
import os.path
import shutil
import unittest

from document_db import DocumentDB
from document_test_utils import *
from document import Document

test_dir = 'test_document_db'

def running_db():
    db = DocumentDB(test_dir)
    db.setup()
    return db

class Test(unittest.TestCase):
    def setUp(self):
        os.mkdir(test_dir)

    def tearDown(self):
        shutil.rmtree(test_dir)

    def test_document_db_creation(self):
        db = DocumentDB(test_dir)

    def test_document_db_setup(self):
        db = running_db()

    def test_document_db_add_correct_length(self):
        db = running_db()
        doc = dummy_document(test_dir)
        db.add(doc)

        self.assertEqual(db.length(), 1)

    def test_document_db_add_has(self):
        db = running_db()
        doc = dummy_document(test_dir)
        db.add(doc)

        self.assertTrue(db.has(doc))

    def test_document_db_empty_has_not(self):
        db = running_db()
        doc = dummy_document(test_dir)

        self.assertFalse(db.has(doc))

    def test_document_db_removed_has_not(self):
        db = running_db()
        doc = dummy_document(test_dir)
        db.add(doc)
        db.remove(doc)

        self.assertFalse(db.has(doc))

    def test_document_db_search_keyword_success(self):
        db = running_db()
        doc = dummy_document(test_dir)
        doc.keywords = u'42 dummy'
        db.add(doc)

        results = db.search_keywords(u'dummy')

        self.assertEqual(len(results), 1)

    def test_document_db_search_keyword_failure(self):
        db = running_db()
        doc = dummy_document(test_dir)
        doc.keywords = u'42 dummy'
        db.add(doc)

        results = db.search_keywords(u'satchmo')

        self.assertEqual(len(results), 0)

    def test_document_db_search_keyword_right_uuid(self):
        db = running_db()
        doc = dummy_document(test_dir)
        doc.keywords = u'42 dummy'
        db.add(doc)

        results = db.search_keywords(u'dummy')

        self.assertEqual(results[0]['uuid'], doc.uuid)


    def test_document_db_add_doc_with_no_files(self):
        db = running_db()
        doc = dummy_document(test_dir)
        doc.repo_files={}
        db.add(doc)

        self.assertTrue(db.has(doc))


if __name__ == '__main__':
    unittest.main()
