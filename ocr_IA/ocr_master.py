#Imports
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
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\tesseract.exe"

#Define working directory
fldr = "C:\\Users\\marti\\arbitration\\ocr_IA"
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
pdf_files = glob(pdf_folder + '/*.pdf')

for file in pdf_files:
    
    filename = file.split('.pdf')[0].split('\\')[-1]
    print("File: ", filename, "Converting to image.")
    
    #Convert pdf to images
    images = convert_from_path(file, 100)
    titles = []
    try:
        for index, image in enumerate(images, start=1):
            title = 'out_'+str(index) + '.jpg'
            titles.append(title)
            try:
                images[index].save(image_folder+title, 'JPEG')
            except:
                pass
    except:
        pass
    print(filename+': ' + str(len(images))+' pages. OCR and saving.')
    
    #Image Preprocessing:
    image_files = glob(image_folder + '/*.jpg')
    for image in image_files:
        image_filename = image.split('.jpg')[0].split('\\')[-1]
        image = cv2.imread(image)
        gray_image = grayscale(image)
        thresh, im_bw = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)
        cv2.imwrite(image_folder_thresh + image_filename + '.jpg', im_bw)

        
    #OCR Images
    for title in titles:
        try:
            data = pytesseract.image_to_string(Image.open(image_folder_thresh+title))
            with open(text_folder+filename+'_thresh.txt', 'a+') as f:
                f.write(data)
        except:
            pass
        
        page = "".join([letter for letter in title if letter.isdigit()])
        print("Page", page, "complete")
        
    print('OCR Complete')
    
    files = glob(image_folder+'*')
    for f in files:
        os.remove(f)
    print("Next Pdf")

print("All PDFs complete")

