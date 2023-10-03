#!/usr/bin/env python
# Script to parse text file from OBO, build class document, and rewrite as an XML file.  CHC 6/25/10

import sys
import re

class term:
   def __init__(self):
      self.id = ''
      self.name = ''
      self.namespace = ''
      self.definition = ''
      self.subset = ''
      self.comment = ''
      self.relationships = []
      self.alternative_ids = []
      self.synonyms = []
   def set_id(self, id_string):
      temp = id_string.split(':', 1)
      self.id = temp[1].strip()
   def set_name(self, name_string):
      temp = name_string.split(':', 1)
      self.name = temp[1].strip()
   def set_namespace(self, ns_string):
      temp = ns_string.split(':', 1)
      self.namespace = temp[1].strip()
   def set_definition(self, def_string):
      temp = def_string.split(':', 1)
      self.definition = re.search(r'\".+\"', def_string).group(0)
   def set_subset(self, subset_string):
      temp = subset_string.split(':')
      self.subset = temp[1].strip()
   def add_synonym(self, syn_string):
      temp = syn_string.split(':', 1)
      syn = re.search(r'\".+\"', temp[1]).group(0)
      self.synonyms.append(syn)
   def add_alternative_id(self, id_string):
      temp = id_string.split(':', 1)
      self.alternative_ids.append(temp[1])
   def add_relationship(self, rstring):
      temp = rstring.split(':', 1)
      if re.match('relationship', temp[0]):
         temp2 = temp[1].split()
         rel = temp2[0]
         term = temp2[1]
      elif re.match('is_a', temp[0]):
         temp2 = temp[1].split()
         rel = 'is_a'
         term = temp2[0]
      self.relationships.append( (rel, term) )
      return (rel, term)
   def add_comment(self, com_string):
      temp = com_string.split(':', 1)
      self.comment = temp[1]
   def get_id(self):
      return self.id
   def get_name(self):
      return self.name
   def get_namespace(self):
      return self.namespace
   def get_definition(self):
      return self.definition
   def get_subset(self):
      return self.subset
   def get_relationships(self):
      return self.relationships

def parse_subsetdef(string):
   temp = string.split(':', 1)
   term = re.search(r'\A([^"])+', temp[1]).group(0).strip()
   definition = re.search(r'\".+\"', temp[1]).group(0).strip()
   return (term, definition)

def parse_term(string, redict):
   if re.search('is_obsolete: true', string):
      return None
   else:
      temp = string.split('\n')  # Assume main passes in a multi-line pattern
      thisterm = term()
      for i in temp:
         if redict[2].match(i): thisterm.set_id(i)
         elif redict[3].match(i): thisterm.set_name(i)
         elif redict[4].match(i): thisterm.set_namespace(i)
         elif redict[5].match(i): thisterm.set_definition(i)
         elif redict[6].match(i): thisterm.set_subset(i)
         elif redict[7].match(i) or redict[8].match(i): thisterm.add_relationship(i)
         elif redict[9].match(i): thisterm.add_comment(i)
         elif redict[10].match(i): thisterm.add_alternative_id(i)
         elif redict[11].match(i): thisterm.add_synonym(i)
      return thisterm

REdict = { \
1 : re.compile('subsetdef'), \
2 : re.compile('id'), \
3 : re.compile('name'), \
4 : re.compile('namespace'), \
5 : re.compile('def'), \
6 : re.compile('subset'), \
7 : re.compile('relationship'), \
8 : re.compile('is_a'), \
9 : re.compile('comment'), \
10 : re.compile('alt_id'), \
11 : re.compile('synonym'), \
12 : re.compile('\[Term\]') }

infile = open(sys.argv[1], 'r')
data = infile.readlines()
infile.close()

subset_definitions = {}
termlist = []

i = 0  # Main index
j = 0  # End index for term boundary
termstring = ''
while i < len(data):
   temp = data[i]
   if REdict[1].match(temp):
      x = parse_subsetdef(temp)
      subset_definitions[x[0]] = x[1]
   elif REdict[12].match(temp):
      termstring = ''
      j = i + 1
      while True:
         termstring += data[j]
         if data[j] == '\n' or (j + 1 == len(data)):
            i = j
            break
         else:
            j+=1
      termlist.append(parse_term(termstring, REdict))
   i += 1

# Testing
print len(termlist)
