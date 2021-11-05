import Classes.Path as Path
from bisect import bisect_left

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class StopWordRemover:

    def __init__(self):
        # Load and store the stop words from the fileinputstream with appropriate data structure.
        # NT: address of stopword.txt is Path.StopwordDir.
        self.stopWordDir=Path.StopwordDir
        self.stopWords = sorted(self.readList())
        return

    def readList(self):
        words = []
        with open(self.stopWordDir, 'r') as f:
            for e in f:
                line = e.strip()
                words.append(line)
        return words

    def contains(self, word):
        return (word <= self.stopWords[-1]) and (self.stopWords[bisect_left(self.stopWords, word)] == word)

    def isStopword(self, word):
        # Return true if the input word is a stopword, or false if not.
        if self.contains(word):
            return True
        return False
