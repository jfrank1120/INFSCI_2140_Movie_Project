
# uncompleted address of preprocessed corpus.
ResultHM1="data//result."
# ResultHM1="/archive2/has197/data/infsci/result."

# address of generated Text index file.
IndexTextDir="data//indextext//"

# address of generated Web index file.
IndexWebDir="data//indexweb//"

IndexWikiDir="data//indexwiki//"

# dataset dir
DatasetDir="data//wiki_movie_plots_deduped.csv"

# DB dir
DatabaseDir="data//wiki_movie_database.db"

# address of stopword list.
StopwordDir="data//stopword.txt"
Variables = "data//variables.txt"
TopicDir="data//topics.json"

# address of Stemmer
from nltk.stem.porter import PorterStemmer
Stemmer=PorterStemmer