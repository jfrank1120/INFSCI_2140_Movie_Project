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
        indexWriter.index(doc[0], doc[1], doc[2])
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

def search():
    return_data = []
    index = MyIndexReader.MyIndexReader("wiki")
    search = QueryRetreivalModel.QueryRetrievalModel(index)
    extractor = ExtractQuery.ExtractQuery()
    queries= extractor.getQuries()
    for query in queries:
        print(query.topicId,"\t",query.queryContent)
        results = search.retrieveQuery(query, 20)
        rank = 1
        for result in results:
            # u_result = u' '.join((str(rank), result.getDocTitle())).decode('utf-8').strip()
            title = result.getDocTitle()#.decode('utf-8')
            return_data.append(f"{rank} , {title}")
            print(rank,title) #.encode('ascii', 'ignore'))
            # print(rank,result.getDocTitle(),' ',result.getScore())
            rank += 1
    return return_data

"""
startTime = datetime.datetime.now()
# PreProcess()
# WriteIndex('wiki')
search()
endTime = datetime.datetime.now()
print ("index text corpus running time: ", endTime - startTime)
"""