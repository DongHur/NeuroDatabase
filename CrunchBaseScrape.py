from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from lxml import html
import os
import json
import numpy as np

# Functions
def find_session_id(driver):
	# Find session_id
	outF = open('session_id.txt', 'w')
	url = driver.command_executor._url 
	session_id = driver.session_id  
	outF.write(session_id)
	outF.write('\n')
	outF.write(url)
	outF.close()

	print("url: ", url)
	print("Session Id: ", session_id)



def main():
  driver = webdriver.Chrome('./chromedriver')
  actions = ActionChains(driver)
  find_session_id(driver)

  driver.get('https://www.crunchbase.com/')
  elem = driver.find_element_by_id('mat-input-0')
  elem.send_keys('hello')
  #mat-input-0

  input('PRESS ENTER WHEN YOU ARE FINISHED')

main()