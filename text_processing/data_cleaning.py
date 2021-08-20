"""
- Identifies all pdf's from a particular arbitrator, grabs the pdf file, uses
  Tesseract and doc2text preprocessing tools to conver the files to machine-
  readable text.
"""
#Imports
import pandas as pd
import os
import doc2text
from glob import glob 
from pdf2image import convert_from_path
import numpy as np

#Folders:
pdf_folder = "/home/martin/new_jersey_arbitration/scraping/out_ia/files"

#Load in data
award_data = pd.read_csv('/home/martin/new_jersey_arbitration/scraping/out_ia/arbitration_awards.csv')

#Some awards contain multiple files: tranform from award level to file level
file_data = pd.DataFrame()
for ind in award_data.index:
    filenames = award_data['Filenames'][ind]
    
    # Convert filenames for each award to a list
    filenames = filenames.split('; ')
    
    # The dictionary below represents the data for each observation which is one file:
    for file in filenames:
        data = {
            "Filename" : file,
            "Current Docket" : award_data["Current Docket"][ind],
            "Docket Numbers" : award_data["Docket Numbers"][ind],
            "Public Employer": award_data["Public Employer"][ind],
            "Union"          : award_data["Union"][ind],
            "County"         : award_data["County"][ind],
            "Arbitrator"     : award_data["Arbitrator"][ind],
            "Date Received"  : award_data["Date Received"][ind],
            "Award Type"     : award_data["Award Type"][ind],
            "Current Status" : award_data["Current Status"][ind],
            "Appellate Court": award_data["Appellate Court"][ind],
            "Supreme Court"  : award_data["Supreme Court"][ind]        
        }
    
        file_data = file_data.append(data, ignore_index=True)

#Define Fuunctions
def get_arbitrator(arbitrator_name):
    '''
    Returns file-level data frame for specific arbitrator
    '''
    output = file_data[file_data['Arbitrator']== "Mastriani, J"]
    return(output)

def get_file(arbitrator_df, folder):
    '''
    This function takes as an input file-level data frame and returns a list that gives 
    the full paths to all dedired files
    
    The folder input should be set to the path of the pdfs that were scraped from PERC
    '''
    output = []
    filenames = arbitrator_df['Filename'].tolist()
    for filename in filenames:
        file = os.path.join(folder, filename)
        output.append(file)
    
    return(output)
    
def ocr_files(df, input_folder):
    
    #Create empty variable to be filled with text
    df["Raw Text"] = ""
    
    #Create and define folders
    img_folder = os.path.join(os.getcwd(), "temp", '')
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
        
    text_folder = os.path.join(os.getcwd(), "text", '')
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
    
    for ind in df.index:
        
        file = os.path.join(input_folder, df['Filename'][ind])
        
        #Extract name from file:
        if '.docx' in file:
            filename = file.split('.docx')[0].split('/')[-1]
        else:
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
    
    
    os.remove(img_folder)
    
    return df
 
#Use Function to create data frama containing Mastriani's files           
file_data_mastriani = get_arbitrator("Mastriani, J")

#OCR the files add add raw text to data frame
file_data_mastriani = ocr_files(file_data_mastriani, pdf_folder)

#Save data frame
file_data_mastriani.to_csv("file_data_mastriani.csv")