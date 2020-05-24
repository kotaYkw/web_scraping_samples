from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://www.webscrapingfordatascience.com/complexjavascript/'

# chromedriver.exeのある絶対パスを指定
driver = webdriver.Chrome(executable_path='/mnt/c/chromedriver_win32/chromedriver.exe')
#driver.implicitly_wait(10)
driver.get(url)
quote_elements = WebDriverWait(driver, 10).until(
	EC.presence_of_all_elements_located(
		(By.CSS_SELECTOR, ".quote:not(.decode")
		)
	)

#for quote in driver.find_elements_by_class_name('quote'):
for quote in quote_elements:
	print(quote.text)

input('Press ENTER to close the automated browser')
driver.quit()
