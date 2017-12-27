from cookpad_scraper.site_url import SiteUrl
from cookpad_scraper.ingredients import Ingredients

class Recipe():
    def __init__(self, id, title, thumbnail_url, author_name, ingredients=Ingredients()):
        self.id            = str(id)
        self.title         = title
        self.thumbnail_url = thumbnail_url
        self.author_name   = author_name
        self.url           = SiteUrl().cookpad + '/recipe/' + self.id
        self.ingredients   = ingredients

        if not self.validate_presence_of(['id', 'title', 'thumbnail_url', 'author_name', 'url']):
            raise ValueError('All attributes must not be None')

    # Returns attributes as dictionary
    def to_json(self):
        return {'title': self.title,'thumbnail_url': self.thumbnail_url,
            'original_id': self.id, 'author_name': self.author_name,
            'url': self.url}

    def validate_presence_of(self, properties):
        # If properties are list, validate all
        if type(properties) is list:
            for property in properties:
                # If one or more properties is None returns False
                if eval("self." + property) is None:
                    return False
        # If properties are not list, validates only one property
        else:
            # returns True if the property is not None, otherwise False
            return eval("self." + properties) is not None

        return True

