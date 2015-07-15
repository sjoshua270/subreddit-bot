#This must be import'able python code.

#Each must be a list of filenames to read in.
import glob
big = glob.glob(
    "big.txt")

import inputclasses
FILENAMES = big
INPUTCLASS = inputclasses.ICAMEInput
#FILENAMES = tagged
#INPUTCLASS = inputclasses.TreebankTaggedInput
