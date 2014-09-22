from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QUrl
from PyQt4.QtDeclarative import QDeclarativeView, QDeclarativeImageProvider

from popplerqt4 import Poppler

class DocumentImageProvider(QDeclarativeImageProvider):
    def __init__(self, images=[]):
        super(QDeclarativeImageProvider,
              self).__init__(QDeclarativeImageProvider.Image)

        self.images = images

    def add_pdf(self, filename):
        pdf = Poppler.Document.load(filename)
        pdf.setRenderHint(Poppler.Document.TextAntialiasing)
        for pageNum in xrange(pdf.numPages()):
            page = pdf.page(pageNum)
            self.images.append(page.renderToImage())

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

    def clear(self):
        self.images = []

    def requestImage(self, idx, size, requestedSize):
        return self.images[int(idx)]

class SearchResultWidget:
    qml_location = 'paperless.qml'

    def __init__(self, view, results=[]):
        # an explicit reference to the provider has to be maintained
        # else a segfault ensues (collected prematurely I assume)
        self.img_provider = DocumentImageProvider()

        self.view = view # QDeclarativeView(self)
        self.results = results

        engine = self.view.engine()
        engine.addImageProvider('document_images', self.img_provider)

        ctx = engine.rootContext()
        ctx.setContextProperty('documentModel', QtCore.QStringList())

        self.view.setSource(QUrl(SearchResultWidget.qml_location))
        self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)

    def new_results(self, repo, docs):
        self.img_provider.clear()

        for doc in docs:
            self.img_provider.load_from_document(repo, doc)

        self.update_document_model()

    def update_document_model(self):
        index_list = QtCore.QStringList()

        for i in xrange(len(self.img_provider.images)):
            index_list.append(str(i))

        ctx = self.view.engine().rootContext()
        ctx.setContextProperty('documentModel', index_list)
