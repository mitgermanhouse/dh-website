from django.core.management.base import BaseCommand, CommandError
from recipes.models import Recipe, Ingredient
from bs4 import BeautifulSoup
import urllib2
import re


class Command(BaseCommand):

    def scrape_recipe(self, link):
        soup = BeautifulSoup(urllib2.urlopen('http://dh.scripts.mit.edu' + link).read())

        h2 = soup.find_all('h2')
        for label in h2:
            if "Serves:" in label.getText():
                serving_size = label.getText().split(" ")[1]
        tr = soup.find_all('tr')
        all_ingredients = []
        for row in tr:
            ing = row.find_all('td')
            if len(ing) == 3:
                ingredient = []
                for td in ing:
                    ingredient.append(td.getText())
                all_ingredients.append(ingredient)
        directions = soup.find('div', attrs={'class': 'code'}).getText()

        title = soup.find('h1').getText()
        print(directions)
        return {"title": self.replace_space(title), "serving_size": serving_size, "ingredients": all_ingredients,
                "directions": directions}

    def replace_space(self, text):
        text = re.sub(r'^[ \t\n]+', '', text)
        text = re.sub(r'$[ \t\n]+', '', text)
        return text

    def handle(self, *args, **options):
        url = 'http://dh.scripts.mit.edu/essen/recipes/'
        soup = BeautifulSoup(urllib2.urlopen(url).read())

        pattern = re.compile("[\/]essen[\/]recipes[\/][0-9]+[\/][0-9]+")

        links = []
        l = soup.find_all("a")
        for link in l:
            link_text = link.get('href')
            if link_text != None:
                if pattern.search(link_text) != None:
                    links.append(link_text)

        count = 0
        for link in links:
            count += 1
            d = self.scrape_recipe(link)

            if len(d['ingredients']) != 0:
                self.add_recipe(d)
                print(d['title'].encode('utf-8') + " added." + str(count) + " of " + str(len(links)) + " complete")

    def add_recipe(self, d):
        r = Recipe(recipe_name=d['title'].encode('utf-8'),
               directions=d['directions'].encode('utf-8'),
               serving_size=int(d['serving_size'].encode('utf-8')))
        r.save()

        for i in d['ingredients']:
            Ingredient(recipe=r,
                       ingredient_name=i[0].encode('utf-8'),
                       quantity=float(i[1].encode('utf-8')),
                       units=i[2].encode('utf-8')).save()



