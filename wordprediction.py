__author__ = 'joshua_sauder'


from prediction_lib import rsg, conf

# Read-in
data = {}
wordcount = 0
for i in conf.FILENAMES:
    print "Processing file", i
    infile = open(i)
    gen = conf.INPUTCLASS(infile)
    data, wordsread = rsg.build_dict(5, gen, data)
    wordcount += wordsread
print "%s total words processed" % wordcount

print '-'*60
sent = list(rsg.random_sentence(data, 5))[:-1]
print ' '.join([itm[0] for itm in sent])