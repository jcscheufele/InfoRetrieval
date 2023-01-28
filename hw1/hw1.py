# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object
# ########################################
import re
import glob
import cs547
import PorterStemmer

MY_NAME = "Joseph Scheufele"
MY_ANUM  = 361589387 # put your WPI numerical ID here
MY_EMAIL = "jcscheufele@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [ 
    ]

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs547.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # self._inverted_index = {
        #       'mike': [0,1],
        #       'football': [0],
        #       'sherman': [0],
        #       'cat': [1],
        #       'slept': [1]
        #       }
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        num_files_indexed = 0
        self._documents = glob.glob(base_path+"/*.txt")
        #self._documents = ['data\\00.txt', 'data\\10.txt']
        num_files_indexed = len(self._documents)

        for doc in self._documents:
            doc_num = int(doc.split("\\")[1].split(".")[0][1])-1
            with open(doc, 'r', encoding="UTF-8") as file:
                for line in file.readlines():
                    tokens = []
                    if line != '':
                        tokens = self.stemming(self.tokenize(line))
                    #print(tokens)
                    for token in tokens:
                        if token != '':
                            #print(token, self._inverted_index.keys())
                            if not(token in self._inverted_index.keys()):
                                self._inverted_index[token] = [doc_num]
                            else:
                                #print(self._inverted_index[token])
                                if not(doc_num in self._inverted_index[token]):
                                    self._inverted_index[token] = self._inverted_index[token] + [doc_num]

        #print(self._inverted_index)
        return num_files_indexed

    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        tokens = re.sub('[^0-9a-zA-Z]+', ' ', text.lower())
        #print(tokens, tokens.split())
        return tokens.split()

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        stemmed_tokens = []
        p = PorterStemmer.PorterStemmer()
        
        for token in tokens:
            #print(token)
            output = ''
            word = ''
            for i in range(len(token)):
                word += token[i].lower()
                #print("word", word)
            if word:
                #print(word)
                output += p.stem(word, 0,len(word)-1)
                #print("Out", output)
            #print(output)
            stemmed_tokens.append(output)
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        results = []
        queryTerms = []

        #print("search term", text)

        textTokens = self.tokenize(text)

        isAND = False
        isOR = False
        if "or" in textTokens:
            queryTerms = [i for i in textTokens if "or" not in i]
            isOR = True
        elif "and" in textTokens:
            queryTerms = [i for i in textTokens if "and" not in i]
            isAND = True
        else: 
            if " " in text:
                queryTerms = textTokens
            else:
                queryTerms = textTokens

        queryTerms = self.stemming(queryTerms)

        #print("Queryterms", queryTerms[0])

        keys = list(self._inverted_index.keys())

        #print("keys", keys)

        #print(isAND, isOR)

        if not (isAND or isOR):
            if queryTerms[0] in keys:
                #print('QueryTerms are found', queryTerms[0])
                #print(self._inverted_index[queryTerms[0]])
                results = [self._documents[i] for i in self._inverted_index[queryTerms[0]]]
        else:
            if isAND:
                if (queryTerms[0] in keys) and (queryTerms[1] in keys):
                    one = set(self._documents[i] for i in self._inverted_index[queryTerms[0]])
                    two = set(self._documents[i] for i in self._inverted_index[queryTerms[1]])
                    results = list(one.intersection(two))
            else:
                one = set()
                two = set()
                if (queryTerms[0] in keys):
                    one = set(self._documents[i] for i in self._inverted_index[queryTerms[0]])
                if (queryTerms[1] in keys):
                    two = set(self._documents[i] for i in self._inverted_index[queryTerms[1]])
                results = list(one.union(two))

        return results
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    num_files = index.index_dir('data/')
    print("indexed %d files" % num_files)
    for term in ('football', 'mike', 'sherman', 'mike OR sherman', 'mike AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

