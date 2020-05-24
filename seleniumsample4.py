from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

url = 'http://www.webscrapingfordatascience.com/postform2/'

driver = webdriver.Chrome(executable_path='/mnt/c/chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(10)
driver.get(url)

driver.find_element_by_name('name').send_keys('yukawa')
driver.find_element_by_css_selector('input[name="gender"][value="M"]').click()
driver.find_element_by_name('pizza').click()
driver.find_element_by_name('salad').click()
Select(driver.find_element_by_name('haircolor')).select_by_value('brown')
driver.find_element_by_name('comments').send_keys(
	['First line', Keys.ENTER, 'Second line'])

input('Press ENTER to submit the form')
driver.find_element_by_tag_name('form').submit()

input('Press ENTER to close the automated browser')
driver.quit()
