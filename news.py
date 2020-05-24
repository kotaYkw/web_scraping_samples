from selenium import webdriver

base_url = 'https://news.google.com/?ned=us&hl=en'

driver= webdriver.Chrome(executable_path='/mnt/c/chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(10)
driver.get(base_url)

#//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[2]/div/article/a
#//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[3]/div/article/a
for i, elem in enumerate(driver.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div')):
	if i == 0:
		continue
	print(elem)
	link = elem.find_element_by_xpath('div/article/a')
	news_url = link.get_attribute('href')
	print(news_url)

driver.quit()