# homework 4
# goal: ranked retrieval, PageRank, crawling
# exports:
#   student - a populated and instantiated cs547.Student object
#   PageRankIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents and providing a
#     ranked result set

# ########################################
# first, create a student object
# ########################################

import re
import cs547
MY_NAME = "Joseph Scheufele"
MY_ANUM  = 361589387 # put your UID here
MY_EMAIL = "jcscheufele@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = []

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "An Aggie does not lie, cheat or steal, or tolerate those who do."
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

from bs4 import BeautifulSoup as bs  # you will want this for parsing html documents
from urllib.request import urlopen
import numpy as np

# our index class definition will hold all logic necessary to create and search
# an index created from a web directory
#
# NOTE - if you would like to subclass your original Index class from homework
# 1 or 2, feel free, but it's not required.  The grading criteria will be to
# call the index_url(...) and ranked_search(...) functions and to examine their
# output.  The index_url(...) function will also be examined to ensure you are
# building the index sanely.

class PageRankIndex(object):
    def __init__(self):
        # you'll want to create something here to hold your index, and other
        # necessary data members
        self.root = ""
        self.web = {}
        self.index = {}
    
    
    def _crawler(self, root):
        soup = bs(urlopen(root), 'html.parser')
        anchors = soup.find_all('a')
        linkNums = []
        for anchor in anchors:
            number = int(str(anchor.string).split(".")[0].split("_")[1])
            linkNums.append(number)
        return linkNums
        

    # index_url( url )
    # purpose: crawl through a web directory of html files and generate an
    #   index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: use BeautifulSoup and urllib
    # parameters:
    #   url - a string containing a url to begin indexing at
    def index_url(self, url):
        self.root = url.replace("index.html", "")
        #print(f"Root: {self.root}")
        soup = bs(urlopen(url), 'html.parser')
        anchors = soup.find_all('a')
        for anchor in anchors:
            link = str(anchor.get('href'))
            #print(f"Link: {link}")
            if link not in self.web.keys():
                self.web[link] = [self._crawler(self.root+link), 0]
        # ADD CODE HERE
        #print(self.web)

        p = np.zeros((len(anchors), len(anchors)))
        t = np.ones((len(anchors), len(anchors))) * .1

        for i in range(len(anchors)):
            links = self.web[f"d_{i}.html"][0]
            for link in links:
                #print("LINK", link)
                #print(p[i, link])
                p[i, link] = 1/len(links)

        #print(p)

        P = .9*p + .1*t

        #print(P)

        err = 1000
        xPrev = np.zeros(len(anchors))
        xPrev[0] = 1
        iteration = 0
        while err > 1e-10/len(anchors):
            #print("Iteration: ", iteration)
            #print("xPrev: ", xPrev)
            xNext = xPrev.dot(P)
            #print("xNext: ", xNext)
            err = np.sum(np.subtract(xNext, xPrev)**2)
            #print("Error: ", err)
            iteration += 1
            xPrev = xNext

        for i in range(len(anchors)):
            self.web[f'd_{i}.html'][1] = xPrev[i]
            
        #print(self.web)

        for key in self.web.keys():
            number = int(key.split(".")[0].split("_")[1])
            soup = bs(urlopen(self.root+key), 'html.parser')
            text = soup.get_text()
            tokens = self.tokenize(text)
            for token in tokens:
                if token not in self.index.keys():
                    self.index[token] = [number]
                elif number not in self.index[token]:
                    self.index[token].append(number)

        #print(self.index)

        return len(anchors)

    # tokenize( text )
    # purpose: convert a string of terms into a list of terms 
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        tokens = re.sub('[^0-9a-zA-Z]+', ' ', text.lower())
        #print(tokens, tokens.split())
        return tokens.split()

    # ranked_search( text )
    # purpose: searches for the terms in "text" in our index and returns
    #   AND results for highest 10 ranked results
    # preconditions: .index_url(...) has been called on our corpus
    # returns: list of tuples of (url,PageRank) containing relevant
    #   search results
    # parameters:
    #   text - a string of query terms
    def ranked_search(self, text):
        tokens = self.tokenize(text)
        docs = []

        for token in tokens:
            docs.append(set(self.index[token]))
            
        # ADD CODE HERE
        
        results = []
        finalDocs = set.intersection(*docs)
        #print("Results: ", finalDocs)

        for doc in finalDocs:
            score = self.web[f"d_{doc}.html"][1]
            results.append((self.root+f"d_{doc}.html", score))

        results.sort(key = lambda x: x[1], reverse=True)

        return results[:10]


# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = PageRankIndex()
    url = 'http://web.cs.wpi.edu/~kmlee/cs547/new10/index.html'
    num_files = index.index_url(url)
    search_queries = (
       'palatial', 'college ', 'palatial college', 'college supermarket', 'famous aggie supermarket'
        )
    for q in search_queries:
        results = index.ranked_search(q)
        print("searching: %s -- results: %s" % (q, results))


# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

