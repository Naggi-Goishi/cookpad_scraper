from setuptools import setup

setup(
   name='cookpad_scraper',
   version='0.0',
   description='Make it easy to scrape cookpad web site with python',
   author='Naggi Goishi',
   author_email='naggi@kakaxi.jp',
   packages=['cookpad_scraper'],  #same as name
   install_requires=['beautifulsoup4', 'requests'], #external packages as dependencies
)
