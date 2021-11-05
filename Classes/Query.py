class Query:

    def __init__(self):
        return

    queryContent = ""
    topicId = ""
    narr = ""
    description = ""

    def getQueryContent(self):
        return self.queryContent

    def getTopicId(self):
        return self.topicId

    def setQueryContent(self, content):
        self.queryContent=content

    def setTopicId(self, id):
        self.topicId=id
    
    def getDescription(self):
        return self.description

    def getNarrative(self):
        return self.narr

    def setDescription(self, description):
        self.description = description

    def setNarrative(self, narr):
        self.narr = narr

    def __repr__(self) -> str:
        return "Query()"
    
    def __str__(self) -> str:
        return (self.topicId,"\t",self.queryContent)