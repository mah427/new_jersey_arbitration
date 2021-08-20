'''
Author:
    Martin Hiti
    
Last Update:
    8/20/2021: 1) accounts for the fact that some of the awards are in .docx 
    format and 2) adds an additional chunck of code that converts the award 
    level data frame to a file level data frame as certain awards contain
    multiple files.
    
IMPORTANT: 
    This file should be used instead of the depricated ia_agreements_scrape.py

Purpose: 
    Webscrape arbitration awards from NJ PERC outputing a .csv that contains 
    award metadata and downlaoding each of the arbitration awards
'''

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import pandas as pd

options = Options()
options.headless = True

# Define function to download files from url
def download_file(download_url, filename, fldr):
    response = urllib.request.urlopen(download_url)  
    os.chdir(fldr)
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()
    
# Set up webdriver
driver = webdriver.Chrome('/home/martin/new_jersey_arbitration/drivers/chromedriver')
driver.get('https://www.perc.state.nj.us/IAAwards.nsf/IA_Issued?OpenView&Start=1&Count=524"')
awards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//body//table[2]//tbody//tr[@valign='top']"))
        )

#Working directories
out_folder = os.getcwd() + '/out_ia'

#Create an empty data frame to store meta data:
headers = ["Current Docket","Docket Numbers", "Public Employer", "Union",
           "County", "Arbitrator", "Date Received", "Award Type",
           "Current Status", "Appellate Court", "Supreme Court",
           "Consolidated with Docket Number(s)", "History", "Filenames"]
df = pd.DataFrame(columns = headers)


for award in awards:
    
    #Go to the Page and create a soup
    award_link = 'https://www.perc.state.nj.us' + BeautifulSoup(award.get_attribute('innerHTML'), 'html.parser').find("a").get('href')
    award_soup = BeautifulSoup(requests.get(award_link).content, 'html.parser')      

    #Put all of the text elements into a list
    award_info_raw = [text.get_text() for text in award_soup.find_all('font')]
    
    #Clean meta data from the list
    docket = award_info_raw[award_info_raw.index('Docket Number: ') + 1]
    current_docket = docket.split(" & ")[0]
    public_employer = award_info_raw[award_info_raw.index("Parties")+1]
    union = award_info_raw[award_info_raw.index("Parties")+3]
    county = award_info_raw[award_info_raw.index('Employer County:')+1]
    arbitrator = [] #Need to create an empty list to store arbitrator info: spil up into different list elements
    for i in range(1,4):
        arbitrator.append(award_info_raw[award_info_raw.index('Arbitrator:')+i])
    arbitrator = ''.join(arbitrator)   
    date = award_info_raw[award_info_raw.index('Date Received:')+1]    
    award_type = award_info_raw[award_info_raw.index('Award Type:')+1]
    status = award_info_raw[award_info_raw.index('Current Status:')+1]
    appellate_court = award_info_raw[award_info_raw.index('Appellate Court:')+1]
    supreme_court = award_info_raw[award_info_raw.index('Supreme Court:')+1]
    cons = award_info_raw[award_info_raw.index('Consolidated with Docket Number(s):')+1]
    histories = award_info_raw[award_info_raw.index('Award History')+1:]
    for i in histories: #Some of the award history section have a blank entry that must be deleted
        if i=="":
            histories.remove(i)
    history = "; ".join(histories)
    
    #Add all of the cleaned info to a row for each observation; print
    award_info_clean = [current_docket, docket, public_employer, union, county, arbitrator, date, award_type, status, appellate_court, supreme_court, cons, history]
    
    # For each of the awards we also find all clickable links which take us
    # to the pdf: we can also extract the name of the file from the link. We 
    # store the names of the files for each observation in a column of the 
    # data frame to make linkage 
    links = award_soup.select_one('body > form > table:nth-child(5)').find_all("a")
    
    #Create empty list
    filenames = []
    
    #Get the link from the html
    for link in links:
        link = "https://www.perc.state.nj.us/" + link.get('href')
        
        #Excrtract the filename and add it to 
        filename = link.split('?OpenElement')[0].split("$File/")[1]
        filenames.append(filename) 
        
        link = link.replace(" ", "%20")
        download_file(link, filename, fldr = out_folder + '/files')
    
    #Join all of the filenames for each arbitration award into one string with
    #each document name seperated by a semicolon. Then add to award_info_clean
    filenames = "; ".join(filenames)
    print(filenames)
    
    award_info_clean.append(filenames)
    #Append meta data to the bottom of the dataframe
    df.loc[len(df)] = award_info_clean

#Save Data Frame as .csv
os.chdir(out_folder)
df.to_csv("arbitration_awards.csv")

##############################################################################

#Data cleaning

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
        
file_data.to_csv("arbitrtation_awards_file_level.csv")

