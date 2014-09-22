class SearchController:
    def __init__(self, result_view, search_string_view, repo):
        assert repo
        assert result_view
        assert search_string_view

        self.search_string = ""
        self.repo = repo
        self.result_view = result_view
        self.search_string_view = search_string_view

        self.search_string_view.returnPressed.connect(self.update_search)

    def update_search(self):
        self.new_search(self.search_string_view.text())
        
    def new_search(self, search_string):
        matches = self.repo.search_keywords(search_string)

        self.result_view.new_results(self.repo, matches)

    def clear(self):
        self.search_string_view.setText('')
        self.result_view.new_results(self.repo, [])
