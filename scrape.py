from  urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys, time, threading


def get_review(req):
	try : 
		with urlopen(req) as response : 
			wine = response.read()
		soup = BeautifulSoup(wine, 'lxml')
		wine_name = soup.find('div', class_='article-title').string
		descr = soup.find('p', class_='description').string
		price = soup.find('span', string='Price').parent.next_sibling.next_sibling.get_text(" ", strip=True).split(',')[0][1:]
		variety = soup.find('span', string='Variety').parent.next_sibling.next_sibling.get_text(strip=True).split(',')
		appellation = soup.find('span', string='Appellation').parent.next_sibling.next_sibling.get_text(strip=True)
		winery = soup.find('span', string='Winery').parent.next_sibling.next_sibling.get_text(strip=True)
		alcohol = soup.find('span', string='Alcohol').parent.next_sibling.next_sibling.get_text(strip=True)
		bottle_size = soup.find('span', string='Bottle Size').parent.next_sibling.next_sibling.get_text(strip=True)
		category = soup.find('span', string='Category').parent.next_sibling.next_sibling.get_text(strip=True)
		usr_rating = soup.find('span', string='User Avg Rating').parent.next_sibling.next_sibling.get_text(strip=True)
		reviewer = soup.find('div', class_='twitter-handle').string
		review = [wine_name,descr, price, variety, appellation, winery, alcohol, bottle_size, category, usr_rating,reviewer]
		return review
	except Exception as e:
		print (repr(e))
	
def get_pages(base_url, pages):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = {'User-Agent': user_agent}
	columns = ['wine_name','descr', 'price', 'variety', 'appellation', 'winery', 'alcohol', 'bottle_size', 'category', 'usr_rating','reviewer']
	wine_review = pd.DataFrame(columns=columns)
	for i in range(pages) : 
		start = time.clock()
		url = base_url+'&page='+str(i+1)
		req = Request(url, headers=headers)
		with urlopen(req) as response:
			html = response.read()
		soup = BeautifulSoup(html, 'lxml')
		links = [url['href'] for url in soup.find_all('a', class_='review-listing')]
		for link in links : 
			wine_review.loc[wine_review.shape[0]] = get_review(Request(link, headers=headers))
		print ("Page "+str(i+1))
	wine_review.to_csv('wine_review.csv', na_rep='NA')


def scrape():	
	no_pages = 100
	base_url = 'http://www.winemag.com/?s=&drink_type=wine'
	start = time.time()
	get_pages(base_url, no_pages)
	print((time.time()-start)/60)

if __name__ == '__main__' : 
	scrape()
