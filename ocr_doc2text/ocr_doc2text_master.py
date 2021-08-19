'''
Purpose: Converts scanned pdfs to machine readable text using doc2text

Links:
    original package: https://github.com/jlsutherland/doc2text
    forked package (updated for python3 compatability): https://github.com/mah427/doc2text

Notes: 
    This can be sed as a base for other OCR docments (just change contents of pdf folder)
    
TO DO:
    Modify code so that it does not automaticallty OCR the documents and only
    preprocesses the images to make the code more versatile
'''

import doc2text
from glob import glob 
import os
from pdf2image import convert_from_path

pdf_folder = os.path.join(os.getcwd(), 'pdf', '')

img_folder = os.path.join(os.getcwd(), 'temp', '')

text_folder = os.path.join(os.getcwd(), 'text', '')

#Create object of all pdf files
pdf_files = glob(pdf_folder +'/*.pdf')

for file in pdf_files:
    
    #Extract name from file:
    filename = file.split('.pdf')[0].split('/')[-1]
    
    print('Converting', filename + ' to images')
    
    #Convert pdf into image (each page becomes one image)
    images = convert_from_path(file, timeout=10000)
    temp_titles = []
    
    for index, image in enumerate(images):
        temp_title = 'out_' +str(index) + '.jpg'
        temp_titles.append(temp_title)
        images[index].save(img_folder + temp_title, 'JPEG')
    
    print(len(images), 'pages:' + 'starting ocr')
    
    #Convert each image into a doc2text class and ocr
    for title in temp_titles:
        
        #Initialized class
        doc = doc2text.Document()
        
        #Read in image
        doc.read(img_folder + title)
        
        #Crop, deskew, and optimize for OCR
        doc.process()
        
        #Extract text from the pages
        doc.extract_text()
        text = doc.get_text()
        with open(text_folder + filename + '.txt.', 'a+') as f:
            f.write(text)
        
        page = int(''.join([letter for letter in title if letter.isdigit()])) + 1
        
        print('Page', page, "completed")
        del doc
        
    #Clear out temporary image folder
    temp_files = glob(img_folder + '*')
    for f in temp_files:
        os.remove(f)
        
