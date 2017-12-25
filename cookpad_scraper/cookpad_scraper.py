from cookpad_scraper.site_url import SiteUrl
from cookpad_scraper.recipe import Recipe
from cookpad_scraper.recipes import Recipes

import requests
import re

from bs4 import BeautifulSoup

class CookpadScraper():
    def __init__(self, soup=None):
        self.base_url = SiteUrl().cookpad
        self.soup     = None

    def recipe(self, id=None, url=None):
        if (id is None) and (url is None):
            raise ValueError("id or url must be specified")

        if (id is not None):
            self.soup = self._request(self.recipe_url(id))
        else:
            self.soup = self._request(url)

        title         = self.get_title()
        thumbnail_url = self.get_thumbnail_url()
        author_name   = self.get_author_name()

        return Recipe(id, title, thumbnail_url, author_name)

    def get_title(self, soup=None):
        self.set_soup(soup)
        return self.soup.find('h1', 'recipe-title').get_text()

    def get_thumbnail_url(self, soup=None):
        self.set_soup(soup)
        return self.soup.find('img', 'large_photo_clickable')['src']

    def get_author_name(self, soup=None):
        self.set_soup(soup)
        return self.soup.find(id='recipe_author_name').get_text()

    def parse_id(self, url):
        recipe_id_regex = re.compile('.*/recipe\/(\d*)')
        return int(recipe_id_regex.match(url)[1])

    def recipe_url(self, id):
        return self.base_url + '/recipe/' + str(id)

    def set_soup(self, soup):
        self.soup = soup or self.soup

        if self.soup is None:
            raise ValueError("soup must be present")

    # Requests and returns list of original ids of pickup recipes in https://cookpad.com/pickup_recipes
    def pickup_recipes(self):
        soup = self._request(self.base_url + '/pickup_recipes')
        recipes = Recipes()

        # For loops all pickup_recipes
        for pickup_recipe in soup.find_all('div', 'pickup_recipe'):
            # Gets url of a pick_up recipe
            url = self.base_url + pickup_recipe.find('a')['href']
            recipes.append(self.recipe(url=url))

        return recipes

    def _request(self, url):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
