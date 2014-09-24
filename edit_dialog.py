from datetime import datetime

from PyQt4 import QtGui, QtCore

from edit_dialog_ui import Ui_Dialog

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
