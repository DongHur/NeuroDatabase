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

class CSV_Data:
    def __init__(self, data, filename):
        self.data = data
        self.len_data = len(data)
        self.tab_data = tablib.Dataset()
        self.filename = filename
        self.fields = ['Company', 'Content', 'URL', 'Activity', 'Description', 'Maturity Level', 'Investors', 'Category', 
                        'Sub Category', 'Tag1', 'Tag2', 'Last Funding', 'Latest Financing', 
                       'Latest Raise (in MM)', 'Total Raised (MM)', 'Co-Investors', 'Year Founded',
                       'Geographies', 'Founder/CEO', 'Founder Email', 'Founder 2', 'Founder 2 Email', 'BrainMind Filter',
                       'Ecosystem Member', 'Source', 'Number of Employees', 'Notes', 'Investors 3',
                       'Investors 5', 'Investors 6']
    
    def create_header(self):
        self.tab_data.headers = self.fields
        
    def create_found(self, i):
        row = []
        row.append(self.data[i]["Company"])
        row.append(self.data[i]["Content"])
        for field in self.fields[2:]:
            row.append(self.data[i][field])
        self.tab_data.append(row)
        
    def create_not_found(self, i):
        row = []
        row.append(self.data[i]["Company"])
        row.append(self.data[i]["Content"])
        for field in self.fields[2:]:
            row.append(" ")
        self.tab_data.append(row)
        
    def run(self):
        for i in range(self.len_data):
            if self.data[i]['Content'] == "FOUND":
                self.create_found(i)
            else:
                self.create_not_found(i)
                
    def export_csv(self):
        csv_data = self.tab_data.export('csv')
        f = open(self.filename, "w")
        f.write(csv_data)
        f.close()