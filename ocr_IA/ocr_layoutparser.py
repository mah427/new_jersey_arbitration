#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 14:41:49 2021

@author: Allison

This builds on ocr_master.py to incorporate layout parser tools

"""
#Imports

import layoutparser as lp 
import matplotlib.pyplot as plt
#matplotlib inline 
import pandas as pd
import numpy as np
import cv2



import os
import requests
from glob import glob
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import pytesseract
import cv2

#Define grayscale function
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Google Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"/opt/local/bin/tesseract"

#Define working directory
#fldr = "C:\\Users\\marti\\new_jersey_arbitration\\ocr_IA"
fldr = "/Users/u6025349/Dropbox/GitHub/new_jersey_arbitration/ocr_IA"
os.chdir(fldr)

#Folder of pdfs:
pdf_folder = os.path.join(os.getcwd(),'pdf','')

#Temp folder to save images
image_folder = os.path.join(os.getcwd(), 'temp','')

#Secondary temp folder: for preprocessed images
image_folder_thresh = os.path.join(os.getcwd(), 'thresh','')

#Folder of text results
text_folder = os.path.join(os.getcwd(), 'text', '')

#Pdf files
#pdf_files = glob(pdf_folder + '/*.pdf')

## TEMP: PRACTICE WITH 1 FILE
pdf_files = glob('/Users/u6025349/Dropbox/GitHub/new_jersey_arbitration/ocr_IA/pdf/IA-2016-003.pdf')

#%% Create images
for file in pdf_files:
          
    
   # filename = file.split('.pdf')[0].split('\\')[-1]
    filename = file.split('.pdf')[0].split('/')[-1]
    print("File: ", filename, "Converting to image.")
   
    #Convert pdf to images
    images = convert_from_path(file, 100)
    titles = []
    try:
        for index, image in enumerate(images, start=0):
            title = 'out_'+str(index) + '.jpg'
            titles.append(title)
            try:
                images[index].save(image_folder+title, 'JPEG')
            except:
                pass
    except:
        pass
    print(filename+': ' + str(len(images))+' pages. OCR and saving.')
 

    #Image Preprocessing (convert to black and white then thresholding)
    image_files = glob(image_folder + '/*.jpg')
    for image in image_files:
        #image_filename = image.split('.jpg')[0].split('\\')[-1]
        image_filename = image.split('.jpg')[0].split('/')[-1]
        image = cv2.imread(image)
        gray_image = grayscale(image)
        thresh, im_bw = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite(image_folder_thresh + image_filename + '.jpg', im_bw)
#%% Tesseract
        
    # #OCR Images using tesseract
    # for title in titles:
    #     try:
    #         data = pytesseract.image_to_string(Image.open(image_folder+title))
    #         with open(text_folder+filename+'.txt', 'a+') as f:
    #             f.write(data)
    #     except:
    #         pass
  

    
    #OCR Images using tesseract 
    for title in titles:
        data = pytesseract.image_to_string(Image.open(image_folder+title))
        with open(text_folder+filename+'.txt', 'a+') as f:
            f.write(data)
        
        page = "".join([letter for letter in title if letter.isdigit()])
        print("Page", page, "complete")
        
    print('OCR Complete')
    
    # Clear out temporary folder
    # files = glob(image_folder+'*')
    # for f in files:
    #     os.remove(f)
    print("Next Pdf")

print("All PDFs complete")


#%% LAYOUT PARSER
ocr_agent = lp.TesseractAgent(languages='eng') 

image = cv2.imread(image_folder_thresh + image_filename + '.jpg')
image = image[..., ::-1]

model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})
layout = model.detect(image)
#lp.draw_box(image, layout, box_width=3)

text_blocks = lp.Layout([b for b in layout if b.type=='Text'])
figure_blocks = lp.Layout([b for b in layout if b.type=='Figure'])

text_blocks = lp.Layout([b for b in text_blocks \
                   if not any(b.is_in(b_fig) for b_fig in figure_blocks)])
    
h, w = image.shape[:2]

left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(image)

left_blocks = text_blocks.filter_by(left_interval, center=True)
left_blocks.sort(key = lambda b:b.coordinates[1])

right_blocks = [b for b in text_blocks if b not in left_blocks]
right_blocks.sort(key = lambda b:b.coordinates[1])

# And finally combine the two list and add the index
# according to the order
text_blocks = lp.Layout([b.set(id = idx) for idx, b in enumerate(left_blocks + right_blocks)])

for block in text_blocks:
    segment_image = (block
                       .pad(left=5, right=5, top=5, bottom=5)
                       .crop_image(image))
        # add padding in each image segment can help
        # improve robustness

    text = ocr_agent.detect(segment_image)
    block.set(text=text, inplace=True)
    
for txt in text_blocks.get_texts():
    print(txt, end='\n---\n')