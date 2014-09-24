from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QUrl
from PyQt4.QtDeclarative import QDeclarativeView, QDeclarativeImageProvider

from popplerqt4 import Poppler

import document_ui

class QPaperlessDoc(QtGui.QWidget):
    def __init__(self, doc, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = document_ui.Ui_Form()
        self.ui.setupUi(self)

# class DocumentImageProvider(QDeclarativeImageProvider):
#     def __init__(self, images=[]):
#         super(QDeclarativeImageProvider,
#               self).__init__(QDeclarativeImageProvider.Image)

#         self.images = images

#     def add_pdf(self, filename):
#         pdf = Poppler.Document.load(filename)
#         pdf.setRenderHint(Poppler.Document.TextAntialiasing)
#         for pageNum in xrange(pdf.numPages()):
#             page = pdf.page(pageNum)
#             self.images.append(page.renderToImage())

#     def load_from_document(self, repo, doc):
#         import os.path
#         import time

#         now = time.time()

#         for repofile in doc.repo_files:
#             path = repo.file_path(repofile)
#             _, ext = os.path.splitext(path)

#             if ext == '.pdf':
#                 self.add_pdf(path)
#             else:
#                 print 'extension', ext
#                 assert False

#         print 'time elapsed', time.time() - now

#     def clear(self):
#         self.images = []

#     def requestImage(self, idx, size, requestedSize):
#         return self.images[int(idx)]
