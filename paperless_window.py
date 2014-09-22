from datetime import datetime

from PyQt4 import QtGui, QtCore

from paperless_ui import Ui_MainWindow
from edit_dialog_ui import Ui_Dialog

from search_result_widget import SearchResultWidget
from search_controller import SearchController
from repository import Repository
from settings import Settings

class EditDialog(QtGui.QDialog):
    def __init__(self, repo, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.add_file_button.pressed.connect(self.add_file)
        self.ui.remove_file_button.pressed.connect(self.remove_file)

        self.file_list = QtCore.QStringList()
        self.file_list_model = QtGui.QStringListModel(self.file_list)

        self.ui.file_list_view.setModel(self.file_list_model)

        self.repo = repo

    def exec_(self):
        result = QtGui.QDialog.exec_(self)

        if result == QtGui.QDialog.Accepted:
            sender = self.ui.sender_edit.text()
            recipient = self.ui.recipient_edit.text()

            qdate = self.ui.date_edit.selectedDate()
            date = datetime.combine(qdate.toPyDate(), datetime.min.time())

            keywords = self.ui.keywords_edit.text()
            files = [unicode(file) for
                     file in list(self.file_list_model.stringList())]
            doc = self.repo.add_document(unicode(sender),
                                         unicode(recipient),
                                         date,
                                         unicode(keywords),
                                         files)
        else:
            doc = None

        return doc

    def add_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Add document')
        model = self.file_list_model
        model.insertRows(model.rowCount(), 1)
        model.setData(model.index(model.rowCount() - 1), filename)

    def remove_file(self):
        list_view = self.ui.file_list_view
        model = self.file_list_model

        for index in list_view.selectedIndexes():
            model.removeRow(index.row())

class PaperlessWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.settings = Settings()

        self._set_data_dir()

        self.repo = Repository(self.settings.getDataDir())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen.triggered.connect(self.openFile)
        self.search_result_widget = SearchResultWidget(self.ui.search_view)
        self.search_controller = SearchController(self.search_result_widget,
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
