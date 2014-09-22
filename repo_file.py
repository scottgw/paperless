class RepoFile:
    def __init__(self, token, filetype):
        self.filetype = filetype
        self.token = token

    def __unicode__(self):
        return self.token.archive_path()
