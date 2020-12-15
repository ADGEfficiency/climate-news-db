class Newspapers:
    """Business logic"""
    def __init__(self, db, papers):
        self.papers = {}
        for paper in papers:
            self.papers[paper] = db(paper)

    def get_all_articles(self):
        data = []
        for paper, db in self.papers.items():
            data.append(db.get())
        return data
