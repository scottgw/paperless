import os.path

from document import *

def dummy_document(dir_name):
    test_files = ['file1.pdf', 'file2.png', 'file3.tiff', 'file4.jpg']
    files = [os.path.join(dir_name) for file in test_files]
    return Document(set(files))
