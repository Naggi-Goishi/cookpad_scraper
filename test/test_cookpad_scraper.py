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

    def test_get_ingredients(self):
        soup = self.cookpad._request(self.cookpad.recipe_url(self.recipe_id))
        ingredients = self.cookpad.get_ingredients(soup)
        self.assertTrue(len(ingredients) > 0, 'Failed to get ingredients from recipe show page')

    # def test_all_main_categories(self):
    #     categories = self.cookpad.all_main_categories()
    #     self.assertTrue(len(categories) > 0, 'Failed to get all main categories')

    # def test_recipes_from_category_page(self):
    #     categories = self.cookpad.all_main_categories()

    #     for category in categories:
    #         print('#', end='')
    #         recipes = self.cookpad.recipes_from_category_page(category.soup)
    #         self.assertTrue(len(recipes) > 0, 'Failed to load recipes from category page')




