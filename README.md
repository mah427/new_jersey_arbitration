# New Jersey Arbitration

Last Updated 8/11/2021

# Project Steps
## Current Tasks
* Convert scanned pdf's to machine readable text. Two options:
    * Google Tesseracr-OCR (using Python Wrapper)
        * See OCR_IA folder: text out put is generally fairly accurate but can be impropved with processing. This method also strugles capturing some of the formatting.
    * ABBYY FineReader
        * Potential to save output as html and use BeautifulSoup to get the text from different elements. This would be extremely advantageous when categorizing different parts of 

## Future Projects
* Segment award text files into sections (union demands, city offer, award)
* Identify provisions of interest (using Rushin 2017) in the arbitration awards (and final offers)

## Completed Taks
 * SCrape interest arbitration awards 

# Project Contents:
Below is a describtion of the cntents and there purpose:
* Scraping
	* Contains master scraping script for police union contracts and arbitration awards
* Interest