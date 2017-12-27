from cookpad_scraper.site_url import SiteUrl
from cookpad_scraper.recipe import Recipe
from cookpad_scraper.recipes import Recipes
from cookpad_scraper.category import Category
from cookpad_scraper.categories import Categories
from cookpad_scraper.ingredient import Ingredient
from cookpad_scraper.ingredients import Ingredients

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

        if (id is None):
            id = self.parse_recipe_id(url)

        self.soup = self._request(self.recipe_url(id))

        title         = self.get_title()
        thumbnail_url = self.get_thumbnail_url()
        author_name   = self.get_author_name()
        ingredients   = self.get_ingredients()

        return Recipe(id, title, thumbnail_url, author_name, ingredients=ingredients)

    def category(self, id=None, url=None, name=None):
        if (id is None) and (url is None):
            raise ValueError("id or url must be specified")

        if (id is None):
            id = self.parse_category_id(url)

        self.soup = self._request(self.category_url(id))

        if name is None:
            name = self.soup.find('h1', 'category_title').get_text()

        return Category(id, name, self.soup)

    def recipes_from_category_page(self, soup=None):
        self.set_soup(soup)
        urls = []
        recipes = Recipes()

        while True:
            recipe_titles = self.soup.find_all('a', 'recipe-title')
            next_page     = self.soup.find('a', 'next_page')

            if next_page is None:
                break

            for recipe_title in recipe_titles:
                urls.append(self.base_url + recipe_title['href'])

            self.soup = self._request(self.base_url + next_page['href'])

        for url in urls:
            recipes.append(self.recipe(url=url))

        return recipes

    def get_title(self, soup=None):
        self.set_soup(soup)
        return self.soup.find('h1', 'recipe-title').get_text()

    def get_thumbnail_url(self, soup=None):
        self.set_soup(soup)
        return self.soup.find('img', 'large_photo_clickable')['src']

    def get_author_name(self, soup=None):
        self.set_soup(soup)
        return self.soup.find(id='recipe_author_name').get_text()

    def get_ingredients(self, soup=None):
        self.set_soup(soup)
        names = self.soup.find_all('div', 'ingredient_name')
        quantities = self.soup.find_all('div', 'ingredient_quantity')
        ingredients = Ingredients()

        if len(names) != len(quantities):
            raise Exception('The name and quantities are not same')

        for i in range(0, len(names)):
            ingredients.append(Ingredient(names[i].get_text(), quantities[i].get_text()))

        return ingredients

    def parse_recipe_id(self, url):
        recipe_id_regex = re.compile('.*/recipe\/(\d*)')
        return int(recipe_id_regex.match(url)[1])

    def parse_category_id(self, url):
        recipe_id_regex = re.compile('.*/category\/(\d*)')
        return int(recipe_id_regex.match(url)[1])

    def recipe_url(self, id):
        return self.base_url + '/recipe/' + str(id)

    def category_url(self, id):
        return self.base_url + '/category/' + str(id)

    def set_soup(self, soup):
        self.soup = soup or self.soup

        if self.soup is None:
            raise ValueError("soup must be present")

    # Requests and returns Recipes of pickup recipes in https://cookpad.com/pickup_recipes
    def pickup_recipes(self):
        soup = self._request(self.base_url + '/pickup_recipes')
        recipes = Recipes()

        # For loops all pickup_recipes
        for pickup_recipe in soup.find_all('div', 'pickup_recipe'):
            # Gets url of a pick_up recipe
            url = self.base_url + pickup_recipe.find('a')['href']
            recipes.append(self.recipe(url=url))

        return recipes

    # Requests and returns Recipes in all main categories in https://cookpad.com/category/list
    def all_main_categories(self):
        soup = self._request(self.base_url + '/category/list')

        # Get all sub categorie's title
        titles = soup.find_all('h2', 'sub_category_title')

        categories = Categories()

        # Loop through titles and get category name and href
        for title in titles:
            href = title.contents[1]['href']
            category = title.get_text()
            url = self.base_url + href

            categories.append(self.category(url=url))

        return categories


    def _request(self, url):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
