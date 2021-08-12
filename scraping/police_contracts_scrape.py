#Import Packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os as os
import requests
import pandas as pd
import time
import urllib.request
import csv

#Set Working Directory
fldr = "insert directory"
os.chdir(fldr)
driver = webdriver.Chrome(fldr + 'chromedriver.exe')


# Define function to downloaf pdf's
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename + '.pdf', 'wb')
    file.write(response.read())
    file.close()
    
# =============================================================================
# def internet_on():
#     try:
#         urllib.request.urlopen('https://www.espn.com/', timeout=30)
#         return True
#     except:
#         return False
# =============================================================================


#URL & HTML
page_url = "https://www.perc.state.nj.us/publicsectorcontracts.nsf/Type?OpenView&Start=1&Count=623&Expand=4#4"
driver.get(page_url)
html = driver.page_source
soup = BeautifulSoup(driver.page_source, 'html.parser')
body = soup.find('body') #Only want material under body tag
table = body.find('table', {'cellpadding':'2'}) #Only want main table of entries identified with 'cellpadding'=2
cities = table.find_all('td', {'colspan' : '7'}) #cities contains soup elements for each municipality

#Create empty list to store all data. Each list within the list will represent one observation at the contract level
all_data = []


for city in cities:
    
    #Get link that expands the menu for a given city showing all contracts in city  & convert to soup
    city_link = "https://www.perc.state.nj.us" + city.find('a')['href']
    soup_city = BeautifulSoup(requests.get(city_link).content, 'html.parser')
    body_city = soup_city.find('body')
    table_city = body_city.find('table', {'cellpadding':'2'})
    contracts = table_city.find_all('a', text=True)[4:]
    
    #Create empty list that will hold lists which represent each observation (contract) in the current city
    city_data = []
    
    
    for contract in contracts:

        #Extract Link of each individuual contract & create contract-level soup
        contract_link = "https://www.perc.state.nj.us/" + contract['href']
        soup_contract = BeautifulSoup(requests.get(contract_link).content, 'html.parser')
        contract_info = soup_contract.find_all('font', text=True)
        
        #if "Police" in soup_contract.get_text():
        try:
            #Create empty list for contract: this list is one observation
            contract_info_list = []
            
            #Add scraped items to list
            for item in contract_info:
                contract_info_list.append(item.get_text())
            employer = contract_info_list[2]
            
            geoid = employer.split("-")
            city = '-'.join(geoid[:-1])
            county = geoid[-1]
            
            union = contract_info_list[4]
            start_date = contract_info_list[6]
            end_date = contract_info_list[8]
            employer_type = contract_info_list[10]
            union_type = contract_info_list[12]
            
            contract_pdf_hrefs = soup_contract.find_all('a', {'style' : "display: inline-block; text-align: center"})
            for href in contract_pdf_hrefs:
                if "Res" not in href.get_text():
                    if "Summary" not in href.get_text():
                        contract_pdf_link = "https://www.perc.state.nj.us" + href.get('href')
                
            row_data = [employer, union, city, county, start_date, end_date, employer_type, union_type, contract_pdf_link]
            
            print(row_data)
            print("")
            
            #Append contract to city data
            city_data.append(row_data)
            
        #Some elements have missing data: will need to manually fill these in
        except IndexError:
            contract_info_list = []
            
            for item in contract_info:
                contract_info_list.append(item.get_text())
            employer = contract_info_list[2]
            
            geoid = employer.split("-")
            city = '-'.join(geoid[:-1])
            county = geoid[-1]
            
            union = contract_info_list[4]
            start_date = "NA"
            end_date = "NA"
            employer_type = contract_info_list[8]
            union_type = contract_info_list[10]
            
            contract_pdf_hrefs = soup_contract.find_all('a', {'style' : "display: inline-block; text-align: center"})
            for href in contract_pdf_hrefs:
                if "Res" not in href.get_text():
                    if "Summary" not in href.get_text():
                        contract_pdf_link = "https://www.perc.state.nj.us" + href.get('href')
                
            row_data = [employer, union, city, county, start_date, end_date, employer_type, union_type, contract_pdf_link]
            
            
            city_data.append(row_data)
    
    #Add city data to overall data
    all_data += city_data
    
    time.sleep(3)
    
    print('next city') 
    
#Convert scraped data to data frame and export as .csv
headers = ['employer', 'union', 'city', 'county', 'start_date', 'end_date' , 'employer_type', 'union_type', 'contract_pdf_link']    
municipal_contracts = pd.DataFrame(columns=headers, data = all_data)
municipal_contracts.to_csv(fldr + "out_contracts/municipal_contracts_improved.csv")


#Download pdfs
with open(fldr + "out_contracts\\municipal_contracts_improved.csv") as f:
    contracts = csv.reader(f)
    headers = next(contracts)
    
    records = []
    for contract in contracts:
        record = dict(zip(headers, contract))
        records.append(record)
        
    #Pdfs
    os.chdir(fldr + 'out_contracts/files')
    for record in records:
        
        if "Police" in record['union_type']:
            
            download_url = record['contract_pdf_link']
            filename = record['union'].replace(" ", "_").replace("/", "_") + '_' + record['start_date'][-4:]  + '_' + record['end_date'][-4:]
            
            #Use function defined at beginning
            os.chdir(fldr + 'out_contracts/files')
            download_file(download_url, filename)
            
            print(filename)
            print('next file')
            print("")
                        
        