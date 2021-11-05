from typing import Collection
import Classes.Path as Path
import whoosh.index as index
from whoosh.reading import IndexReader
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexTokenizer
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
import itertools

# Efficiency and memory cost should be paid with extra attention.
class MyIndexReader:

    searcher=[]

    def __init__(self, type):
        path_dir= Path.IndexWikiDir
        # if type=="trectext":
        # path_dir = Path.IndexTextDir
        self.searcher = index.open_dir(path_dir).searcher()
        self.collection_size = None
        self.reader = index.open_dir(path_dir).reader()
        self.all_document = len(list(self.reader.all_doc_ids()))
        self.getWordCount = len(list(self.reader.all_terms()))
    
    def __len__(self):
        return self.all_document
    
    # Total number of words in the collection
    def CollectionSize(self):
        if self.collection_size is None:
            count = map(self.getDocLength, range(self.__len__()))
            self.collection_size = sum(list(count))
            self.avg_doc_length = self.collection_size/self.__len__()
        return self.collection_size
    

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        return self.searcher.document_number(doc_no=docNo)

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        # print(len(self.searcher.stored_fields))
        return self.searcher.stored_fields(docId)["doc_no"]

    def getDocTitle(self, docId):
        return self.searcher.stored_fields(docId)["doc_title"]

    # Return DF.
    def DocFreq(self, token):
        results = self.searcher.search(Term("doc_content", token))
        return len(results)

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        results = self.searcher.search(Term("doc_content", token), limit=None)
        count = 0
        for result in results:
            words = self.searcher.stored_fields(result.docnum)["doc_content"].split(" ")
            for word in words:
                if word==token:
                    count+=1
        return count
    
    def RelativeCollectionFreq(self, token, mu):
        return self.CollectionFreq(token) + mu

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        results = self.searcher.search(Term("doc_content", token), limit=None)
        postList = {}
        for result in results:
            words = self.searcher.stored_fields(result.docnum)["doc_content"].split(" ")
            count=0
            for word in words:
                if word==token:
                    count+=1
            postList[result.docnum]=count
        return postList

    # Return the length of the requested document.
    def getDocLength(self, docId):
        words = self.searcher.stored_fields(docId)["doc_content"].split(" ")
        return len(words)
