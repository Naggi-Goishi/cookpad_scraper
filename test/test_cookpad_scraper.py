import unittest

from cookpad_scraper import CookpadScraper
from cookpad_scraper import Recipe

class CookpadScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.cookpad   = CookpadScraper()
        self.recipe_id = 1785529

    def test_recipe(self):
        recipe = self.cookpad.recipe(id=self.recipe_id)
        self.assertTrue(type(recipe) is Recipe, 'Failed to get recipe whose id is: ' + str(self.recipe_id))

    def test_pickup_recipes(self):
        self.assertTrue(len(self.cookpad.pickup_recipes()) > 0, 'Failed to get pickup_recipes')
