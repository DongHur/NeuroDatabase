from selenium import webdriver
import os
import json
import numpy as np

outF = open('session_id.txt','r')
linesArray = outF.readlines()
outF.close()

print('session id: ', linesArray[0])
print('url: ', linesArray[1])

session_id = linesArray[0]
url = linesArray[1]
# url = 'http://127.0.0.1:49306'
# session_id = 'de68c03cde2b8398ad4667e2dc02320b'

driver = webdriver.Remote(command_executor = url, desired_capabilities = {})
driver.session_id = session_id


# driver.get('https://course-evaluation-reports.fas.harvard.edu/fas/list;jsessionid=3231BBC6748B6B51CC833E2667C1E6F5?')

# driver.get('https://www.google.com/search?q=asdf&oq=asdf&aqs=chrome..69i57j69i60l2j69i61j69i60.390j0j7&sourceid=chrome&ie=UTF-8')