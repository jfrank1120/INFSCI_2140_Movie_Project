import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class WordNormalizer:

    def __init__(self):
        self.stemmer = Path.Stemmer()
        return

    def lowercase(self, word):
        # Transform the word uppercase characters into lowercase.
        return word.lower()

    def stem(self, word):
        # Return the stemmed word with Stemmer in Classes package.
        return self.stemmer.stem(word)
