# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from fractions import Fraction
from scrapy import exceptions


class RecipeFilterPipeline(object):
    def __init__(self):
        self.filters = [
            'cup',
            'tablespoon',
            'teaspoon',
            'spoonful',
            'can',
            'ingredients',
            'vegetable',
            'snack',
            'squash'
        ]

    def __is_quantity(self, word):
        if word.isdigit():
            return True
        try:
            num = float(Fraction(word))
            print 'Converted "%s" to "%f"' % (word, num)
            return True
        except Exception as e:
            print e
            return False

    def process_item(self, item, spider):
        for word in self.filters:
            desc = unicode(item['ingredients']).lower()
            if word in desc or self.__is_quantity(desc):
                raise scrapy.exceptions.DropItem('Word Filtered: %s' % word)
            else:
                return item
