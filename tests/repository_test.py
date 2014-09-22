import unittest

from repository import Repository

repo_name = 'test_repository'

test_empty_files = set({u'empty1', u'empty2'})

def test_doc(repo):
    return repo.add_document(u'sendy', u'recipy', None,
                             u'welcome to the jungle', {})


def test_doc_with_files(repo):
    return repo.add_document(u'sendy', u'recipy', None,
                             u'welcome to the jungle',
                             test_empty_files)

class Test(unittest.TestCase):
    def setUp(self):
        for file in test_empty_files:
            open(file, 'a').close()

    def tearDown(self):
        import shutil
        import os

        for file in test_empty_files:
            os.remove(file)

        shutil.rmtree(repo_name)

    def test_repository_create(self):
        repo = Repository(repo_name)

    def test_repository_add_has(self):
        repo = Repository(repo_name)
        doc = test_doc(repo)
        self.assertTrue(repo.has_document_uuid(doc.uuid))

    def test_repository_add_files(self):
        repo = Repository(repo_name)
        doc = test_doc_with_files(repo)
        self.assertTrue(repo.has_document_uuid(doc.uuid))


    def test_repository_add_remove_has_not(self):
        repo = Repository(repo_name)
        doc = test_doc(repo)

        repo.remove_document(doc)

        self.assertFalse(repo.has_document_uuid(doc.uuid))

    def test_repository_add_search_keyword_success(self):
        repo = Repository(repo_name)
        doc = test_doc(repo)

        result = repo.search_keywords('jungle')

        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()
