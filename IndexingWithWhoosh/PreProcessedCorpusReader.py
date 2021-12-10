import Classes.Path as Path

class PreprocessedCorpusReader:

    corpus = 0

    def __init__(self, type):
        self.corpus = open(Path.ResultHM1 + type, "r", encoding="utf8")

    def nextDocument(self):
        val=self.corpus.readline().strip()
        if val=="":
            self.corpus.close()
            return
        docNo, title = val.split("__#__")
        content=self.corpus.readline().strip()
        return {'docNo' : docNo,
                'title' : title,
                'content' : content}