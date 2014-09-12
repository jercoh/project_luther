from scraper import Scraper
from bs4 import BeautifulSoup
import csv, re

awards_base_url = "http://data.newsday.com/long-island/data/entertainment/movies/oscar-winners-history/?q=&searchField=actorDirectorName&fieldSelect-result=&fieldSelect-category=&fieldSelect-year=&currentRecord="

class AwardScraper(Scraper):
	def __init__(self, base_url = awards_base_url, search_url = ""):
		Scraper.__init__(self, base_url, search_url)
		self.file = open('academy_awards.csv', 'wb')
		self.writer = csv.writer(self.file, delimiter='\t')
		self.writer.writerow(['Year', 'Category', 'Won', 'FilmName', 'ActorDirectorName'])
		self.soup = self.connect(base_url)
		self.next_record = '1'

	def scrape_page(self):
		table = self.soup.find("table", { "id" : "sdb-results" })
		trs = table.find_all("tr")
		for i in range(1,len(trs)):
			tr = trs[i]
			year = self.get_year(tr)
			category = self.get_category(tr)
			won = self.get_won(tr)
			film_name = self.get_film_name(tr)
			actor_director_name = self.get_actor_director_name(tr)
			row = [year, category, won, film_name, actor_director_name]
			self.writer.writerow(row)

	def get_year(self, row):
		year = row.find('td', {'class': re.compile('year$')}).text
		return int(year)

	def get_category(self, row):
		return row.find('td', {'class': re.compile('category$')}).text

	def get_won(self, row):
		won = row.find('td', {'class': re.compile('result$')}).text
		return self.str2bool(won)

	def get_film_name(self, row):
		film_name = row.find('a', {'href': re.compile('(filmName)')}).text
		return film_name.replace('\"', '')

	def get_actor_director_name(self, row):
		return row.find('a', {'href': re.compile('(actorDirectorName)')}).text

	def get_next_page(self):
		if self.next_record == '1001':
				return '1051'
		else:
			select = self.soup.find('select', {'name': 'currentRecord'})
			option = select.find('option', {'selected': 'SELECTED'})
			next_option = option.findNextSibling()
			if next_option:
				return next_option['value']
			else:
				return None

	def get_current_page(self):
		select = self.soup.find('select', {'name': 'currentRecord'})
		option = select.find('option', {'selected': 'SELECTED'})
		return option['value']

	def scrape_all(self):
		while self.get_next_page():
			self.next_record = self.get_next_page()
			self.scrape_page()
			self.soup = self.connect(awards_base_url+self.next_record)
		self.soup = self.connect(awards_base_url+self.next_record)
		self.scrape_page()

