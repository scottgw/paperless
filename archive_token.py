import uuid
import os.path

class ArchiveToken:
    def __init__(self, filename, parent_uuid):
        self.uuid = unicode(uuid.uuid1())
        self.parent_uuid = parent_uuid
        _, self.filename = os.path.split(filename)

    """
    Constructs a path for this token in the archive that will be unique.

    This is current a combination of the parent's UUID, the UUID for this
    document and the original filename.
    """
    def archive_path(self):
        return os.path.join(self.parent_uuid, self.uuid + '_' + self.filename)
