import Classes.Path as Path
import re
# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class WordTokenizer:

    def __init__(self, content):
        # Tokenize the input texts.
        self.result = self.tokenize(content, 'words')
        # Maintain index, to send the next word
        self.idx = 0
        return

    def tokenize(self, content, criteria):
        if criteria == 'words':
            words = []
            # Remove punctuation and spaces by replacing it with a single space
            clean = re.sub(r"""
               [-'",.;@#?!&$]+
               \ *           
               """,
               " ",          
               content, flags=re.VERBOSE)
            words_ = re.findall(r"\w+|[^\w\s]+",clean)
            for w in words_:
                if w:
                    words.append(w)
        else:
            raise NotImplementedError('Specified criteria not implemented yet.')
        return words

    def nextWord(self):
        # Return the next word in the document.
        # Return null, if it is the end of the document.
        try:
            word = self.result[self.idx]
            self.idx = self.idx + 1
            return word
        # when no words are left, return None
        except IndexError:
            return None
