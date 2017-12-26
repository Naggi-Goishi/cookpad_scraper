from cookpad_scraper.recipes import Recipes

class Category():
    def __init__(self, id, name, soup=None, recipes=Recipes()):
        self.id   = id
        self.name = name
        self.recipes = recipes
        self.soup    = soup
