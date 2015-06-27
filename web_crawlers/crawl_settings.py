# -*- coding: utf-8 -*-

# Scrapy settings for recipe project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'recipe_spider'

LOG_FILE = 'crawler.log'

SPIDER_MODULES = ['spiders.recipe_spiders']
NEWSPIDER_MODULE = 'spiders.recipe_spiders'
DEFAULT_ITEM_CLASS = ['data_items.Website']
ITEM_PIPELINE = {'data_pipelines.RecipeFilterPipeline': 1}

import recipe_storage
#STORAGE_TYPE = recipe_storage.SqlRecipeStorage
STORAGE_TYPE = recipe_storage.TextRecipeStorage

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recipe (+http://www.yourdomain.com)'
