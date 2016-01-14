from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.allrecipes.com"

def get_recipe_links(section_url):
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")
	article = soup.find("article", "grid-col--fixed-tiles")
	recipe_links = [BASE_URL + article.ng-isolate-scope["href"] for ng-isolate-scope in article.findAll("ng-isolate-scope")]
	return recipe_links

def get_recipe_features(recipe_link):
	html = urlopen(category_links).read()
	soup = BeautifulSoup(html, "lxml")
	title = soup.find("h1", "recipe-summary__h1").string
	rating1 = soup.find("div", "rating-stars").data-ratingstars
	rating2 = summaryGroup.meta["content"]
	times_cooked = soup.find("span", "made-it-count").string
	review_count = soup.find("span", "review-count").string
	ingredient_count = len(soup.findAll("li", "checkList__line")) - 1
	return {"title": title,
			"rating1": rating1,
			"rating2": rating2,
			"times_cooked": times_cooked,
			"review_count": review_count,
			"ingredient_count": ingredient_count}

