CREATE TABLE "Flavor_Types" ("flavor_name" VARCHAR(32) NOT NULL  UNIQUE  DEFAULT '', "flavor_mask" INTEGER NOT NULL  UNIQUE  DEFAULT 0);
CREATE TABLE "basic_foods" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE  DEFAULT 1, "food_group_id" INTEGER NOT NULL  DEFAULT 36, "type" VARCHAR(64) NOT NULL  DEFAULT '', "name" VARCHAR(64) DEFAULT NULL, "detail" VARCHAR(256) DEFAULT NULL);
CREATE TABLE "food_groups" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE  DEFAULT 1, "group" VARCHAR(64) NOT NULL  DEFAULT '');
CREATE TABLE "ingredient_uses" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE  DEFAULT 0, "use_type" VARCHAR(32) NOT NULL  UNIQUE  DEFAULT '');
CREATE TABLE "ingredients" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE  DEFAULT null, "recipe_id" INTEGER NOT NULL  DEFAULT null, "amount" VARCHAR(32) NOT NULL  DEFAULT null, "use" INTEGER NOT NULL  DEFAULT 0, "swap_index" INTEGER NOT NULL  DEFAULT 0, "name" VARCHAR(127) NOT NULL  DEFAULT '');
CREATE TABLE "recipes" ("id" INTEGER PRIMARY KEY  NOT NULL ,"recipe" VARCHAR(255) NOT NULL ,"servings" INTEGER NOT NULL  DEFAULT (1) ,"address" VARCHAR(2048) NOT NULL  DEFAULT ('') , "recipe_sha256" VARCHAR(128) NOT NULL  DEFAULT '');
