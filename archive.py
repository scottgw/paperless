import os
import os.path
import shutil

class Archive:
    def __init__(self, name):
        self.name = name
        if not os.path.exists(self.name):
            os.mkdir(self.name)

    def _path_to_doc(self, doc):
        return os.path.join(self.name, doc.uuid)

    def get(self, archive_token):
        path = self.token_path(archive_token)

        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
        else:
            return None

    def token_path(self, archive_token):
        arch_path = archive_token.archive_path()
        return os.path.join(self.name, arch_path)

    def add_document(self, doc):
        os.mkdir(self._path_to_doc(doc))

    def add_file(self, filename, archive_token):
        shutil.copy2(filename, self.token_path(archive_token))

    def add_bytes(self, bytes, archive_token):
        with open(self.token_path(archive_token), 'w') as file:
            file.write(bytes)

    def remove_document(self, document):
        os.rmdir(self._path_to_doc(document))

    def remove_file(self, archive_token):
        os.remove(self.token_path(archive_token))

    def has_document(self, document):
        return os.path.exists(self._path_to_doc(document))
