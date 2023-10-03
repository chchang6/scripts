#!/usr/bin/env python
# Script to read Endnote RIS export and
# 1. Create tab-delimited file of citation data
# 2. Copy PDF file from current location to folder with relative path
#    from sheet
# 3. Create hyperlink to file in new field

import sys
from os import mkdir
from os.path import isdir

class Reference:
   def __init__(self):
      self.authors = [] # AU in RIS
      self.title = '' # TI in RIS
      self.year = None # PY
      self.category = None # LB; M3 if LB not defined
      self.PDFlink = None # L1; replace with link to PDF
      self.DOI = None
      self.URL = None # UR
   def add_author(self, author_string):
      self.authors.append(author_string)
   def add_title(self, title_string):
      self.title = title_string
   def add_year(self, year_int):
      self.year = year_int
   def add_category(self, category_string):
      self.category = category_string
   def add_PDFlink(self, path_string):
      self.PDFlink = path_string
   def add_DOI(self, DOI_string):
      self.DOI = DOI_string
   def add_URL(self, URL_string)
      self.URL = URL_string)
   def get_authors(self):
      return iter(self.authors)
   def get_title(self):
      return self.title
   def get_year(self):
      return self.year
   def get_category(self):
      return self.category
   def get_PDFlink(self):
      return self.PDFlink
   def get_DOI(self):
      return self.DOI
   def get_URL(self):
      return self.URL

class Journal_Article(Reference):
   def __init__(self):
      self.type = 'journal article'
      self.source = '' # T2
      self.volume = 0 # VL
      self.issue = 0 # M1
      self.pages = None # SP; replace with tuple for begin and end
   def add_source(self, source_string):
      self.source = source_string
   def add_volume(self, volume_int):
      self.volume = volume_int
   def add_issue(self, issue_string):
      self.issue = issue_string
   def add_pages(self, pages_tuple):
      self.pages = pages_tuple
   def get_source(self):
      return self.source
   def get_volume(self):
      return self.volume
   def get_issue(self):
      return self.issue
   def get_pages(self):
      return self.pages

class Book(Reference):
   def __init__(self):
      self.type = 'book'
      self.volume = 0 # VL
      self.editors = [] # A2
      self.booktitle = '' # T2
      self.place_published = None # CY
      self.publisher = None # PB
      self.ISBN = None # SN, if book
   def add_volume(self, volume_int):
      self.volume = volume_int
   def add_editor(self, ed_string):
      self.editors.append(ed_string)
   def add_title(self, title_string):
      self.booktitle = title_string
   def add_pubplace(self, place_string):
      self.place_published = place_string
   def add_publisher(self, publisher_string):
      self.publisher = publisher_string
   def add_ISBN(self, ISBN_string):
      self.ISBN = ISBN_string
   def get_volume(self):
      return self.volume
   def get_editor(self):
      return self.editors
   def get_title(self):
      return self.booktitle
   def get_pubplace(self):
      return self.place_published
   def get_publisher(self):
      return self.publisher
   def get_ISBN(self):
      return self.ISBN

class Book_Section(Book):
   def __init__(self):
      self.type = 'book chapter'
      self.pages = None # SP; replace with tuple for begin and end
      self.chapter = None # SE
   def add_pages(self, page_tuple):
      self.pages = page_tuple
   def add_chapter(self, chapter_string):
      self.chapter = chapter_string
   def get_pages(self):
      return self.pages
   def get_chapter(self):
      return self.chapter

class Government_Document(Reference):
   def __init__(self):
      self.type = 'government document'
      self.department = None # A2 in GOVDOC
      self.pages = None # SP; might mean total or range

class Conference_Paper(Reference):
   def __init__(self):
      self.type = 'conference paper'
      self.location = None # CY
      self.conference_name = None # T2
      self.publisher = None # PB

class Conference_Proceedings(Reference):
   def __init__(self):
      self.type = 'conference proceedings'
      self.authors = [] # AU in CONF
      self.editors = [] # A2 in CONF
      self.confname = None # T2 in CONF
      self.confloc = None # CY in CONF
      self.publisher = None # PB in CONF
      self.ISBN = None # SN in CONF
   def add_author(self, author_string):
      self.authors.append(author_string)
   def add_editor(self, ed_string):
      self.editors.append(ed_string)
   def add_conference_name(self, name_string):
      self.confname = name_string
   def add_conference_location(self, location_string):
      self.confloc = location_string
   def add_publisher(self, publisher_string):
      self.publisher = publisher_string
   def add_ISBN(self, ISBN_string):
      self.ISBN = ISBN_string
   def get_author(self):
      return self.authors
   def get_editor(self):
      return self.editors
   def get_conference_name(self):
      return self.confname
   def get_conference_location(self):
      return self.confloc
   def get_publisher(self):
      return self.publisher
   def get_ISBN(self):
      return self.ISBN

def parse(reflist):
   test = [i.strip() for i in reflist[0].split('-')]
   parsing_function = ref_parse[test]
   parsed_ref = parsing_function(reflist)
   return parsed_ref

refs = []
ref_parse = { 	'JOUR': parse_journal,
		'CHAP': parse_chapter,
		'CPAPER': parse_conf_paper,
		'CONF': parse_conf_proc,
		'FIGURE': parse_figure,
		'GOVDOC': parse_govdoc}

ref_types = { 'JOUR': 'journal article', 
              'CHAP': 'book chapter',
              'CPAPER': 'conference paper',
              'CONF': 'conference proceeding',
              'FIGURE': 'figure',
              'GOVDOC': 'government document'}

with open(sys.argv[1], 'r') as data:
   for line in data:

# To find PDFs, assume that the Endnote library name is sys.argv[1] without the '.txt' extension
library = sys.argv[1][0:-4]
source_PDFlink_prefix = '/Users/cchang/Documents/Endnote/' + library + '.enlp/' + library + '.Data/PDF/'
target_PDFlink_prefix = '/Users/cchang/Documents/References/' + library + '/'

# Parse
for line in iter(file.readline, ''):
   if line[0:2] == 'TY': # Start block
      data = []
   elif line[0:2] == 'ER': # End block
      refs.append(parse(data))
   elif len(line) < 2: # Just newline
      continue
   else:
      data.append(line)

# Create folders to hold PDFs
for i in refs:
   if i.get_PDFlink():
      if i.get_category():
         t2 = i.get_category()
         target_PDF_path = target_PDFlink_prefix + t2
         if not isdir(target_PDFlink_prefix + t2):
            mkdir(target_PDFlink_prefix + t2)


