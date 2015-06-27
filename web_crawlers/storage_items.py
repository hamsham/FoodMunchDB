# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IngredientItem(scrapy.Item):
    food = scrapy.Field(serializer=unicode)
    amount = scrapy.Field(serializer=unicode)
    index = scrapy.Field(serializer=int)
    use = scrapy.Field(serializer=int)


class RecipeItem(scrapy.Item):
    name = scrapy.Field(serializer=unicode)
    description = scrapy.Field(serializer=unicode)
    url = scrapy.Field(serializer=unicode)
    servings = scrapy.Field(serializer=unicode)
    ingredients = scrapy.Field(serializer=list)  # IngredientItem
