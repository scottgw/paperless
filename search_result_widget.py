from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QUrl
from PyQt4.QtDeclarative import QDeclarativeView, QDeclarativeImageProvider

from popplerqt4 import Poppler

import document_ui

class QPdfPage(QtGui.QLabel):
    def __init__(self, page, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.page = page

        self.image = page.renderToImage(18, 18)

        # size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
        #                                 QtGui.QSizePolicy.Preferred)
        # size_policy.setVerticalStretch(200)
        # image_widget.setSizePolicy(size_policy)
        self.setPixmap(QtGui.QPixmap.fromImage(self.image))

    # def sizeHint(self):
    #     pixmap = self.pixmap()
    #     width = pixmap.width()
    #     height = pixmap.height()
    #     return QtCore.QSize(width, height + 20)
        

class QPaperlessDoc(QtGui.QWidget):
    def __init__(self, repo, doc, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = document_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.sender_label.setText(doc.sender)
        self.ui.recipient_label.setText(doc.recipient)

        self.load_from_document(repo, doc)

    def add_pdf(self, filename):
        pdf = Poppler.Document.load(filename)
        pdf.setRenderHint(Poppler.Document.TextAntialiasing)
        for pageNum in xrange(min(1, pdf.numPages())):
            page = pdf.page(pageNum)
            pdf_page = QPdfPage(page)
            # image = page.renderToImage(18, 18)

            # image_widget = QtGui.QLabel()
            # size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
            #                                 QtGui.QSizePolicy.Preferred)
            # size_policy.setVerticalStretch(200)
            # image_widget.setSizePolicy(size_policy)
            # image_widget.setPixmap(QtGui.QPixmap.fromImage(image))

            self.ui.pic_widget.layout().addWidget(pdf_page)

    def load_from_document(self, repo, doc):
        import os.path
        import time

        now = time.time()

        for repofile in doc.repo_files:
            path = repo.file_path(repofile)
            _, ext = os.path.splitext(path)

            if ext == '.pdf':
                self.add_pdf(path)
            else:
                print 'extension', ext
                assert False

        print 'time elapsed', time.time() - now


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
