from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import string
import pickle

BASE_URL = "http://www.allrecipes.com"
SITEMAP_URL = "http://dish.allrecipes.com/faq-sitemap/"
SITEMAP_PICKLE = "allrecipes_sitemap.pickle"
RECIPE_LINKS_PICKLE = 'allrecipes_recipes.pickle'
RECIPE_INGREDIENTS_PICKLE = 'recipe_ingredients.pickle'
PATH_TO_CHROMEDRIVER = '/Users/charlesfarr/desktop/chromedriver' #Update

def sitemap_scraper(sitemap_url):
	## BeautifulSoup setup
	html = urlopen(sitemap_url).read()
	soup = BeautifulSoup(html,"lxml")

	#empty list for collecting links
	links = []

	#filter all links - append only those that are indexes of recipes
	for link in soup.find_all('a'):
		if '/recipes/' in unicode(link):
			links.append(link.get('href').encode('ascii','ignore'))

	# dump to pickle file of indexes
	with open(SITEMAP_PICKLE,'wb') as f:
		pickle.dump(links, f, pickle.HIGHEST_PROTOCOL)

def recipe_index_scraper(section_url):

	# THIS IS WHERE IT WOULD BE VALUABLE TO FIGURE OUT HOW TO OVERRIDE THE INFINITE SCROLL
		# simpliest way would be to use the '?page=#' at the end, it will be necessary to use Selenium here "http://allrecipes.com/recipes/15876/us-recipes/southern/?page=9" 

	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")
	links = []
	for link in soup.find_all('a'):
		if '/recipe/'in unicode(link):
			links.append(BASE_URL + link.get('href').encode('ascii','ignore'))

	cleanLinks = list(set(links))
	return cleanLinks

	############ Taken from NYT Scraper - need to figure out how to redirect same browser window
	# browser = webdriver.Chrome(executable_path = PATH_TO_CHROMEDRIVER)
	# browser.get(search_results)
	
	# soup = BeautifulSoup(browser.page_source,'lxml')
	# results = soup.find('div', class_='searchResults')
	# thumbs = results.find_all('li')
	
	# article_links = []
	# #article_authors = []

	# for thumb in thumbs:
	# 	#author = thumb.find('span',class_='byline').contents
	# 	ele = thumb.find('div', class_="element2")
	# 	link = ele.find('a').get('href')

	# 	article_links.append(str(link))
	# 	#article_authors.append(str(author))

	browser.close()
	return article_links #, article_authors

def recipe_page_scraper(recipe_link):
	return "deadass"

def link_parser(link):
	stripped_link = link[29:35]

	if stripped_link[len(stripped_link) - 1] == '/':
		return stripped_link[:(len(stripped_link) - 1)]
	else:
		return stripped_link

def main():
	# Open the pickled LIST of recipe indices
	index_links = []
	with open(SITEMAP_PICKLE, 'rb') as f:
		index_links = pickle.load(f)

	full_index_links = []
	for link in index_links:
		new_link = BASE_URL + link
		full_index_links.append(new_link)

	recipe_links = []
	for link in full_index_links:
		ind_recp_links = recipe_index_scraper(link)

	# Open the pickled LIST of recipe links
	recipe_links = []
	with open(RECIPE_LINKS_PICKLE,'rb') as f:
		recipe_links = pickle.load(f)

	# Open the pickled DICTIONARY of recipe ingredients
	recipe_ingredients = {}
	with open(RECIPE_INGREDIENTS_PICKLE,'wb') as f:
		pickle.dump(links, f, pickle.HIGHEST_PROTOCOL)


########### Order of Execution
# 1. sitemap_scraper(SITEMAP_URL)
# 2. call recipe_index_scraper() on ALL links returned from sitemap_scraper

# def get_recipe_features(recipe_link):
# 	#print(recipe_link)
# 	html = urlopen(recipe_link).read()
# 	soup = BeautifulSoup(html, "lxml")
# 	title = soup.find("h1", "recipe-summary__h1").string
# 	#print(title)
# 	times_cookedString = unicode(soup.find("div", "total-made-it")["data-ng-init"])
# 	times_cookedString = times_cookedString[5:]
# 	times_cookedString = times_cookedString[:-1]
# 	times_cooked = int(times_cookedString)
# 	#print(times_cooked)
# 	rating = soup.find(attrs = {'class':'recipe-summary__stars'}).find('div')['data-ratingstars']
# 	#print(rating)
# 	review_count = soup.find("span", "review-count").string
# 	#print(review_count)
# 	ingredient_count = len(soup.findAll("li", "checkList__line")) - 1
# 	#print(ingredient_count)
# 	return {"link": recipe_link,
# 			"title": title,
# 			"rating": rating,
# 			"times_cooked": times_cooked,
# 			"review_count": review_count,
# 			"ingredient_count": ingredient_count}

# def main():
# 	recipeLinks = get_recipe_links(BASE_URL)

# 	with open('recipeData.csv','w') as csvfile:
# 		fieldnames = ['title', 'rating','times_cooked', 'review_count', 'ingredient_count','link']
# 		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 		writer.writeheader()
# 		for x in range(len(recipeLinks)):
# 			recipeData = get_recipe_features(recipeLinks[x])
# 			writer.writerow({
# 				'title': recipeData['title'],
# 				'rating':recipeData['rating'],
# 				'times_cooked': recipeData['times_cooked'],
# 				'review_count': recipeData['review_count'],
# 				'ingredient_count':recipeData['ingredient_count'],
# 				'link':recipeData['link']})

# def addtoCSV():
# 	allListLinks = ['http://allrecipes.com/recipes/105/appetizers-and-snacks/dips-and-spreads/?internalSource=hub%20nav&referringId=76&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202','http://allrecipes.com/recipes/104/appetizers-and-snacks/cheese/?internalSource=hub%20nav&referringId=76&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202','http://allrecipes.com/recipes/107/appetizers-and-snacks/meat-and-poultry/?internalSource=hub%20nav&referringId=76&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202','http://allrecipes.com/recipes/116/appetizers-and-snacks/spicy/?internalSource=hub%20nav&referringId=76&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202','http://allrecipes.com/recipes/108/appetizers-and-snacks/seafood/?internalSource=hub%20nav&referringId=76&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202','http://allrecipes.com/recipes/17146/appetizers-and-snacks/snacks/?internalSource=hub%20nav&referringId=76&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']
# 	for x in range(len(allListLinks)):
# 		recipeLinks = get_recipe_links(allListLinks[x])
# 		with open('recipeData.csv','a') as csvfile:
# 			fieldnames = ['title', 'rating','times_cooked', 'review_count', 'ingredient_count','link']
# 			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 			for x in range(len(recipeLinks)):
# 				recipeData = get_recipe_features(recipeLinks[x])
# 				writer.writerow({
# 					'title': recipeData['title'],
# 					'rating':recipeData['rating'],
# 					'times_cooked': recipeData['times_cooked'],
# 					'review_count': recipeData['review_count'],
# 					'ingredient_count':recipeData['ingredient_count'],
# 					'link':recipeData['link']})

# def addMoreToCSV():
# 	#allListLinks = ['http://allrecipes.com/recipes/153/breakfast-and-brunch/eggs/quiche/?internalSource=hub%20nav&referringId=148&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/1308/breakfast-and-brunch/eggs/scrambled-eggs/?internalSource=hub%20nav&referringId=148&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/1564/breakfast-and-brunch/eggs/frittata/?internalSource=hub%20nav&referringId=148&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/1314/breakfast-and-brunch/eggs/omelets/?internalSource=hub%20nav&referringId=148&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']

# 	#allListLinks = ['http://allrecipes.com/recipes/17199/breakfast-and-brunch/eggs/breakfast-sandwiches/?internalSource=hub%20nav&referringId=148&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/1307/breakfast-and-brunch/eggs/breakfast-strata/?internalSource=hub%20nav&referringId=148&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/659/meat-and-poultry/chicken/chicken-breasts/?internalSource=hub%20nav&referringId=201&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/664/meat-and-poultry/chicken/baked-and-roasted/?internalSource=hub%20nav&referringId=201&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']

# 	#allListLinks = ['http://allrecipes.com/recipes/662/meat-and-poultry/chicken/whole-chicken/?internalSource=hub%20nav&referringId=201&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/649/meat-and-poultry/chicken/chicken-salad/?internalSource=hub%20nav&referringId=201&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/661/meat-and-poultry/chicken/chicken-thighs/?internalSource=hub%20nav&referringId=201&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/663/meat-and-poultry/chicken/chicken-wings/?internalSource=hub%20nav&referringId=201&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']

# 	#allListLinks = ['http://allrecipes.com/recipes/362/desserts/cookies/?internalSource=hub%20nav&referringId=79&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/836/desserts/cookies/bar-cookies/?internalSource=hub%20nav&referringId=362&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/847/desserts/cookies/fruit-cookies/?internalSource=hub%20nav&referringId=362&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/845/desserts/cookies/international-cookies/?internalSource=hub%20nav&referringId=362&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202'] 

# 	allListLinks = ['http://allrecipes.com/recipes/844/desserts/cookies/cut-out-cookies/?internalSource=hub%20nav&referringId=362&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/839/desserts/cookies/chocolate-chip-cookies/?internalSource=hub%20nav&referringId=362&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/265/everyday-cooking/vegetarian/main-dishes/?internalSource=hub%20nav&referringId=87&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/264/everyday-cooking/vegetarian/side-dishes/?internalSource=hub%20nav&referringId=87&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']
# 	linksToSave = ['http://allrecipes.com/recipes/263/everyday-cooking/vegetarian/appetizers/?internalSource=hub%20nav&referringId=87&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/17684/everyday-cooking/vegetarian/whole-grain/?internalSource=hub%20nav&referringId=87&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/266/everyday-cooking/vegetarian/soups-and-stews/?internalSource=hub%20nav&referringId=87&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202', 'http://allrecipes.com/recipes/155/everyday-cooking/vegetarian/breakfast-and-brunch/?internalSource=hub%20nav&referringId=87&referringContentType=recipe%20hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']

# 	for x in range(len(allListLinks)):
# 		recipeLinks = get_recipe_links(allListLinks[x])
# 		with open('recipeData.csv','a') as csvfile:
# 			fieldnames = ['title', 'rating','times_cooked', 'review_count', 'ingredient_count','link']
# 			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 			for x in range(len(recipeLinks)):
# 				recipeData = get_recipe_features(recipeLinks[x])
# 				writer.writerow({
# 					'title': recipeData['title'],
# 					'rating':recipeData['rating'],
# 					'times_cooked': recipeData['times_cooked'],
# 					'review_count': recipeData['review_count'],
# 					'ingredient_count':recipeData['ingredient_count'],
# 					'link':recipeData['link']})

