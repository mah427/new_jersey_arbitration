# RA_Martin Project Notes
## File Overview
**Notes: each `.py` file contains specific to do's and more detailed comments**
#### Repo Name: New Jersey Arbitration
* README.md
* arbitration_awards_notes.md: *notes on important elements of award documents*
* `abbyy_processing/`
    * Tesseract_ABBYY_Comparison.ipyng
    * `raw_data/`
        * *pdf file scraped from PERC*
    * `html/`
         * *ABBYY html output of OCR for files in raw_data/*
* `ocr_IA/`: *This folder contains a first attempt extracting machine readable text from the scanned arbitration awards.  `ocr_doc2text/` and `ocr_layoutparser/` are two other folders which use different packages for the same purpose. Currently the most accurate OCR results are in the `ocr_doc2text/` folder how the `ocr_IA/` folder contains a good base script which can be adapted to different packages/methods of OCR'ing in the future.*
    * `ocr_master.py` :
        * *Basline file for OCR'ing batches of pdfs. To run, place all pdfs in the folder below, run the script, and see results in the `text/` folder*
    * `pdf/`
    * `text/`
* `ocr_doc2text/`: *This folder contains materials for converting batches of pdfs to machine readable text using Tesseract OCR. This folder improves on ocr_ia by incorporating a number of preprocessing strategies found in the doc2text package. The doc2text package was modified to be compatabile with python3 (see notes in ocr_doc2text_master.py for more details)*
    * `ocr_doc2text_master.py` *This file uses doc2text to convert batches of pdf files into machine readable text. The most recent version of this file defines a function which takes as an input a file level data frame and then returns the data fram with an additional column with the raw text of the file*
    * `pdf/`
    * `text/`
* `ocr_layoutparser`
    * `ocr_layoutparser.ipynb` : *Jupyter Notebook containing first attempt at using layout parser to convert. The goal is to preserve elements of the formating of the document when extracting infromation, especially tables. The initial attempt was relatively unsuccessful, but the follwing strategies may yield better results*
        * Test Google Cloud Vision functionality to preserve hierarchy of the text in the documents
        * Train a custom dataset for use with Detectron2's deep learning capabilities using [layout-model training](https://github.com/Layout-Parser/layout-model-training) and [annotation service](https://github.com/Layout-Parser/annotation-service)
    * `pdf/`
* `scraping/`
    * `ia_scrape.py`: *script that scrapes arbitration awards from NJ PERC outputing a .csv that contains awards metadata and downloading each of file. **Important:** the most recent update to thies file (8/20/2021) improves the code by 1) accounting for the fact that some of the awards are in .docx format and 2) converting the award level data frame to a file level data frame as certain awards (docket numbers) contain multiple files. This makes it much easier to link meta data for each file with the text once we start conducting textual analysis/splitting*
    * `out_ia/` : contains output from above webcrape
        * `arbitration_awards.csv` *Contains award meta data at the docket number level.*
        * `arbitration_awards_file_level.csv` *Contains award meta data at the file level. This is the output of the most recent update*
        * `files/`
    * `police_contract_scrape.py`: *script that scrapes police union contracts from NJ PERC outputting a .csv that contains contract metadata and grabs the link to the contract. The second half of the script then dowloads the file in each of the links. However, the program crashes anytime the internet connection is lost. The next step in improving this scrape is to ensure that the program waits until connection is re-established rather than cashing*
    * `out_contracs/`
        * `municipal_contracs_improved.csv`
        * Note: will add a `files/` folder that contains each of the folder once the scraping script is improved*

*

## Important Links
Raw Data:

[Arbitration awards](https://www.perc.state.nj.us/IAAwards.nsf)

[Police contract](https://www.perc.state.nj.us/publicsectorcontracts.nsf/ER?OpenView&CollapseView)

OCR:

[layout-parser package](https://github.com/Layout-Parser/layout-parser)

[doc2text package](https://github.com/jlsutherland/doc2text)

[Example OCR code](https://nanonets.com/blog/ocr-with-tesseract/)

Text Analysis:

[Elliot Ash NLP course](https://github.com/elliottash/text_ml_course_2018)

[NLTK course](https://www.nltk.org/book/)

