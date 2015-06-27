__author__ = 'hammy'

import abc
import inspect
import os
import re
import sys
import traceback
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))

import crawl_settings
from spider_runner import SpiderRunner
from storage_items import IngredientItem, RecipeItem
from food_types import IngredientUse


# -----------------------------------------------------------------------------
# Abstract base class for crawling websites.
# -----------------------------------------------------------------------------
class RecipeSpider(CrawlSpider):
    name = ''
    allowed_domains = []
    start_urls = []
    allowed_link_regex = ''
    rules = ()

    def __init__(self, *args, **kwargs):
        CrawlSpider.__init__(self, *args, **kwargs)

    @abc.abstractmethod
    def get_recipe_name(self, response):
        pass

    @abc.abstractmethod
    def get_ingredients(self, response):
        pass

    @abc.abstractmethod
    def get_servings(self, response):
        pass

    @abc.abstractmethod
    def get_description(self, response):
        pass

    def _extract_recipe_item(self, response):
        name = self.get_recipe_name(response)
        if not name:
            print "No data found at %s" % response.url
            return None
        item = RecipeItem()
        item['name'] = name
        item['servings'] = self.get_servings(response)
        item['url'] = response.url
        item['description'] = self.get_description(response)
        item['ingredients'] = self.get_ingredients(response)
        return item

    def process_webpage(self, response):
        try:
            recipe = self._extract_recipe_item(response)

            if not recipe:
                print 'No recipe found at "%s"' % response.url
                return

            outdir = '%s/extractions' % os.getcwd()
            filename = '%s/%s.txt' % (outdir, response.url.split('/')[-1])

            with crawl_settings.STORAGE_TYPE(filename) as storage:
                print 'Storing Extracted Recipe:'
                print '\tRecipe:    %s' % recipe['name']
                print '\tWebsite:   %s' % response.url
                print '\tFile Name: %s' % storage.get_storage_name()
                storage.write(recipe)
        except Exception as e:
            sys.stderr.write('---------------------------------------\n')
            print traceback.print_exc(file=sys.stderr)
            print type(e)
            sys.stderr.write('---------------------------------------\n')
            raise e


# -----------------------------------------------------------------------------
# Class to extract recipe data from the USDA's "What's Cooking" pages.
# -----------------------------------------------------------------------------
class USDARecipeSpider(RecipeSpider):
    name = 'ingredients'
    allowed_domains = ['whatscooking.fns.usda.gov']
    start_urls = [
        'http://www.whatscooking.fns.usda.gov/search/solr-results'
        #, 'http://www.whatscooking.fns.usda.gov/search/quantity'
    ]

    allowed_link_regex = r'(http\:\/\/www\.whatscooking\.fns\.usda\.gov\/(quantity|solr\-results)\/.*)' \
        '|(http\:\/\/www\.whatscooking\.fns\.usda\.gov\/search\/(quantity|solr\-results)\?keyword.*\d+$)'
    rules = (
        Rule(
            LinkExtractor(allow=allowed_link_regex),
            callback='process_webpage', follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        RecipeSpider.__init__(self, *args, **kwargs)

    @staticmethod
    def __extract_ingredients(response):
        field = response.xpath('//div[contains(@class, "tcell ingredient-name")]/text()')
        if not field:
            field = response.xpath('//div[contains(@class, "ingredient-name")]/text()')
        for selection in field:
            selection = selection.extract().strip()
            yield selection

    @staticmethod
    def __extract_measures(response):
        try:
            amounts = response.xpath('//div[contains(@class, "quantity-unit")]')
            units = response.xpath('//div[contains(@abbr)]/text()')
            for a, u in zip(amounts, units):
                a = a.extract().strip()
                u = u.extract().strip()
                output = a if len(a) else u
                yield output
        except ValueError:
            amounts = response.xpath('//div[contains(@class, "tcell ingredient-lmeasure")]')
            units = response.xpath('//div[contains(@class, "tcell ingredient-lweight")]')
            amountregex = '\<div.*tcell\ ingredient\-lmeasure.*\>(.*)\<\/div\>'
            unitregex = '\<div.*tcell\ ingredient\-lweight.*\>(.*)\<\/div\>'

            for amountpath, unitpath in zip(amounts, units):
                a = re.match(amountregex, amountpath.extract()).group(1).strip()
                u = re.match(unitregex, unitpath.extract()).group(1).strip()
                output = a if len(a) else u
                yield output

    def get_recipe_name(self, response):
        selector = response.xpath('//div/h1[@id="mainPageTitle"]/text()')
        validator = response.xpath('//*[@id="recipeSummaryInfo"]')
        if not validator or not selector:
            return None
        suffix = selector.extract()[0].strip()
        return suffix

    def get_ingredients(self, response):
        results = []
        ingredientlist = USDARecipeSpider.__extract_ingredients(response)
        measurelist = USDARecipeSpider.__extract_measures(response)
        index = 0
        swappable = False

        for i, a in zip(ingredientlist, measurelist):
            ingredient = IngredientItem()
            if not len(i) and not len(a):
                continue

            if i == 'OR':
                swappable = True
                continue

            if i.lower().find('optional') is not -1:
                ingredient['use'] = IngredientUse.OPTIONAL
            else:
                if not swappable:
                    ingredient['use'] = IngredientUse.REQUIRED
                else:
                    ingredient['use'] = IngredientUse.SWAPPABLE
                    results[-1]['use'] = IngredientUse.SWAPPABLE
                    index -= 1
            ingredient['food'] = i
            ingredient['amount'] = a
            ingredient['index'] = index
            index += 1
            swappable = False
            results.append(ingredient)
        return results

    def get_description(self, response):
        selector = response.xpath('//div[contains(@class, "recipe_source")]/text()')
        return selector.extract()[0].strip()

    def get_servings(self, response):
        selector = response.xpath('//div[contains(@class, "r_summary_block")]/div/text()')
        return selector.extract()[0].strip()


if __name__ == '__main__':
    runner = SpiderRunner(USDARecipeSpider())
    runner.runSpider()
