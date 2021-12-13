from PreProcessData.MovieCollection import MovieCollection
import IndexingWithWhoosh.PreProcessedCorpusReader as PreprocessedCorpusReader
import IndexingWithWhoosh.MyIndexWriter as MyIndexWriter
import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery
import PreProcessData.StopWordRemover as StopWordRemover
import PreProcessData.WordNormalizer as WordNormalizer
import PreProcessData.WordTokenizer as WordTokenizer
import Classes.Path as Path
import datetime
from Classes.Query import Query as Query
from Classes.Document import Document as Document
import random

# from main1 import query
import sqlalchemy as db
import Classes.Path as Path
import itertools

DEFAULT_NUM_MOVIES = 10
DEFAULT_NUM_KEYWORDS = 11

def PreProcess():
    # Open the collection by type.
    # if type == "trectext":
    type = 'wiki'
    collection = MovieCollection()
    # print(collection.visualizeDataset())
    # print(collection.visualizeDatabase())
    # Initialize essential objects.
    stopwordRemover = StopWordRemover.StopWordRemover()
    normalizer = WordNormalizer.WordNormalizer()
    wr = open(Path.ResultHM1 + type, "w", encoding="utf8")
    doc = []

    #Process the corpus, document by document, iteratively.
    count = 0
    while True:
        doc = collection.nextDocument()
        if doc == None:
            break
        docNo, title, content = doc

        # Output the docNo.
        wr.write(str(docNo)+"__#__"+title+"\n")

        # Output the preprocessed content.
        tokenizer = WordTokenizer.WordTokenizer(content)
        while True:
            word = tokenizer.nextWord()
            if word == None:
                break
            word = normalizer.lowercase(word)
            if stopwordRemover.isStopword(word) == False:
                wr.write(normalizer.stem(word) + " ")
        wr.write("\n")
        count += 1
        if count % 10000 == 0:
            print("finish " + str(count) + " docs")
    wr.close()
    return

def WriteIndex(type):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus =PreprocessedCorpusReader.PreprocessedCorpusReader(type)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter(type)
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc)
        count+=1
        if count%10000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return

def ReadIndex(type, token):
    # Initiate the index file reader.
    index =MyIndexReader.MyIndexReader(type)
    # retrieve the token.
    df = index.DocFreq(token)
    ctf = index.CollectionFreq(token)
    print(" >> the token \""+token+"\" appeared in "+ str(df) +" documents and "+ str(ctf) +" times in total")
    if df>0:
        posting = index.getPostingList(token)
        for docId in posting:
            docNo = index.getDocNo(docId)
            print(docNo+"\t"+str(docId)+"\t"+str(posting[docId]))

# def search():
#     return_data = []
#     index = MyIndexReader.MyIndexReader("wiki")
#     search = QueryRetreivalModel.QueryRetrievalModel(index)
#     extractor = ExtractQuery.ExtractQuery()
#     queries= extractor.getQuries()
#     for query in queries:
#         print(query.topicId,"\t",query.queryContent)
#         results = search.retrieveQuery(query, 20)
#         rank = 1
#         for result in results:
#             # u_result = u' '.join((str(rank), result.getDocTitle())).decode('utf-8').strip()
#             title = result.getDocTitle()#.decode('utf-8')
#             return_data.append(f"{rank} , {title}")
#             print(rank,title) #.encode('ascii', 'ignore'))
#             # print(rank,result.getDocTitle(),' ',result.getScore())
#             rank += 1
#     return return_data

class SearchforMovie():
    def __init__(self):
        self.index = MyIndexReader.MyIndexReader("wiki")
        self.search = QueryRetreivalModel.QueryRetrievalModel(self.index)
        self.extractor = ExtractQuery.ExtractQuery()
        self.query = None
        self.result = None
        self.result_by_origin = None
        self.result_by_year = None
        self.engine = db.create_engine('sqlite:///'+ Path.DatabaseDir + '?check_same_thread=False')
        self.connection = self.engine.connect()
        metadata = db.MetaData()
        # self.table = db.select([table])
        self.movies = db.Table('table', metadata, autoload=True, autoload_with=self.engine)

        # query = db.select([self.movies.columns.index, self.movies.columns.Title, self.movies.columns.Plot])
        # self.ResultProxy = self.connection.execute(query)
        

    def set_query(self, value):
        """
        Expects a string separated by space
        """
        q = Query()
        q.setQueryContent(value)
        self.query = q
    
    def populateAttributes(self, docTitle):
        """
        Given a string as movie title, return a Document object,
        with all the attributes in the dataset
        """

        doc = Document()
        q = db.select([self.movies]).where(self.movies.columns.Title == docTitle)
        result = self.connection.execute(q).fetchall()
        doc.setDocNo(result[0][0])
        doc.setDocYear(result[0][1])
        doc.setDocTitle(result[0][2])
        doc.setDocOrigin(result[0][3])
        doc.setDocDirector(result[0][4])
        doc.setDocCast(result[0][5])
        doc.setDocGenre(result[0][6])
        doc.setDocLink(result[0][7])
        doc.setDocPlot(result[0][8])
        return doc

    def retrieve(self, topK, query=None):
        """
        Retrieves topK results from movie dataset.
        Arguments
        topK : integer, number of movie names to retrieve
        query : If self.query is None, use this query
        """
        startTime = datetime.datetime.now()
        movie_list = []
        if self.query == None:
            self.query = self.set_query(query)
        result = self.search.retrieveQuery(self.query, topK)
        for k in result:
            movie_list.append(k.getDocTitle())
        endTime = datetime.datetime.now()
        elapsed_time = endTime - startTime
        self.result = result
        # self._create_results_by_origin()
        # self._create_results_by_year()
        
        return [movie_list, elapsed_time]
    
    def get_similar(self, moviename):
        # movie_list = self.retrieve(20, query=moviename)
        movie_list = []
        q = Query()
        content = db.select([self.movies.columns.Plot]).where(self.movies.columns.Title == moviename)
        text = self.connection.execute(content).fetchall()[0]
        # print(text[0])
        keywords = random.sample(text[0].split(' '), DEFAULT_NUM_KEYWORDS)
        q.setQueryContent(' '.join(keywords))
        result = self.search.retrieveQuery(q, DEFAULT_NUM_MOVIES)
        for k in result:
            movie_list.append(k.getDocTitle())
        return movie_list

    def filter_results_by_origin(self, movie_list, origin):
        self.result_by_origin = {}
        q = db.select([self.movies.columns.Title], self.movies.columns.Title.in_(movie_list)).where(getattr(self.movies.columns, 'Origin/Ethnicity') == origin)
        result = self.connection.execute(q).fetchall()
        return [f[0] for f in result]

    def filter_results_by_year(self, movie_list, year):
        self.result_by_origin = {}
        q = db.select([self.movies.columns.Title], self.movies.columns.Title.in_(movie_list)).where(getattr(self.movies.columns, 'ReleaseYear') > year)
        result = self.connection.execute(q).fetchall()
        return [f[0] for f in result]

    def get_recommendation_by_past_search(self, movie_list):
        # print(' '.join(movie_list))
        
        q = db.select([self.movies.columns.Plot], self.movies.columns.Title.in_(movie_list))
        result = self.connection.execute(q).fetchall()
        all_words = ' '.join([f[0] for f in result]).split(" ")
        keywords = random.sample(all_words, DEFAULT_NUM_KEYWORDS)
        # keywords = random.sample(text[0].split(' '), 10)
        query = Query()
        query.setQueryContent(' '.join(keywords))
        titles = [k.getDocTitle() for k in self.search.retrieveQuery(query, DEFAULT_NUM_MOVIES)]
        return titles



if __name__ == "__main__":
    dummyClass = SearchforMovie()
    dummyClass.set_query("city action jump")
    result = dummyClass.retrieve(topK=10)
    print(result)
    doc = dummyClass.populateAttributes(result[5])
    print("Finding similar movies : ", result[4])
    similar_movies = dummyClass.get_similar(result[4])
    print(similar_movies)
    print(dummyClass.filter_results_by_origin(similar_movies, "American"))
    print(dummyClass.filter_results_by_year(similar_movies, 1950))
    past_movie_list = similar_movies
    print(dummyClass.get_recommendation_by_past_search(past_movie_list))
    
    


# """
# startTime = datetime.datetime.now()
# # PreProcess()
# # WriteIndex('wiki')
# search()
# endTime = datetime.datetime.now()
# print ("index text corpus running time: ", endTime - startTime)
# """