from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions

# ******** Functions *********
Data = {}
# Start Scraping
course_name = driver.find_element_by_id('page-content').text
course_summary = driver.find_element_by_id('summaryStats').text

table_list = driver.find_elements_by_tag_name('table')
for table in table_list:
	tr_list = table.find_elements_by_xpath('.//tbody/tr')
	for tr in tr_list:
		td_list = tr.find_elements_by_tag_name('td')
		for count, td in enumerate(td_list):
			Data[str(count)] = td.text

# ****************************