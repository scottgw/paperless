import os
import os.path
import shutil
import unittest

from document_test_utils import *
from document import *

test_dir = 'test_document'

def test_path(filename):
    return os.join(test_dir, filename)

class Test(unittest.TestCase):
    def setUp(self):
        os.mkdir(test_dir)

    def tearDown(self):
        shutil.rmtree(test_dir)

    def test_document_creation(self):
        doc = dummy_document(test_dir)

    def test_document_has_repofiles(self):
        doc = dummy_document(test_dir)
        doc.repo_files

    def test_document_has_date(self):
        doc = dummy_document(test_dir)
        doc.date

    def test_document_has_keywords(self):
        doc = dummy_document(test_dir)
        doc.keywords
        

if __name__ == '__main__':
    unittest.main()
