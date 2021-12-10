import Classes.Path as Path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.analysis import RegexTokenizer
import os
# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    writer=[]

    def __init__(self, type):
        path_dir= Path.IndexWikiDir
        # if type=="trectext":
        # path_dir = Path.IndexTextDir
        os.makedirs(path_dir, exist_ok=True)
        schema = Schema(doc_no=ID(stored=True),
                        doc_title=TEXT(analyzer=RegexTokenizer(), stored=True),
                        doc_content=TEXT(analyzer=RegexTokenizer(), stored=True)
                        )
                        # doc_url=ID(stored=True),
                        # doc_year=NUMERIC(stored=True),
                        # doc_origin=KEYWORD(stored=True),
                        # doc_genre=KEYWORD(stored=True)
                        # )
        indexing = index.create_in(path_dir, schema)
        self.writer = indexing.writer()
        return

    # This method build index for each document.
	# NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, value):
        self.writer.add_document(doc_no= value['docNo'],
                                 doc_title= value['title'],
                                 doc_content= value['content'])
                                #  doc_url= value['url'],
                                #  doc_year= value['year'],
                                #  doc_origin= value['origin'],
                                #  doc_genre= value['genre']
                                #  )
        return



    # Close the index writer,and you should output all the buffered content (if any).
    def close(self):
        self.writer.commit()
        return
