from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# 独自のカスタマイズ条件を設定するためのクラス
class at_least_n_elements_found(object):
	def __init__(self, locator, n):
		self.locator = locator
		self.n = n
	def __call__(self, driver):
		# ここで何らかの処理を実行し、条件の結果次第でFalseまたはそれ以外の値を返す
		elements = driver.find_elements(*self.locator)
		if len(elements) >= self.n:
			return elements
		else:
			return False

url = 'http://www.webscrapingfordatascience.com/complexjavascript/'

# chromedriver.exeのある絶対パスを指定
driver = webdriver.Chrome(executable_path='/mnt/c/chromedriver_win32/chromedriver.exe')
driver.get(url)

# 明示的待機を使わないケースでは暗黙的待機を使う
driver.implicitly_wait(10)

div_element = driver.find_element_by_class_name('infinite-scroll')
quotes_locator = (By.CSS_SELECTOR, ".quote:not(.decode")

nr_quotes = 0
while True:
	# アクション（チェーン）の使用を開始
	action_chain = ActionChains(driver)
	# 名言のブロックに移動
	action_chain.move_to_element(div_element)
	# クリックして操作対象にする
	action_chain.click()
	# Page Downキーを約１０秒押す
	action_chain.send_keys([Keys.PAGE_DOWN for i in range(10)])
	# 以上のアクションを実行する
	action_chain.perform()

	# 少なくともnr_quotes+1個の名言を取得しようとする
	try:
		all_quotes = WebDriverWait(driver, 3).until(
			at_least_n_elements_found(quotes_locator, nr_quotes + 1)
			)
	except TimeoutException as ex:
		# 3秒以内に新しい名言が見つからず、あるのはこれが全部とみなす
		print("...done!")
		break
	# それ以外の場合名言のカウンターを更新する
	nr_quotes = len(all_quotes)
	print("...now seeing", nr_quotes, "quotes")

# all_quotesにはすべての名言の要素が含まれている
print(len(all_quotes), 'quotes found\n')
for quote in all_quotes:
	print(quote.text)

input('Press ENTER to close the automated browser')
driver.quit()
