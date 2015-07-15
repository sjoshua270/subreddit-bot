#!/usr/local/bin/python -i

"""Usage

-n num      n-gram length (default 3)
"""
from cmd_line import command_line
import sys
import os
import rsg
import conf
import inputclasses
import pprint


def num_cbreaks(sent):
    """Counts the number of continuity breaks in the given sentence.

    sent: list of (word, its position list)
    """
    breaks = 0
    for i in range(length, len(sent)):

        end_of_prev_ngram = sent[i-1]
        word,posls = end_of_prev_ngram
        prev_absolute_wordpositions = [pos[2] for pos in posls]

        end_of_ngram = sent[i]
        word, posls = end_of_ngram
        cur_absolute_wordpositions = [pos[2] for pos in posls]

        for cur_absolute_wordpos in cur_absolute_wordpositions:
            if cur_absolute_wordpos - 1 in prev_absolute_wordpositions:
                break #No continuity break!
        else:
            breaks += 1
            #print "%-25s: Continuity break -----" %word
    return breaks
    

def do_stats(num_sents, benchmarkincr=.05, status=1):
    """Generates a lot of sentences, and displays statistical info
    
    num_sents: number of sentences to run the analysis on
    benchmarkincr: for progress indicator
    status: boolean, whether or not to show the progress indicator
    """
    global length
    total_breaks = 0
    total_words = 0
    total_nobreaks = 0
    lastbenchmark = 0.0
    for i in xrange(num_sents):
        if status:
            if 1.0 * i / num_sents > lastbenchmark + benchmarkincr:
                print "%d%% done, %d sentences analyzed" %(100.0 * i / num_sents, i)
                lastbenchmark += benchmarkincr
        sent = list(rsg.random_sentence(data, length))[:-1]
        num_breaks = num_cbreaks(sent)
        if num_breaks == 0: total_nobreaks += 1
        total_breaks += num_breaks
        total_words  += len(sent)
    avg_words_per_sent   = total_words * 1.0 / num_sents
    avg_breaks_per_sent = total_breaks * 1.0 / num_sents
    breaks_per_word      = total_breaks * 1.0 / total_words
    perc_total_nobreaks  = total_nobreaks *1.0 / num_sents
    print "------------------- Results -----------------------"
    allvars = locals(); allvars.update(globals())
    print """
length=%(length)s
num_sents=%(num_sents)s
perc_total_nobreaks=%(perc_total_nobreaks)s #Straight-copied sentences; indicator of sparseness
avg_words_per_sent=%(avg_words_per_sent)s
avg_breaks_per_sent=%(avg_breaks_per_sent)s
breaks_per_word=%(breaks_per_word)s
""" % allvars

def show(linetag):
    """hard-coded to work with the ICAME-Brown1 corpus on the leland systems"""
    fgrepable_linetags = linetag
    s = os.popen("fgrep --no-filename -C 10 '%s' /afs/ir/data/linguistic-data/Brown/ICAME-Brown1/*" %fgrepable_linetags).read().replace('\n', ' \n')
    s = s.replace(linetag, '\001%s\033[31m%s\033[0m\002' %(ANSIBOLD,linetag))
    return s

def clines(linetags):
    """hard-coded to work with the ICAME-Brown1 corpus on the leland systems"""
    fgrepable_linetags = '\n'.join(linetags)
    return os.popen("fgrep --no-filename '%s' /afs/ir/data/linguistic-data/Brown/ICAME-Brown1/*" %fgrepable_linetags).read().replace('\n', ' \n')


## ---------------------   Begin "main" area -----------------------------
flags = command_line('h', __doc__, [], ['n'])
flags.read()

strlen = flags.switch('n')
if strlen:  length = int(strlen)
else:       length = 3

# Read-in
data = {}
wordcount = 0
for i in conf.FILENAMES:
    print "Processing file", i
    infile = open(i)
    gen = conf.INPUTCLASS(infile)
    data, wordsread = rsg.build_dict(length, gen, data)
    wordcount += wordsread
print "%s total words processed" %wordcount

ANSIBOLD=os.popen("tput bold").read()

print "h for help.  Control-D to exit"

while 1:
    opt = raw_input("? ")
    if opt=='h':
        print """
[Enter]=new sentence;  
s=show sentence;
a=all positions; 
c=context positions; 
b=continuity analysis"""

    elif opt=='s':
        print ' '.join([itm[0] for itm in sent])
    elif opt=='a':
        pprint.pprint(sent) 
    elif opt=='c':
        for i, (w, posls) in zip(range(len(sent)), sent):
            print "%s) %s "%(i,w)
            linetags = [pos[0] for pos in posls]
            ctxtlines = clines(linetags)
            s = ctxtlines
            s = '\t' + s.strip().replace('\n','\n\t') + '\n'
            s = s.replace(" %s " %w, '\001%s\033[31m %s \033[0m\002' %(ANSIBOLD,w))
            print s,
        print
    elif opt=='b':
        words = [w for w,posls in sent]
        
        breaks = 0
        for i in range(0,length):
            end_of_ngram = sent[i]
            word, posls = end_of_ngram
            print "%-25s: n/a" %word
        for i in range(length, len(sent)):

            end_of_prev_ngram = sent[i-1]
            word,posls = end_of_prev_ngram
            prev_absolute_wordpositions = [pos[2] for pos in posls]

            end_of_ngram = sent[i]
            word, posls = end_of_ngram
            cur_absolute_wordpositions = [pos[2] for pos in posls]

            for cur_absolute_wordpos in cur_absolute_wordpositions:
                if cur_absolute_wordpos - 1 in prev_absolute_wordpositions:
                    print "%-25s: continuous.." %word
                    break #No continuity break!
            else:
                print "%-25s: Continuity break over the n-1-gram: %s " \
                        %(word, words[i-(length-1):i])
    elif opt=='':
        print '-'*60
        sent = list(rsg.random_sentence(data, length))[:-1]
        print ' '.join([itm[0] for itm in sent])
    else:
        #read-eval-print loop by default
        print eval(opt)
