import Classes.Path as Path
import json

class TopicCollection:

    def __init__(self):
        self.file = Path.TopicDir
        self.file_obj = open(self.file)
        return

    def getDocument(self):
        dict_ =  json.load(self.file_obj)
        # self.file_obj.close()
        return dict_