from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.get('http://web1.ncaa.org/stats/StatsSrv/careersearch');
select = Select(driver.find_element_by_name('searchOrg'))
select.select_by_value('5')
select = Select(driver.find_element_by_name('academicYear'))
select.select_by_value('2014')
time.sleep(10)
driver.quit()