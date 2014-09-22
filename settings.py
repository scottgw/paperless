from PyQt4 import QtCore

class Settings(QtCore.QSettings):
    data_dir_key = 'data_dir'

    def __init__(self):
        super(Settings, self).__init__()

    def getDataDir(self):
        if not self.contains(Settings.data_dir_key):
            val = None
        else:
            val = str(self.value(Settings.data_dir_key).toString())

        return val

    def setDataDir(self, dir):
        self.setValue(Settings.data_dir_key, dir)
