from search_result_widget import QPaperlessDoc

class SearchController:
    def __init__(self, result_box, search_string_view, repo):
        self.search_string = ""
        self.repo = repo
        self.result_box = result_box
        self.search_string_view = search_string_view

        self.search_string_view.returnPressed.connect(self.update_search)

    def update_search(self):
        self.new_search(self.search_string_view.text())
        
    def new_search(self, search_string):
        matches = self.repo.search_keywords(search_string)

        for match in matches:
            pdoc = QPaperlessDoc(self.repo, match, self.result_box)
            self.result_box.layout().addWidget(pdoc)

    def clear(self):
        self.search_string_view.setText('')
        self.result_box
