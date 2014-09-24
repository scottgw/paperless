from datetime import datetime

from PyQt4 import QtGui, QtCore

from paperless_ui import Ui_MainWindow

from edit_dialog import EditDialog
from search_controller import SearchController
from repository import Repository
from settings import Settings

class PaperlessWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.settings = Settings()

        self._set_data_dir()

        self.repo = Repository(self.settings.getDataDir())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen.triggered.connect(self.openFile)

        self.search_controller = SearchController(self.ui.search_result_box,
                                                  self.ui.search_line,
                                                  self.repo)

        self.ui.clear_button.pressed.connect(self.search_controller.clear)
        self.ui.add_button.pressed.connect(self.show_dialog)

    def _set_data_dir(self):
        import os.path
        while not self.settings.getDataDir():
            file_dialog = QtGui.QFileDialog(self, 'Choose data directory')
            file_dialog.setFileMode(QtGui.QFileDialog.Directory)

            if file_dialog.exec_():
                files = file_dialog.selectedFiles()
                if len(files) > 0 and os.path.exists(str(files[0])):
                    self.settings.setDataDir(files[0])

    def show_dialog(self):
        dialog = EditDialog(self.repo, self)
        result = dialog.exec_()

    def loadPdfFromFilename(self, filename):
        document = Poppler.Document.load(filename)
        document.setRenderHint(Poppler.Document.TextAntialiasing)
        page = document.page(0)
        image = page.renderToImage()
        pixmap = QtGui.QPixmap.fromImage(image)
        print 'FIXME: loaded pdf'
        # self.scene.addPixmap(pixmap)

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Open File', '$HOME')

        if filename:
            self.loadPdfFromFilename(filename)
