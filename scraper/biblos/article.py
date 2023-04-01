class Article():
    def __init__(self):
        self.title = None
        self.authors = None
        self.ext_authors = None
        self.typ = None
        self.series = None
        self.release_data = None
        self.points = None
        self.mnisw_list = None
        self.impact = None
    
    def __str__(self):
        return f"Title: {self.title}\nAuthors: {self.authors}\nExt_authors: {self.ext_authors}\nType: {self.typ}\nSeries: {self.series}\nRelease date: {self.release_date}\nPoints: {self.points}\nImpact: {self.impact}\nMNiWS list: {self.mnisw_list}"
    
    # Builder pattern
    def add_title(self,title):
        self.title=title
    def add_authors(self,authors):
        self.authors=authors
    def add_ext_authors(self,ext_authors):
        self.ext_authors=ext_authors
    def add_typ(self,typ):
        self.typ=typ
    def add_series(self,series):
        self.series=series
    def add_release_date(self,release_date):
        self.release_date=release_date
    def add_points(self,points):
        self.points=points
    def add_mnisw_list(self,mnisw_list):
        self.mnisw_list=mnisw_list
    def add_impact(self,impact):
        self.impact=impact