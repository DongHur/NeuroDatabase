from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from lxml import html
import os
import json
import numpy as np
import time
import tablib
import sys
# IMPORT IMPORTANT CLASSES FOR SCRAPING AND DATA CREATION
from tool.Scrape import Scrape
from tool.CSV_Data import CSV_Data


# GET ARGUMENTS
company_txt_name = input("INPUT Text Filename: ")
txt_filename = "company_txt/"+company_txt_name+".txt"
csv_filename = "company_csv/"+company_txt_name+".csv"

# OPEN GOOGLE CHROME
driver = webdriver.Chrome('./chromedriver')
actions = ActionChains(driver)
url = driver.command_executor._url 
session_id = driver.session_id  
# GO TO WEBSITE
driver.get('https://www.crunchbase.com/')
time.sleep(1)
input('Press Enter After Verifying You Can Scrape Google Chrome')

# START SCRAPING
with open(txt_filename) as f:
    company_list = f.read().split('\n')
overview_field = ['acquired by', 'operating status', 'funding status', 'last funding type', 
                    'company type', 'website' , 'last funding type', 'categories',
                    'ipo status','founded date', 'founders','contact email',
                    'number of employees', 'founders', 'categories']

Content_List = np.array([])
wait_time = 1.5
for idx_company, company_str in enumerate(company_list):
    # SEARCH COMPANY
    searchbar = driver.find_elements_by_xpath("//input[@id='mat-input-0']")
    searchbar[0].send_keys(company_str)
    searchbar[0].clear()
    searchbar[0].send_keys(Keys.RETURN)
    time.sleep(wait_time)
    
    search_list = driver.find_elements_by_xpath("/html[1]/body[1]/chrome[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/search[1]/page-layout[1]/div[1]/div[1]/form[1]/div[2]/results[1]/div[1]/div[1]/div[3]/sheet-grid[1]/div[1]/div[1]/grid-body[1]/div[1]/div[1]")
    found = False
    try:
        for company_ele in search_list[0].find_elements_by_tag_name("grid-row"):
            verify_company = company_ele.text.split('\n')[1]
            is_company = verify_company.lower().find(company_str.lower())
            print("CHECKING :", company_ele.text.split('\n')[1])
            if is_company >= 0:
                print(company_str, " FOUND")
                found = True
                # CLICK FIRST LINK
                hyperlink_str = "//a[@title='" + verify_company + "']"
                driver.find_element_by_xpath(hyperlink_str).click()
                time.sleep(wait_time)
                
                Scrape_Company = Scrape(driver, verify_company)
                print("SCRAPING OVERVIEW")
                overview = Scrape_Company.scrape_overview(overview_field)
                print("SCRAPING FUNDING ROUNDS")
                funding = Scrape_Company.scrape_funding_rounds()
                print("SCRAPING INVESTOR")
                investor = Scrape_Company.scrape_investor()
                print("ORGANIZING CONTENT")
                Content = Scrape_Company.organize_content(overview, funding, investor)
                break
            else:
                print(company_str, " NOT FOUND")  
                continue
            print("")
        if not found:
            Content = {"Company": company_str, "Content": "NOT FOUND"}
        Content_List = np.append(Content_List, Content)
        print("______________________________________")
    except:
        print("COULDN'T FIND ", company_str)
        print("______________________________________")
    time.sleep(wait_time)

# CREATE CSV DATAFILE
CSV = CSV_Data(data=Content_List, filename=csv_filename) 
CSV.run()
CSV.create_header()
CSV.export_csv()