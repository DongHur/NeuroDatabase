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

class Scrape:
    def __init__(self, driver, company):
        self.driver = driver
        self.company = company.lower()
    def scrape_overview(self, overview_field):
        # CLICK READ MORE
        try: 
            self.driver.find_elements_by_xpath("//a[@class='cb-link cb-display-inline ng-star-inserted']")[0].click()
        except:
            pass
        # FIND CONTENT CARD
        mat_card = self.driver.find_elements_by_xpath("/html[1]/body[1]/chrome[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/entity[1]/page-layout[1]/div[2]/div[1]/div[2]/div[1]/div[1]/entity-section[1]/section-layout[1]/mat-card[1]")
        content = mat_card[0].find_elements_by_class_name('section-layout-content')
        # FIND OVERVIEW FIELD CONTENT
        field_content = content[0].text.split('\n')
        field_content = np.array([cont.lower().strip() for cont in field_content])  
        try: # FINDING DESCRIPTION
            description_info = content[0].find_elements_by_tag_name('description-card')[0].text
        except:
            description_info = " "
        try: # FINDING GEOGRAPHIES
            geography_idx = np.where(field_content == self.company)[0][0]
            geographies_info = field_content[geography_idx+2]
        except:
            geographies_info = " "
        # CREATE OVERVIEW DATA OBJECT
        Overview = {"company": self.company, "content": "FOUND"}
        for interest in overview_field:
            try:
                idx = np.where(field_content==interest)[0].item()
                Overview[str(interest)]=field_content[idx+1]
            except:
                Overview[str(interest)]=" "
        Overview['description'] = description_info   
        Overview['geographies'] = geographies_info
        return Overview
    
    def scrape_funding_rounds(self):
        # GET TOTAL FUNDING AMOUNT FIELD
        try:
            funding_mat_card = self.driver.find_elements_by_xpath("//section-layout[@id='section-funding-rounds']")
            funding_field_content = funding_mat_card[0].text.split('\n')
            funding_field_content = np.array([cont.lower().strip() for cont in funding_field_content])
            tfa_idx = np.where(funding_field_content == "total funding amount")[0].item()
            total_funding_amount = funding_field_content[tfa_idx+1]
        except: 
            total_funding_amount = " "
        # GET LATEST FUNDING FIELDS
        try:
            investors= self.driver.find_elements_by_xpath("//section-layout[@id='section-funding-rounds']//tbody//tr")
            latest_inv_info = investors[0].text.split('\n')
            latest_funding = latest_inv_info[0]
            latest_financing = latest_inv_info[1]
            latest_raise = latest_inv_info[3]
        except:
            latest_funding = " "
            latest_financing = " "
            latest_raise = " "
        # CREATE FUNDING_INFO DATA
        funding_info={"total funding amount": total_funding_amount,
                     "latest funding": latest_funding,
                     "latest financing": latest_financing,
                     "latest raise": latest_raise}
        return funding_info
    
    def scrape_investor(self):
        try: 
            investors= self.driver.find_elements_by_xpath("//section-layout[@id='section-investors']//tbody//tr")
            investors_info = ""
            for i in range(len(investors)):
                investors_info += investors[i].text.split('\n')[0] + ", "
        except:
            investors_info = " "
        return investors_info
    
    def organize_content(self, overview, funding, investor):
        # CREATE ACTIVITY DATA
        if overview['acquired by'] != " ":
            activity = "acquired" +', '+overview['operating status']
        else:
            activity = overview['operating status']
        # CREATE MATURITY LEVEL DATA
        maturity_level = ""
        if overview['funding status'] != " ":
            maturity_level +=  overview['funding status']+','
        if overview['last funding type'] != " ":
            maturity_level +=  overview['last funding type']+','
        if overview['ipo status'] != " ":
            maturity_level +=  overview['ipo status']+','
        if overview['company type'] != " ":
            maturity_level +=  overview['company type']+','
        if maturity_level:
            maturity_level = maturity_level[:-1]
        else:
            maturity_level = " "
        # CREATE CONTENT OBJECT
        Content = {
            "Company": self.company,
            "Content": "FOUND",
            "URL": overview['website'],
            "Activity": activity,
            "Description": overview['description'],
            "Maturity Level": maturity_level,
            "Investors": investor,
            "Category": overview['categories'],
            "Sub Category": " ",
            "Tag1": " ",
            "Tag2": " ",
            "Last Funding": funding["latest funding"],
            "Latest Financing": funding["latest financing"],
            "Latest Raise (in MM)": funding["latest raise"],
            "Total Raised (MM)": funding["total funding amount"],
            "Co-Investors": " ",
            "Year Founded": overview["founded date"],
            "Geographies": overview["geographies"],
            "Founder/CEO" : overview["founders"],
            "Founder Email": overview["contact email"],
            "Founder 2": " ",
            "Founder 2 Email": " ",
            "BrainMind Filter": " ",
            "Ecosystem Member": " ",
            "Source": "crunchbase",
            "Number of Employees": overview["number of employees"],
            "Notes": " ",
            "Investors 3": " ",
            "Investors 5": " ",
            "Investors 6": " "
        }
        return Content
    
    {'total funding amount': '$125m', 'latest funding': 'Jul 19, 2017', 
     'latest financing': 'Series C - Brain Corp', 'latest raise': '$114M'}