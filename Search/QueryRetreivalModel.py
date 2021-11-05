import Classes.Query as Query
import Classes.Document as Document
import Classes.Path as Path


from itertools import repeat
import numpy as np
import os

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.mu = 300
        # print(self)
        # Use a flag to load these variables or recalculate for corpus
        self.reload = False
        flag = (not os.path.isfile(Path.Variables)) or self.reload
        # Get total number of documents
        # Get total number of unique terms
        # Get collection size
        if flag:
            # print("recalculating ...")
            self.number_docs = len(self.indexReader)
            self.unique_word_count = self.indexReader.getWordCount
            self.csize = self.indexReader.CollectionSize()
            self.save()
        else:
            # print("loading ..")
            self.number_docs = None
            self.unique_word_count = None
            self.csize = None
            self.load()
        # Calculate relative frequency size for the collection
        # Increase frequency of each unique term by mu 
        self.ref_size = (self.mu*self.unique_word_count) + self.csize
        return

    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    
    def populateResults(self, total_docId, keys):
        """
        Populates a dictionary with (docId, score) pairs.

        Args:
        total_docId : A complete list of docIds for which the function needs to calculate the score
        keys : A list of keywords from the query

        Returns:
        A dictionary  with (docId, score) pairs.
        """
        result = {}
        # Get relative collection frequencies for each element in keys
        cfs = list(map(self.indexReader.RelativeCollectionFreq, keys, repeat(self.mu)))

        # Get posting lists of for each term in query
        postings = list(map(self.indexReader.getPostingList, keys))
        
        # Calculate score for each document
        for docId in total_docId:
            # Retrieve document length
            dlen = self.indexReader.getDocLength(docId)

            # Get counts of different query terms in this document
            counts = list(map(self.check_count, 
                              repeat(docId), 
                              range(len(keys)), 
                              repeat(postings))) 

            # Calculate probability score for each document
            score = self.getScore(dlen,
                                   self.mu, 
                                   counts, 
                                   cfs, 
                                   self.ref_size)

            # Store (docID, score) pairs in a dictionary
            result[docId] = score    
        return result

    def getScore(self, dlen, mu, counts, cfs, csize):
        """
        Calculate probability score with Query likelihood model, also includes Dirichlet smoothing
        Args: 
        dlen : Document length
        mu : mu hyperparameter for smoothing
        counts : corresponding counts of all the keywords in this document
        cfs : relative collection frequencies for all the keywords
        csize : relative collection frequency of the collection

        Returns:
        score : log probability score which tells if the document is relevant to query, higher is better 
        """
        dmu = dlen + mu
        dmu_inv = 1/dmu
        dlen_inv = 1/dlen
        csize_inv = 1/csize
        score = dlen*dmu_inv*dlen_inv*np.array(counts) + mu*dmu_inv*csize_inv*np.array(cfs)
        return np.sum(np.log(score))    
    
    def check_count(self, docId, kid, postings):
        """
        Check if this document contains the keyword, and return the frequency
        
        Args:
        docId: the document
        kid: keyword index in query
        postings: A list containing posting lists of keywords, at the same index
        
        Returns:
        Frequency of keyword in the document with docId
        """
        post = postings[kid]
        if docId in post:
            return post[docId]
        else:
            return 0

    def getUnion(self, query):
        """
        Calculate union of posting list for each query term

        Args:
        query : String of query terms separated by space

        Returns:
        posting_union : A list of all documents that contain one or more of the query terms
        """
        keys = query.queryContent.split(" ")
        posting_union = set()
        for k in keys:
            posting = self.indexReader.getPostingList(k)
            posting_union = set.union(set(posting.keys()), set(posting_union))
        return list(posting_union)

    def retrieveQuery(self, query, topN):
        """
        Retrieves query results. Returns the list of topN documents using Query Likelihood Model.

        Args: 
        query : input string, query terms separated by space
        topN : return topN documents

        Returns:
        topk : List of topN documents with highest score
        """
        # print(self.mu)
        keys = query.queryContent.split(" ")
        result = {}
        # Get a exclusive list of all documents which contain one or more words in the query
        total_docId = self.getUnion(query)
        # Get scores for each document in the list
        result = self.populateResults(total_docId, keys)

        # Sort the documents with respect to score in descending order
        topk = []
        result_sorted = dict(sorted(result.items(), reverse=True, key=lambda item: item[1]))
        for i, doc in enumerate(result_sorted.keys()):
            d = Document.Document()
            d.setDocId(doc)
            docTitle = self.indexReader.getDocTitle(doc)
            d.setDocTitle(docTitle)
            d.setDocNo(self.indexReader.getDocLength(doc))
            d.setScore(result_sorted[doc])
            topk.append(d)
            if i == topN-1:
                break
        return topk

    # Save some variables
    def save(self):
        # f = open(, "w")
        with open(Path.Variables, 'w') as file:
            file.write('\n'.join(map(str, [self.number_docs, self.unique_word_count, self.csize])))
    
    # Load some variables
    def load(self):
        with open(Path.Variables, "r", encoding="utf-8") as g:
            data = list(map(int, g.readlines()))
        self.number_docs, self.unique_word_count, self.csize = data

