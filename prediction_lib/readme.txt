Random Sentence Generator with n-grams

Michael Bieniosek and Brendan O'Connor

More information at 
<http://www.stanford.edu/~brendano/ling138/rsg-project.html>

To run:

1) Edit conf.py to give you the files in your corpus, and select the right
reader.  It's currently set up for the untagged ICAME Brown corpus for the
Leland machines at Stanford.  

2) Run main.py.  It'll process the corpus, create the probability tree,
and then give you the prompt so you can make it spit out sentences, and
also introspect their origins.

Note that some functions, like introspection, are hard-coded to use the
untagged ICAME corpus.  grep ICAME *.py  should show you all the places where
that is true.

present/ has a few files we used for our in-class presentation.
old/ has, well, old files that aren't used anymore.

That's it!  Have fun!
