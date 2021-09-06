'''
Author:
    Martin Hiti
    
Last Update:
    8/20/2021: converted script into function (see bellow)
    
Purpose: 
    Converts scanned pdfs to machine readable text using doc2text. 
         
    The section of the code that is commented out is the old script used
    to test the functionality of doc2text. The second half, which is not
    commented out contains a function for OCR'ing files which can be uded
    on any file level data set.

Links:
    original package: https://github.com/jlsutherland/doc2text
    forked package (updated for python3 compatability): https://github.com/mah427/doc2text

Notes: 
    This can be sed as a base for other OCR docments (just change contents of pdf folder)
    
To Do:
    [] Modify code so that it does not automaticallty OCR the documents and only
    preprocesses the images to make the code more versatile
'''

import doc2text
from glob import glob 
import os
from pdf2image import convert_from_path

pdf_folder = os.path.join(os.getcwd(), 'pdf', '')

img_folder = os.path.join(os.getcwd(), 'temp', '')

text_folder = os.path.join(os.getcwd(), 'text', '')

# =============================================================================
# #Create object of all pdf files
# pdf_files = glob(pdf_folder +'/*.pdf')
# 
# for file in pdf_files:
#     
#     #Extract name from file:
#     filename = file.split('.pdf')[0].split('/')[-1]
#     
#     print('Converting', filename + ' to images')
#     
#     #Convert pdf into image (each page becomes one image)
#     images = convert_from_path(file, timeout=10000)
#     temp_titles = []
#     
#     for index, image in enumerate(images):
#         temp_title = 'out_' +str(index) + '.jpg'
#         temp_titles.append(temp_title)
#         images[index].save(img_folder + temp_title, 'JPEG')
#     
#     print(len(images), 'pages:' + 'starting ocr')
#     
#     #Convert each image into a doc2text class and ocr
#     for title in temp_titles:
#         
#         #Initialized class
#         doc = doc2text.Document()
#         
#         #Read in image
#         doc.read(img_folder + title)
#         
#         #Crop, deskew, and optimize for OCR
#         doc.process()
#         
#         #Extract text from the pages
#         doc.extract_text()
#         text = doc.get_text()
#         with open(text_folder + filename + '.txt.', 'a+') as f:
#             f.write(text)
#         
#         page = int(''.join([letter for letter in title if letter.isdigit()])) + 1
#         
#         print('Page', page, "completed")
#         del doc
#         
#     #Clear out temporary image folder
#     temp_files = glob(img_folder + '*')
#     for f in temp_files:
#         os.remove(f)
# =============================================================================

def ocr_files(df, input_folder):
    '''
    Inputs: file level data frame (from scraping folder)
            input_folder: folder where raw files (pdf) are stores
            
    Output: Data frame with new column, "Raw Text" which contains the machine
            readable text of the file
    '''
    #Create empty variable to be filled with text
    df["Raw Text"] = ""
    
    #Create folders (if the do note already exist)
    img_folder = os.path.join(os.getcwd(), "temp", '')  #Temporary folder
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
        
    text_folder = os.path.join(os.getcwd(), "text", '') #Text to be stored here
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
    
    #Iterate through each file in the dataframe
    for ind in df.index:
        
        #Create full path to file
        file = os.path.join(input_folder, df['Filename'][ind])
        
        #Extract name from file:
        if '.docx' in file:
            filename = file.split('.docx')[0].split('/')[-1]
        else:
            filename = file.split('.pdf')[0].split('/')[-1]
            
        #filename = df['Filename'][ind]  <- simlpler alternative to above code
    
        print('Converting', filename + ' to images')
    
        #Convert pdf into image (each page of a pdf becomes one image)
        images = convert_from_path(file, timeout=10000)
        temp_titles = []
    
        for index, image in enumerate(images):
            temp_title = 'out_' +str(index) + '.jpg'
            temp_titles.append(temp_title)
            images[index].save(img_folder + temp_title, 'JPEG')
    
        print(len(images), 'pages:' + 'starting ocr')
    
        #Convert each image into a doc2text class and OCR
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
            with open(text_folder + filename + '.txt', 'a+') as f:
                f.write(text)
        
            page = int(''.join([letter for letter in title if letter.isdigit()])) + 1
        
            print('Page', page, "completed")
            del doc
        
        # Add raw text to data frame
        with open(text_folder + filename + '.txt') as f:
            raw_text = f.read()
        
        df.at[ind,"Raw Text"]=raw_text
            
        #Clear out temporary image folder
        temp_files = glob(img_folder + '*')
        for f in temp_files:
            os.remove(f)
    
    #Delete temporary image folder
    os.remove(img_folder)
    
    # Returns the original data frame with an extra column containg the machine
    # readdable text for a given file
    return df  
