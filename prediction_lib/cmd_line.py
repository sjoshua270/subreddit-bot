#!/sw/bin/python
#by Martin Kay
"""comand_line class parses command-line switches and returns
   a dictionary containing their values plus the remainder of
   the command line.

   call: comand_line(self, h_switch='', h_string='', lg=[], \
                     nd=[], ags=sys.argv[1:])

   Parameters of the object can be changed after it is created
   using the methods:
     help_switch(s):
     help_string(s):
     long(l):
     needs(n):
     args(a):
     default(d):

   The help switch, if supplied, is a single character which, if it
   is supplied as a switch, causes the program to exit having
   displayed the help string.

   Switch values are retrieved by calling
   comand_line.switch(self, switch_name, [default]).

   If a switch does not have an explicit value, it is given the value
   '-'.

   If a switch is not supplied, but its value is called for, The default is
   returned, or None if no default is supplied.

   The name of each switch is preceded by '-' and the first item
   that might otherwise be interpreted as a switch marks the end of
   the list of switches.  Single character switches with default values
   can be collected in a single word. The syntax of the list is
   determined by the 'long' and 'needs' list as in the following examples:
     Input       Output         Conditions
     -----       ------         ----------
     -abc        {alpha: None}  abc in long but not needs
     -abc beta   {alpha: beta}  abc in needs
     -abc        {a: None, b: None, c: None}
                                abc in neithr long nor needs
     -abc=beta   {alpha: beta}  long and needs irrelevant. No
                                spaces flanking '='
   Repetions of switches override values assigned to them ealier.

   Called as a program, it can be used to show what would be returned
   under particular circumstances, by supplying suitable value for the
   parameters 'long', 'needs' and 'args'.

   Examples:
     cmd_line.py -a -b -pq foo fie
     flags.avs =  {'a': '-', 'p': '-', 'b': '-', 'q': '-'}
     flags.rest() =  ['foo', 'fie']

     cmd_line.py -args='-a -b -pq foo fie'
     flags.avs =  {'a': '-', 'p': '-', 'b': '-', 'q': '-'}
     rest.rest() =  ['foo', 'fie']

     cmd_line.py -args='-a -b -pq foo fie' -long='pq rs'
     flags.avs =  {'a': '-', 'pq': '-', 'b': '-'}
     rest.rest() =  ['foo', 'fie']

     cmd_line.py -args='-a -b -pq foo fie' -needs='pq rs'
     flags.avs =  {'a': '-', 'pq': 'foo', 'b': '-'}
     rest.rest() =  ['fie']

"""

class command_line(object):

  import sys
  import string
  import re

  eq=re.compile('\s*=\s*')

  def __init__(self, h_switch='', h_string='', lg=[], \
               nd=[], ags=sys.argv[1:]):
    self.help_switch(h_switch)
    self.help_string(h_string)
    self.long(lg)
    self.needs(nd)
    self.args(ags)
    command_line.avs={}
    command_line.default_value='-'

  def help_switch(self, s):
    self.h_switch=s

  def help_string(self, s):
    self.h_string=s

  def long(self, l):
    self.lg=l

  def needs(self, n):
    self.nd=n

  def args(self, a):
    self.ags=a

  def default(self, d):
    self.default_value=d

  def read(self, args=None):
    if args==None: args=self.ags
    while args and args[0][0]=='-':
      arg, args = args[0][1:], args[1:]
      if not arg: arg='-'
      av=self.eq.split(arg, 1)
      length=len(av)
      if length==1:
         if arg in self.nd:
            self.avs[arg]=args[0]
            args = args[1:]
         elif arg in self.lg:
            self.avs[arg] = self.default_value
         else:
            for i in arg:
              if i==self.h_switch:
                 print self.h_string
                 command_line.sys.exit(0)
              self.avs[i]=self.default_value
      else:
        self.avs[av[0]]=av[1]
    self.ags=args

  def switch(self, s, default=None):
    try: return self.avs[s]
    except KeyError: return default

  def on(self, s):
    try:
      if self.avs[s]:
        return 1
    except KeyError:
      pass
    return 0

  def rest(self):
    return self.ags

if __name__ == '__main__':
  import os
  flags = command_line('h', __doc__, [], [])
  flags.read()
  long = flags.switch('long')
  if long:
    long=long.split()
  else: long=[]
  needs = flags.switch('needs')
  if needs:
    needs=needs.split()
  else:  needs=[]
  args=flags.switch('args')
  if(args):
    args = os.popen('echo ' + args).read().split()
    new_flags = command_line('h', __doc__, long, needs)
    new_flags.read(args)
    print 'flags.avs = ', new_flags.avs
    print 'rest.rest() = ' , new_flags.rest()
  else:
    print 'flags.avs = ', flags.avs
    print 'flags.rest() = ' , flags.rest()
