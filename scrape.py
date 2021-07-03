import requests
from bs4 import BeautifulSoup
import sys
import os
import json
import time
import datetime

HISTROY_FILE = f'{os.path.realpath(__file__)}{os.sep}history.json'

def in_history(url):
	today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if os.path.exists(HISTROY_FILE):
		history = f.read()
		json.loads(history)
		if url in history:
			return True
		else:
			with open(HISTROY_FILE, 'w') as f:
				history[url] = today
				history = json.dumps(history)
				f.write(history)
			return False
		
	else:
		with open(HISTROY_FILE, 'w') as f:
			history = json.dumps({url: today})
			f.write(history)
		return False

def save(datestamp, ticker, url):
	today = datetime.datetime.now()
	with open(f'{os.path.realpath(__file__)}{os.sep}{today}.txt', 'a') as f:
		f.write(f'{datestamp} {ticker} {url}')

def get_html(url):
	r = requests.get(url)
	if r.status_code == 200:
		return BeautifulSoup(r.text, 'html.parser')
	else:
		return False

def main(url, search):
	soup = get_html(url)
	if soup:
		rows = soup.find_all('tr', class_='Periodicals')
		for row in rows:
			if row != ' ' and row != None:
				headline = row.find('div', class_='story_header')
				if headline != None:
					headlineText = headline.find('span').text.strip()
					if search.upper() in headlineText.upper():
						datestamp, timestamp = row['data-datenews'].split()
						article_url = headline.find('a', class_='newsTitleLink')['href']
						ticker = row.find('span', class_='ticker').next_element
						print(headlineText)
						if not in_history(url):
							save(datestamp, ticker, url)

	else:
		print(f' [!] Error 01: unable to read data from {url}')

if __name__ == '__main__':
	arguments = sys.argv
	if len(arguments) > 1:
		url = 'https://thefly.com/news.php'
		search = arguments[1]
		main(url, search)

	else:
		print(' Usage:\n    python scrape.py "phrase to find"')