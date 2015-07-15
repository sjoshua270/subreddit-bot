from __future__ import generators
import re,string
        
class Metadata(object):
    def __init__(self, pos, tag):
        self.pos = pos
        self.tag = tag

EMPTY_METADATA = Metadata(('A00 0000', 42,42), None)

class ICAMEInput(object):
    """Looks like:
    A01 0010    The Fulton County Grand Jury said Friday an investigation
    A01 0020 of Atlanta's recent primary election produced "no evidence" that
    A01 0030 any irregularities took place.   The jury further said in term-end
    """
    def __init__(self, infile):
        self.infile = infile
    def __iter__(self):
        wordcount = 0
        for line in self.infile:
            posstr = " ".join(line.split()[:2])
            toks = line.split()[2:]
            for horizpos, tok in zip(range(len(toks)), toks):
                wordcount += 1
                yield tok, Metadata((posstr, horizpos, wordcount), None)
                if len(tok)>0 and tok[-1] == ".": #assume end of sentence
                    #Then begin a new sentence:
                    yield '#', EMPTY_METADATA

class TreebankTaggedInput(object):
    """Looks like:
        In/IN 
        [ American/JJ romance/NN ]
        ,/, almost/RB 
        [ nothing/NN ]
        rates/VBZ 
        [ higher/JJR ]
    """
    def __init__(self, infile):
        raise NotImplemented
    #    self.infile = infile
    #def __iter__(self):
    #    for line in self.infile:
    #        for tok in line.split():
    #            if '/' in tok:
    #                yield tok.split('/')[0]
    #            if tok == "./.":
    #                yield '#'
    #        
            
        
