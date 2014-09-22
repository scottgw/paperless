import os
import os.path
import shutil
import unittest

from archive_token import *
from document import *
from archive import *
from document_test_utils import *

test_file = 'test.repo'
test_dir = 'repo_test'
dummy_filenames = ['test1', 'test2', 'test3']
dummy_files = [os.path.join(test_dir, filename) for
               filename in dummy_filenames]

class Test(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)

        for file in dummy_files:
            open(file, 'a').close()

    def tearDown(self):
        if os.path.exists(test_file):
            shutil.rmtree(test_file)

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_archive_creation(self):
        archive = Archive(test_file)

    def test_archive_add(self):
        archive = Archive(test_file)
        doc = dummy_document(test_dir)
        archive.add_document(doc)

        for file in dummy_files:
            archive_token = ArchiveToken(file, doc.uuid)
            archive.add_file(file, archive_token)

    def test_archive_add_has_document(self):
        archive = Archive(test_file)
        doc = dummy_document(test_dir)
        archive.add_document(doc)

        for file in dummy_files:
            archive_token = ArchiveToken(file, doc.uuid)
            archive.add_file(file, archive_token)

        self.assertTrue(archive.has_document(doc))

    def test_archive_add_get_failure(self):
        archive = Archive(test_file)
        doc = dummy_document(test_dir)
        archive.add_document(doc)

        for file in dummy_files:
            archive_token = ArchiveToken(file, doc.uuid)
            archive.add_file(file, archive_token)

        otherfile = ArchiveToken('other_file', doc.uuid)

        retrieved = archive.get(otherfile)

        self.assertEqual(retrieved, None)

    def test_archive_add_get_equal(self):
        archive = Archive(test_file)
        doc = dummy_document(test_dir)
        archive.add_document(doc)

        original = 'oh happy day'
        archive_token = ArchiveToken('dummy_file', doc.uuid)
        archive.add_bytes(original, archive_token)
        
        retrieved = archive.get(archive_token)

        self.assertNotEqual(retrieved, None)
        self.assertEqual(retrieved, original)

    def test_archive_add_remove(self):
        archive = Archive(test_file)
        doc = dummy_document(test_dir)
        archive.add_document(doc)

        text = 'oh happy day'
        archive_token = ArchiveToken('dummy_file', doc.uuid)
        archive.add_bytes(text, archive_token)
        archive.remove_file(archive_token)
        archive.remove_document(doc)

        self.assertFalse(archive.has_document(doc))
        

if __name__ == '__main__':
    unittest.main()
