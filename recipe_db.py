__author__ = 'hammy'

import sys
import sqlite3
import hashlib
import inspect
import os
import traceback


class RecipeDB:
    CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    DATABASE_PATH = '%s/FoodData.db' % CURRENT_DIR

    def __init__(self):
        print "Opening database connection to '%s'" % RecipeDB.DATABASE_PATH
        self.connection = sqlite3.connect(database=RecipeDB.DATABASE_PATH)
        self.connection.text_factory = sqlite3.OptimizedUnicode

    def close(self):
        self.connection.close()

    def __delete_recipe(self, recipeid):
        recipeid = str(recipeid)
        recipequery = 'DELETE FROM recipes WHERE id=?;'
        recipecursor = self.connection.cursor()
        recipecursor.execute(recipequery, (recipeid,))
        recipecursor.close()
        foodquery = 'DELETE FROM ingredients WHERE recipe_id=?;'
        foodcursor = self.connection.cursor()
        foodcursor.execute(foodquery, (recipeid,))
        foodcursor.close()

    def __insert_recipe(self, hashid, recipeitem):
        name = recipeitem['name']
        address = recipeitem['url']
        servings = recipeitem['servings']
        recipedata = (name, servings, address, hashid)
        recipequery = 'INSERT INTO recipes (recipe, servings, address, recipe_sha256) VALUES(?, ?, ?, ?);'
        self.connection.execute(recipequery, recipedata)

        locatequery = 'SELECT id FROM recipes WHERE recipe_sha256=?;'
        recipeid = self.connection.execute(locatequery, (hashid,)).fetchone()[0]

        def ingredient_iter():
            for ingredient in recipeitem['ingredients']:
                food = ingredient['food']
                amount = ingredient['amount']
                index = ingredient['index']
                use = ingredient['use']
                yield (recipeid, amount, use, index, food)
        itemquery = 'INSERT INTO ingredients (recipe_id, amount, use, swap_index, name) VALUES(?, ?, ?, ?, ?);'
        self.connection.executemany(itemquery, ingredient_iter())

    def insert_recipe(self, recipeitem):
        name = recipeitem['name']
        hashid = hashlib.sha256()
        hashid.update(name.encode('unicode_escape'))
        hashid = hashid.hexdigest()
        query = 'SELECT id FROM recipes WHERE recipe_sha256=?;'
        cursor = self.connection.cursor()
        cursor.execute(query, (hashid,))
        idlist = cursor.fetchall()
        try:
            for recipeid in idlist:
                self.__delete_recipe(recipeid)
            self.__insert_recipe(hashid, recipeitem)
            self.connection.commit()
        except sqlite3.InterfaceError as e:
            self.connection.rollback()
            sys.stderr.write('---------------------------------------\n')
            print traceback.print_exc(file=sys.stderr)
            sys.stderr.write('---------------------------------------\n')
            raise e


if __name__ == '__main__':
    print RecipeDB.DATABASE_PATH
