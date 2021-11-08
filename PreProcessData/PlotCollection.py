from enum import auto
from typing import ChainMap
import Classes.Path as Path
import pandas as pd
import sqlalchemy as db
# from sqlalchemy import create_engine
import os
import re


# import mysql.co

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.

# FORMAT  = RELEASE YEAR, TITLE, ORIGIN, DIRECTOR, CAST, GENRE, WIKI-PAGE, PLOT
class PlotCollection:

    def __init__(self):
        # 1. Open the file in Path.DataTextDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.file = Path.DatasetDir
        self.file_obj = open(self.file)
        self.curr_idx = 1
        self.chunksize = 10 ** 6
        self.total_entries = 34886
        self.engine = db.create_engine('sqlite:///' + Path.DatabaseDir)
        self.connection = self.engine.connect()
        metadata = db.MetaData()
        self.movies = db.Table('table', metadata, autoload=True, autoload_with=self.engine)
        if not os.path.isfile(Path.DatabaseDir):
            self.populateDB()

        query = db.select([self.movies.columns.index, self.movies.columns.Title, self.movies.columns.Plot])
        self.ResultProxy = self.connection.execute(query)
        return

    def close(self):
        self.ResultProxy.close()
        return

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        # df = pd.read_sql("SELECT * FROM 'table' WHERE index={0}".format(self.curr_idx),con=self.db)
        # df = pd.read_sql("SELECT * FROM 'table' ORDER BY ReleaseYear LIMIT 1,{0}".format(self.curr_idx),con=self.db)
        # df = self.iterator.execute("SELECT * FROM 'table' ORDER BY ReleaseYear")

        # while True:
        partial_results = self.ResultProxy.fetchmany(1)
        if (partial_results == []):
            return None
        # print(partial_results[0])
        clean_content = re.sub('<[^<]+?>', '', partial_results[0][2])
        title = partial_results[0][1]
        clean_title = title.encode('ascii', 'ignore')
        return partial_results[0][0], clean_title.decode('utf-8'), clean_content

    def populateDB(self):
        i = 0
        j = 1
        for df in pd.read_csv(self.file, chunksize=self.chunksize, iterator=True):
            df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
            df.index += j
            i += 1
            df.to_sql('table', self.db, if_exists='append')
            j = df.index[-1] + 1

    def visualizeDataset(self):
        print(pd.read_csv(self.file, nrows=5))

    def visualizeDatabase(self):
        # df = pd.read_sql_query("SELECT * FROM 'table' ", con=self.db)
        # print(pd.read_sql_query("SHOW COLUMNS FROM 'table'", con=self.db))
        # print(pd.read_sql("SELECT * FROM 'table' WHERE ReleaseYear=1902", con=self.db))
        print(pd.read_sql("SELECT COUNT(*) FROM 'table'", con=self.db))
        # cursor = self.db.cursor()
        # print(cursor)
        # print(df.head(5))
