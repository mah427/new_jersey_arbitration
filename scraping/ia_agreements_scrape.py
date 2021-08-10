# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 15:08:26 2021

@author: mhiti
"""
#Import Packages
from bs4 import BeautifulSoup
import os as os
import requests
import pandas as pd
import time
import urllib.request
import csv

#Set Working Directory
fldr = "C:/Users/marti/nj_arbitration/scraping/" #Working Directory
os.chdir(fldr)


# Define function to downloaf pdf's
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename + '.pdf', 'wb')
    file.write(response.read())
    file.close()

page_url = "https://www.perc.state.nj.us/IAAwards.nsf/IA_Issued?OpenView&Start=1&Count=524"
page = requests.get(page_url)

#Page Soup
soup = BeautifulSoup(page.content, 'html.parser')

#Table Soup
soup_table = soup.find("table", {'cellpadding':'2'})

#Awards Soup
data = []
headers = ["Current Docket","Docket Numbers", "Public Employer", "Union",
           "County", "Arbitrator", "Date Received", "Award Type",
           "Current Status", "Appekkate Court", "Supreme Court",
           "Consolidated with Docket Number(s)", "History"]
link_html_index_list = []

awards_soup = soup_table.find_all("tr", {'valign':'top'})

for index, award in enumerate(awards_soup):
    
    award_info_url = 'https://www.perc.state.nj.us/' + award.find("a").get('href')
    award_info_page = requests.get(award_info_url)
    award_info_soup = BeautifulSoup(award_info_page.content, 'html.parser')    
    award_info = award_info_soup.find_all("font")
    
    award_info_list = []
    
    for item in award_info:
        award_info_list.append(item.get_text())
    
    docket = award_info_list[award_info_list.index('Docket Number: ') + 1]
    current_docket = docket.split(" & ")[0]
    public_employer = award_info_list[award_info_list.index("Parties")+1]
    union = award_info_list[award_info_list.index("Parties")+3]
    county = award_info_list[award_info_list.index('Employer County:')+1]
    arbitrator = []
    for i in range(1,4):
        arbitrator.append(award_info_list[award_info_list.index('Arbitrator:')+i])
    arbitrator = ''.join(arbitrator)   
    date = award_info_list[award_info_list.index('Date Received:')+1]    
    award_type = award_info_list[award_info_list.index('Award Type:')+1]
    status = award_info_list[award_info_list.index('Current Status:')+1]
    appellate_court = award_info_list[award_info_list.index('Appellate Court:')+1]
    supreme_court = award_info_list[award_info_list.index('Supreme Court:')+1]
    cons = award_info_list[award_info_list.index('Consolidated with Docket Number(s):')+1]
    histories = award_info_list[award_info_list.index('Award History')+1:]
    for i in histories:
        if i=="":
            histories.remove(i)
            print("REmoved")
    history = ";".join(histories)
    
    link_html=award_info_soup.find_all("a")
    
    link_html_index = [link_html, index]
    
    link_html_index_list.append(link_html_index)
    
    row = [
        current_docket, docket, public_employer, union, 
        county, arbitrator, date, award_type, 
        status, appellate_court, supreme_court,
        cons, history]
    
    print(row)
    data.append(row)

#Export meta-data to csv    
os.chdir(fldr+'out_ia')
df = pd.DataFrame(data, columns = headers)
df.to_csv("arbitration_awards.csv")
    
#File Link and Date
os.chdir(fldr+'out_ia/files')
for html_index in link_html_index_list:
    index = html_index[1]
    
    if index > 515:
        html = html_index[0]
        for element in html:
            link = "https://www.perc.state.nj.us/" + element.get('href')
            
            if index in [444, 478, 493, 494]:
                error_soup = BeautifulSoup(requests.get(link).content, 'html.parser')
                error_htmls = error_soup.find_all("a")
                for error_html in error_htmls:
                    link = "https://www.perc.state.nj.us/" + error_html.get('href')
                    link = link.replace("?OpenElement","")
                    link2 = link.replace(" ","%20")
                    index = html_index[1]
                    filename = link.split("$File/")[1].split(".pdf")[0].replace("?OpenElement","").replace(".","" + "_") + "Index=" + str(index)
                    download_file(link2, filename)
                    print(filename, "downloaded")
                    print("")
                    
            elif index in [449,450,516,517]:
                error_htmls = html[1:]
                for error_html in error_htmls:
                    link = "https://www.perc.state.nj.us/" + error_html.get('href')
                    link = link.replace("?OpenElement","")
                    link2 = link.replace(" ","%20")
                    index = html_index[1]
                    filename = link.split("$File/")[1].split(".pdf")[0].replace("?OpenElement","").replace(".","" + "_") + "Index=" + str(index)
                    download_file(link2, filename)
                    print(filename, "downloaded")
                    print("")
                    
            else:    
                link = link.replace("?OpenElement","")
                link2 = link.replace(" ","%20")
                filename = link.split("$File/")[1].split(".pdf")[0].replace("?OpenElement","").replace(".","" + "_") + "Index=" + str(index)
                download_file(link2, filename)
                print(filename, "downloaded")
                print("")


