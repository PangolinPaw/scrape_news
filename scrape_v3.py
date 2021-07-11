# Browser automation:
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
# HTML processing:
from bs4 import BeautifulSoup
# Data handing:
import csv
import sys
import os
import json
# Delays & datestamps:
import time
import datetime

# Set this for your particular installation:
PATH_TO_FIREFOX = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe' 


THIS_DIR = f'{os.path.split(os.path.abspath(__file__))[0]}{os.sep}'
URL = 'https://thefly.com/news.php'
DELAY = 1
driver = None

def load_page():
	global driver
	print(' [Opening browser]')
	binary = FirefoxBinary(PATH_TO_FIREFOX)
	driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'geckodriver.exe')
	driver.get(URL)
	accept_cookeis()

def accept_cookeis():
	waitCount = 0
	acceptCookies = []
	while len(acceptCookies) == 0:
		acceptCookies = driver.find_elements_by_css_selector('button')
		time.sleep(DELAY)
		waitCount += 1
		if waitCount > 10:
			break
	if len(acceptCookies) > 0:
		acceptCookies[0].click()

def scroll_down():
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scrape_articles(search):
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	rows = soup.find_all('tr')
	saved_results = 0
	for row in rows:
		if row != ' ' and row != None:
			headline = row.find('div', class_='story_header')
			if headline != None:
				headlineText = headline.find('span').text.strip()
				if search.upper() in headlineText.upper():
					print(f' [+] Matching article found: "{headlineText}"')

					datestamp, timestamp = row['data-datenews'].split()
					article_url = headline.find('a', class_='newsTitleLink')['href']
					ticker = row.find('span', class_='ticker')
					if ticker != None:
						ticker = ticker.next_element
					if not in_history(article_url):
						print('     Novel article, saving to file')
						save_article_data(datestamp, ticker, article_url)
						saved_results += 1
					else:
						print('     Article encountered before, ignoring')
	print( f' [i] {saved_results} articles saved.')

def in_history(url):
	history_file = f'{THIS_DIR}history.json'
	today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if os.path.exists(history_file):
		with open(history_file, 'r') as f:
			history = f.read()
			history = json.loads(history)
		if url in history:
			return True
		else:
			with open(history_file, 'w') as f:
				history[url] = today
				history = json.dumps(history, indent=4)
				f.write(history)
			return False
		
	else:
		with open(history_file, 'w') as f:
			history = json.dumps({url: today}, indent=4)
			f.write(history)
		return False

def save_article_data(datestamp, ticker, url):
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	with open(f'{THIS_DIR}{today}.txt', 'a') as f:
		f.write(f'{datestamp} {ticker} {url}\n')

def main(search):
	load_page()
	time.sleep(DELAY)
	scroll_down()
	time.sleep(DELAY * 5)
	scrape_articles(search)
	driver.quit()

if __name__ == '__main__':
	arguments = sys.argv
	if len(arguments) > 1:
		search = arguments[1]
		if len(arguments) > 2:
			interval = int(arguments[2])
			print(f' [Repeating search every {interval} minutes]')
			run_num = 0
			while True:
				run_num += 1
				print(f' [i] Run {run_num}')
				main(search)
				for x in range(interval * 60):
					print(f'\r [Next run in {(interval * 60) - (x + 1)} seconds]  ', end='')
					time.sleep(1)
				print()
				print()
		else:
			print(' [Executing single search]')
			main(search)
	else:
		print('''
  Usage:
	python scrape.py "<search term>" [interval]

	search term			A word or phrase which articles must contain.
	interval			(Optional) The number of minutes between each repetition
					of the search. If blank, seach is completed only once.''')