import requests
from bs4 import BeautifulSoup
import sys
import os
import json
import time
import datetime

THIS_DIR = f'{os.path.split(os.path.abspath(__file__))[0]}{os.sep}'

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

def save(datestamp, ticker, url):
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	with open(f'{THIS_DIR}{today}.txt', 'a') as f:
		f.write(f'{datestamp} {ticker} {url}\n')

def get_html(url):
	r = requests.get(url)
	if r.status_code == 200:
		return BeautifulSoup(r.text, 'html.parser')
	else:
		return False

def main(url, search):
	soup = get_html(url)
	saved_results = 0
	if soup:
		rows = soup.find_all('tr', class_='news')
		for row in rows:
			if row != ' ' and row != None:
				headline = row.find('div', class_='story_header')
				if headline != None:
					headlineText = headline.find('span').text.strip()
					if search.upper() in headlineText.upper():
						print(f' [+] Matching article found: "{headlineText}"')

						datestamp, timestamp = row['data-datenews'].split()
						article_url = headline.find('a', class_='newsTitleLink')['href']
						ticker = row.find('span', class_='ticker').next_element
						if not in_history(article_url):
							print('     Novel article, saving to file')
							save(datestamp, ticker, article_url)
							saved_results += 1
						else:
							print('     Article encountered before, ignoring')
		print( f' [i] {saved_results} articles saved.')

	else:
		print(f' [!] Error 01: unable to read data from {url}')

if __name__ == '__main__':
	arguments = sys.argv
	if len(arguments) > 1:
		url = 'https://thefly.com/news.php'
		search = arguments[1]
		if len(arguments) > 2:
			interval = int(arguments[2])
			print(f' [Repeating search every {interval} minutes]')
			run_num = 0
			while True:
				run_num += 1
				print(f' [i] Run {run_num}')
				main(url, search)
				for x in range(interval * 60):
					print(f'\r [Next run in {(interval * 60) - (x + 1)} seconds]  ', end='')
					time.sleep(1)
				print()
				print()
		else:
			print(' [Executing single search]')
			main(url, search)

	else:
		print('''
 Usage:
   python scrape.py "<search term>" [interval]

   search term			A word or phrase which articles must contain.
   interval			(Optional) The number of minutes between each repetition
 				of the search. If blank, seach is completed only once.''')