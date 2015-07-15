from __future__ import generators

class Node:
    """Represents a bunch of possible next-words for one word-as-a-node
    Doesn't include the word itself; rather, it's associated with the word 
    in a key:value relationship elsewhere
    
    These only live as leafs at the bottom of the tree
    """
    def __init__(self):
        self.n = 0
        self.dict = {} #word : freq
        self.list = None
        self.metadata_dt = {} #word : metadatas
    def add_child(self, child, metadata):
        self.n += 1
        if self.dict.has_key(child):
            self.dict[child] += 1
            self.metadata_dt[child].append(metadata)
        else:
            self.dict[child] = 1
            self.metadata_dt[child] = [metadata]
        
    def finalize(self):
        self.list = []
        counter = 0
        for word, freq in self.dict.iteritems():
            counter += freq
            self.list.append((counter, word))
    def get_word(self, rand):
        n = rand * self.n
        if not self.list:
            self.finalize()
        item_bottom = 0
        item_top = len(self.list) - 1
        while item_top > item_bottom + 1:
            item_middle = (item_top + item_bottom) / 2
            if n < self.list[item_middle][0]:
                item_top = item_middle
            elif n > self.list[item_middle][0]:
                item_bottom = item_middle
            else:
                return self.list[item_middle][1]
        return self.list[item_top][1]

SENTENCE_DELIM= '#'

def build_dict(n, token_source, n_tuple_dict = None):
    """Will build upon the n_tuple_dict tree, and return a new, updated tree"""
    if not n_tuple_dict: n_tuple_dict = {}
    starting_ngram = [SENTENCE_DELIM for i in xrange(n)]

    count=0
    cur_ngram = starting_ngram
    for tok, metadata in token_source:
        count += 1
        cur_ngram   = cur_ngram[1:] + [tok]
        curnode     = n_tuple_dict

        for i in xrange(n - 1): #Populate the n-1-length path with {}'s and a Node
            if not curnode.has_key(cur_ngram[i]):
                if i == n - 2:
                    curnode[cur_ngram[i]] = Node()
                else:
                    curnode[cur_ngram[i]] = {}
            curnode = curnode[cur_ngram[i]]
        #curnode is now actually a node, not a dict
        curnode.add_child(cur_ngram[n - 1], metadata)
        if tok == SENTENCE_DELIM:
            cur_ngram = starting_ngram[:]
    return n_tuple_dict, count

def get_choosing_node(dict, sequence):
    """Traverses a sequence of words, length=n, down the tree.  It returns
    the bottom node, which is a Node node, that contains a probability table."""
    working = dict
    for i in xrange(len(sequence)):
        if working.has_key(sequence[i]):
            working = working[sequence[i]]
        else:
            raise Exception, "word " + sequence[i] + " in sequence can't be found"
    return working


import random
import time
random.seed(time.clock())

MAXWORDS=2056
def random_sentence(dict, n):
    """yields word, positionlist.  Uses the dict as the big tree, and n as
    the length of the n-gram"""
    startwith = [SENTENCE_DELIM for i in xrange(n-1)]
    newword = 'guten Tag'
    wordcount = 0
    while newword != SENTENCE_DELIM:
        endnode = get_choosing_node(dict, startwith)
        newword = endnode.get_word(random.random())
        
        if newword is SENTENCE_DELIM:
            yield ".", [('A00 0000', 0, 0)]
        else:
            poslist = [metadata.pos for metadata in endnode.metadata_dt[newword]]
            yield newword, poslist
            startwith = startwith[1:] + [newword]
        wordcount += 1
        if wordcount > MAXWORDS:
            yield ".", [('A00 0000', 0, 0)]
            break
            
