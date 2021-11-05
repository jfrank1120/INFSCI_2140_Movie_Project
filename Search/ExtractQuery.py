import Classes.Query as Query
from Classes import Path
from PreProcessData import StopWordRemover
from PreProcessData import WordNormalizer
from PreProcessData import WordTokenizer
from PreProcessData import TopicCollection
class ExtractQuery:

    def __init__(self):
        # 1. you should extract the 4 queries from the Path.TopicDir
        # 2. the query content of each topic should be 1) tokenized, 2) to lowercase, 3) remove stop words, 4) stemming
        # 3. you can simply pick up title only for query.
        self.topic = Path.TopicDir
        # Initialize preprocessors
        self.stopwordRemover = StopWordRemover.StopWordRemover()
        self.normalizer = WordNormalizer.WordNormalizer()
        self.tokenizer = WordTokenizer.WordTokenizer
        # A collection processor is created to read topics.txt
        self.collection = TopicCollection.TopicCollection()
        
        self.count = 0
        self.delimiter = " "
        return

    # Return extracted queries with class Query in a list.
    def getQuries(self):
        queries = []
        # extract queries from topicDir
        # while True:
        doc = self.collection.getDocument()
        # print(doc)
        # break
        # instantiate query object
        query = Query.Query()
        # if there are no more queries exit
        if doc == None:
            return
        # get topicID and querytitle
        topicId, queryTitle = doc.values()

        # Remove trailing newline characters
        query.setTopicId(topicId)

        queryContent = []
        # tokenize
        tokenizer = self.tokenizer(content=queryTitle)
        while True:
            word = tokenizer.nextWord()
            if word == None:
                break
            word = self.normalizer.lowercase(word)
            if self.stopwordRemover.isStopword(word) == False:
                queryContent.append(self.normalizer.stem(word))
        
        # store queries as Query instance
        # all the words are joined with a delimiter (e.g. space) to form a string
        query.setQueryContent(self.delimiter.join(queryContent))
        queries.append(query)
        return queries

