# New Jersey Arbitration

Last Updated 8/11/2021

# Project Steps
## Current Tasks


* Set up collaboration with Git Hub
* Convert scanned pdf's to machine readable text. Potential options:
    * Google Tesseract-OCR (using Python Wrapper)
        * See OCR_IA folder: text out put is generally fairly accurate but can be impropved with processing. This method also strugles capturing some of the formatting. 
    * ABBYY FineReader
        * Potential to save output as html and use BeautifulSoup to get the text from different elements. This would be extremely advantageous when categorizing different parts of the awards.

* Read through awards to get a better understanding of contents 

## Future Tasks
* Segment award text files into sections (union demands, city offer, award)
    * Custom-built splitter relaing on the relatively standard format of awards anf contracts to 
* Identify provisions of interest (using Rushin 2017) in the arbitration awards (and final offers)
    * Text classification pipeline: Dataset preparation, feartture engineering (text data to featre vectors), model training
## Completed Taks
 * Scraped interest arbitration awards and police CBAs from NJ PERC

# Project Contents:
Below is a describtion of the cntents and there purpose:
* Scraping (folder)
	* ia_agreements_scrape.py: python code to scrape meta data form Interest Arbitration awards and downlaod awards
	* police_contracts_scrape.py: python code to scrape meta data for Police Union Contracts
* OCR_IA (folder)
    * ocr_master.py: uses Google Tesseract-OCR to convert pdfs to txt files. 
    * OCR_preprocessing.ipynb: WORKING FILE: explores potential steps to preprocess the image to improve OCR quality

## File Tree
```
new_jersey_arbitration
│   README.md
│   arbitration_awards_notes.md   
│   Tesseract_ABBYY_Comparison.ipynb
└───scraping
│   │   ia_agreements_scrape.py
│   │   police_contracts_scrape.py
│   └───out_contracts
│   │       municipalcontracts.csv
│   └───out_ia
│           files
│           arbitration_awards.csv
└───ocrIA
│   │   ocr_master.py
│   │  file022.txt
│   └───pdf
│   └───text
└───abby_processing
│   └───raw_data
│   └───html
```
