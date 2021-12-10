class Document:

    def __init__(self):
        return

    docid = ""
    docno = ""
    score = 0.0
    docTitle = ""

    def getDocId(self):
        return self.docid

    def getDocNo(self):
        return self.docno

    def getScore(self):
        return self.score

    def getDocTitle(self):
        return self.docTitle

    # Getters
    def getDocYear(self):
        return self.docYear

    def getDocOrigin(self):
        return self.docOrigin

    def getDocDirector(self):
        return self.docDirector

    def getDocCast(self):
        return self.docCast

    def getDocGenre(self):
        return self.docGenre

    def getDocLink(self):
        return self.docLink

    def getDocPlot(self):
        return self.docPlot

    def setDocId(self, docid):
        self.docid = docid

    def setDocNo(self, no):
        self.docno = no

    def setScore(self, the_score):
        self.score = the_score

    def setDocTitle(self, title):
        self.docTitle = title

    def setDocYear(self, value):
        self.docYear = value

    def setDocOrigin(self, value):
        self.docOrigin = value

    def setDocDirector(self, value):
        self.docDirector = value

    def setDocCast(self, value):
        self.docCast = value

    def setDocGenre(self, value):
        self.docGenre = value

    def setDocLink(self, value):
        self.docLink = value

    def setDocPlot(self, value):
        self.docPlot = value

    def __str__(self) -> str:
        return self.docTitle