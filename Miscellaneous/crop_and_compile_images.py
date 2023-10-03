#!/usr/bin/env python

import glob, os
import re
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from sys import exit
from datetime import datetime as dt

def filename_transform(match_object):
   if match_object.group('AMPM') == 'P' and int(match_object.group('hour')) != 12:
      hour = int(match_object.group('hour')) + 12
   elif match_object.group('AMPM') == 'A' and int(match_object.group('hour')) == 12:
      hour = 0
   else:
      hour = int(match_object.group('hour'))
   output_filename = match_object.group('year') + match_object.group('month') + match_object.group('day') + '_' + \
                     f'{hour:02d}' + match_object.group('minute') + match_object.group('second') + '.png'
   return output_filename

def filefilter(start_dt, end_dt, file_list):
   # Inclusive to select range of files
   new_list = []
   for i in file_list:
      if RE2.match(i):
         j = filename_transform(RE2.match(i))
      else:
         j = i
      assert RE1.match(j)
      t = dt.strptime(j, '%Y%m%d_%H%M%S.png')
      if (t >= start_dt) and (t <= end_dt):
         new_list.append((i, j))
   return(sorted(new_list, key=lambda x: x[1]))

def remove_files(filelist):
   for i in filelist:
      os.remove(i)
   return

def pdf_cat(input_files, output_stream):
    input_streams = []
    try:
        # First open all the files, then produce the output file, and
        # finally close the input files. This is necessary because
        # the data isn't read from the input files until the write
        # operation. Thanks to
        # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733
        for input_file in input_files:
            input_streams.append(open(input_file, 'rb'))
        writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(output_stream)
    finally:
        for f in input_streams:
            f.close()

RE1 = re.compile('[0-9]{8}_[0-9]{6}.png')
RE2 = re.compile('Screen Shot (?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}) at (?P<hour>[0-9]{1,2})\.(?P<minute>[0-9]{2})\.(?P<second>[0-9]{2}) (?P<AMPM>[AP])')
# For testing crop window
#png_filelist=['20201016_155516.png']
#pdf_outfile = open('20201015_112305.pdf', 'wb')
# Production
action = 'compile' # One of "crop", "compile", or "cropandcompile"
png_filelist=glob.glob('*.png')
start_dt = dt(2021, 5, 28, 12, 42, 44)
end_dt = dt(2021, 5, 28, 13, 00, 12)
png_filelist = filefilter(start_dt, end_dt, png_filelist)
pdf_outfile = open('May282021_Wipke.pdf', 'wb')
pdf_filelist = []

# Production
if 'crop' in action:
    crop_from_top = 100
    crop_from_left = 0
    symmetric = True
    if symmetric:
       crop_from_bottom = crop_from_top
       crop_from_right = crop_from_left
    else:
       crop_from_bottom = 100
       crop_from_right = 240
else:
    crop_from_top = 0
    crop_from_left = 0
    crop_from_bottom = 0
    crop_from_right = 0

for i in png_filelist:
    if 'crop' in action:
        im = Image.open(i[0])
        im2 = im.crop((0 + crop_from_left, 0 + crop_from_top, im.width - crop_from_right, im.height - crop_from_bottom))
        cropped_name = i[1]
        cropped_name = re.sub('\.png', '_cropped.png', i[1])
        im2.save(cropped_name)
        if action == 'cropandcompile':
            im3 = im2.convert('RGB')
            im3 = Image.open(cropped_name)
            im3outname = re.sub('\.png', '.pdf', i[1])
            im3.save(im3outname)
    else:
        im = Image.open(i[0])
        im3 = im.convert('RGB')
        im3outname = re.sub('\.png', '.pdf', i[1])
        im3.save(im3outname)
    #exit()
    pdf_filelist.append(im3outname)

print(pdf_filelist)
pdf_cat(pdf_filelist, pdf_outfile)

#remove_files(png_filelist)
remove_files(pdf_filelist)

