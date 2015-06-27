__author__ = 'hammy'

import abc
import codecs
import sys
import inspect
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)
from food_types import IngredientUse
from recipe_db import RecipeDB


# -----------------------------------------------------------------------------
# Abstract base class for storing recipe data.
# -----------------------------------------------------------------------------
class RecipeStorage:
    """
    A RecipeStorage object is a write-only storage object which inputs a
    storage_item.RecipeStorage object to the particular output format determined
    by a derived class.
    """
    def __init__(self, filename):
        """
        Initialize *this to store data at a location, given a file/path name.

        :param filename: A string object, containing the pathname of a file
        where all serialization routines will be performed during a call to
        "self.write()".
        """
        self._filename = filename

    @abc.abstractmethod
    def __enter__(self):
        """
        Open the filename provided by the constructor in preparation to store
        recipe data.
        :return: self
        """
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the output, preventing any more data writes.
        """
        pass

    @abc.abstractmethod
    def write(self, recipeitem):
        """
        Write out the data from a storage_items.RecipeStorage to a file.

        :param recipeitem: storage_items.RecipeStorage
        """
        pass

    def get_storage_name(self):
        return self._filename


# -----------------------------------------------------------------------------
# Class to store recipes in a single text file.
# -----------------------------------------------------------------------------
class TextRecipeStorage(RecipeStorage):
    """
    A TextRecipeStorage object will save storage_item.RecipeStorage objects
    text files.
    """
    def __init__(self, filename):
        """
        Initialize this object to store recipe data in a text file at a
        location, given a file/path name.

        :param filename: A string object, containing the pathname of the text
        file where all serialization routines will be performed during a call
        to "self.write()".
        """
        RecipeStorage.__init__(self, filename)
        self.__outfile = None

    def __enter__(self):
        """
        Open the output file, provided to the constructor, in preparation to
        store recipe data.
        :return: self, if the file was opened successfully, None if not.
        """
        try:
            self.__outfile = codecs.open(self._filename, 'w+', encoding='utf-8')
            return self
        except IOError as e:
            output = "An exception occurred while opening the file %s:\n\t%s"
            sys.stderr.write(output % (e.filename, e.message))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the output, preventing any more data writes.
        """
        if self.__outfile:
            self.__outfile.close()
        return False

    def write(self, recipeitem):
        """
        Write out the data from a storage_items.RecipeStorage to a file.

        :param recipeitem: storage_items.RecipeStorage
        """
        storage = self.__outfile
        storage.write("%s\n\n" % recipeitem['url'])
        storage.write(recipeitem['name'])
        storage.write('\n\n')
        storage.write('Servings: %s' % str(recipeitem['servings']))
        storage.write('\n\n')
        storage.write(recipeitem['description'].strip())
        ingredients = recipeitem['ingredients']
        for ing in ingredients:
            storage.write('\n')
            storage.write('\n\t%d: %s' % (ing['index'], ing['food']))
            if ing['use'] is IngredientUse.SWAPPABLE:
                storage.write(' (SWAPPABLE)')
            elif ing['use'] is IngredientUse.OPTIONAL:
                storage.write(' (OPTIONAL)')
            storage.write('\n\t\t%s' % ing['amount'])


# -----------------------------------------------------------------------------
# Class to store recipe data in a SQL database.
# -----------------------------------------------------------------------------
class SqlRecipeStorage(RecipeStorage):
    """
    A SqlRecipeStorage object will save storage_item.RecipeStorage objects
    the custom food storage database.
    """
    def __init__(self, dbpath):
        """
        Initialize this object to store recipe data in a database file at a
        location, given a file/path name.

        :param dbpath: A string object, containing the pathname of the database
        where all serialization routines will be performed during a call to
        "self.write()".
        """
        dbpath = RecipeDB.DATABASE_PATH  # because you just can't trust people.
        RecipeStorage.__init__(self, dbpath)
        self.__database = None

    def __enter__(self):
        """
        Open the output database, in preparation to store recipe data.
        :return: self, if the file was opened successfully, None if not.
        """
        self.__database = RecipeDB()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the output, preventing any more data writes.
        """
        self.__database.close()

    def get_storage_name(self):
        return RecipeDB.DATABASE_PATH

    def write(self, recipeitem):
        """
        Write out the data from a storage_items.RecipeStorage to a file.

        :param recipeitem: storage_items.RecipeStorage
        """
        self.__database.insert_recipe(recipeitem)
