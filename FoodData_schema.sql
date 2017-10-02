
-- The 'foods' table is for holding all single ingredients in a recipe. These
-- are the atoms of our food molecules.
DROP TABLE IF EXISTS Foods;

CREATE TABLE Foods (
  id             INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  id_str         VARCHAR(64) NOT NULL DEFAULT NULL,
  category       INTEGER     NOT NULL DEFAULT NULL,
  date_added     TIMESTAMP   NOT NULL DEFAULT NULL,
  date_modified  TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id)
);



-- High-level info about a recipe. This table lists only basic recipe
-- information. Ingredients, methods, and other information is contained in
-- other tables which reference this one.
DROP TABLE IF EXISTS Recipes;
		
CREATE TABLE Recipes (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  id_str        VARCHAR(64) NOT NULL DEFAULT NULL,
  prep_time     INT         NOT NULL DEFAULT NULL,
  cook_time     INT         NOT NULL DEFAULT NULL,
  num_favorites INT         NOT NULL DEFAULT NULL,
  PRIMARY KEY (id)
);



-- This table provides a way to monitor different measurements and their
-- conversions into a common format (liters).
DROP TABLE IF EXISTS Measurements;
		
CREATE TABLE Measurements (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  id_str        VARCHAR(64) NOT NULL DEFAULT NULL,
  amt_per_liter FLOAT       NOT NULL DEFAULT 0.0,
  PRIMARY KEY (id)
);



-- This table will be able to reference the top-level recipe table to provide
-- information about what's included in a recipe.
DROP TABLE IF EXISTS Recipe_Ingredients;
		
CREATE TABLE Recipe_Ingredients (
  id                INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  recipe_id         INTEGER     NOT NULL DEFAULT NULL,
  food_id           INTEGER     NOT NULL DEFAULT NULL,
  measurement_id    INTEGER     NOT NULL DEFAULT NULL,
  measurement_amt   DECIMAL     NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (recipe_id)       REFERENCES Recipes(id),
  FOREIGN KEY (food_id)         REFERENCES Foods(id),
  FOREIGN KEY (measurement_id)  REFERENCES Measurements(id)
);



-- Categories such as meats, fats, sugars, vegetables, keto, paleo, vegan, etc.
DROP TABLE IF EXISTS Food_Categories;
		
CREATE TABLE Food_Categories (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  id_str        VARCHAR(64) NOT NULL DEFAULT NULL,
  date_added    TIMESTAMP   NOT NULL DEFAULT NULL,
  date_modified TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id)
);



-- High-level info about a user. NO PRIVATE DATA.
DROP TABLE IF EXISTS Users;
		
CREATE TABLE Users (
  id        INTEGER         NOT NULL AUTO_INCREMENT DEFAULT NULL,
  email     VARCHAR(128)    NOT NULL DEFAULT NULL,
  salt      INTEGER         NOT NULL DEFAULT NULL,
  PRIMARY KEY (id)
);



-- URI store for picture paths
DROP TABLE IF EXISTS Recipe_Pictures;
		
CREATE TABLE Recipe_Pictures (
  id            INTEGER         NOT NULL AUTO_INCREMENT DEFAULT NULL,
  id_str        VARCHAR(64)     NOT NULL DEFAULT NULL,
  user_id       INTEGER         NOT NULL DEFAULT NULL,
  recipe_id     INTEGER         NOT NULL DEFAULT NULL,
  picture_uri   VARCHAR(1024)   NOT NULL DEFAULT NULL,
  thumbnail_uri VARCHAR(1024)   NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)         REFERENCES Users(id),
  FOREIGN KEY (recipe_id)       REFERENCES Recipes(id)
);



-- This table monitors information on when recipes were modified and how.
DROP TABLE IF EXISTS Recipe_Modifications;
		
CREATE TABLE Recipe_Modifications (
  id                INTEGER         NOT NULL AUTO_INCREMENT DEFAULT NULL,
  user_id           INTEGER         NOT NULL DEFAULT NULL,
  recipe_id         INTEGER         NOT NULL DEFAULT NULL,
  date_modified     TIMESTAMP       NOT NULL DEFAULT NULL,
  field_modified    VARCHAR(64)     NOT NULL DEFAULT NULL,
  comment           VARCHAR(1024)   NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)     REFERENCES Users (id),
  FOREIGN KEY (recipe_id)   REFERENCES Recipes (id)
);



-- Monitor/audit table for modifications to pictures.
DROP TABLE IF EXISTS Picture_Modifications;
		
CREATE TABLE Picture_Modifications (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  picture_id    INTEGER     NOT NULL DEFAULT NULL,
  date_modified TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (picture_id)  REFERENCES Recipe_Pictures (id)
);



-- Semi-personal information about a user.
DROP TABLE IF EXISTS User_Info;
		
CREATE TABLE User_Info (
  id                INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  user_id           INTEGER     NOT NULL DEFAULT NULL,
  first_name        VARCHAR(64) NOT NULL DEFAULT NULL,
  middle_name       VARCHAR(64) NOT NULL DEFAULT NULL,
  last_name         VARCHAR(64) NOT NULL DEFAULT NULL,
  date_registered   TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)         REFERENCES Users (id)
);



-- Information which can help determine who likes what recipe.
DROP TABLE IF EXISTS Recipe_Favorites;
		
CREATE TABLE Recipe_Favorites (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  user_id       INTEGER     NOT NULL DEFAULT NULL,
  recipe_id     INTEGER     NOT NULL DEFAULT NULL,
  date_added    TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)     REFERENCES Users (id),
  FOREIGN KEY (recipe_id)   REFERENCES Recipes (id)
);



-- Table which allows for users to create their own categories.
DROP TABLE IF EXISTS User_Recipe_Groups;
		
CREATE TABLE User_Recipe_Groups (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  id_str        VARCHAR(64) NOT NULL DEFAULT NULL,
  user_id       INTEGER     NOT NULL DEFAULT NULL,
  date_added    TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)     REFERENCES Users (id)
);



-- Table which maps recipes to user-made groups.
DROP TABLE IF EXISTS User_Recipe_Groups;
		
CREATE TABLE Recipes_To_User_Groups (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  user_id       INTEGER     NOT NULL DEFAULT NULL,
  recipe_id     INTEGER     NOT NULL DEFAULT NULL,
  group_id      INTEGER     NOT NULL DEFAULT NULL,
  date_added    TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)     REFERENCES Users (id),
  FOREIGN KEY (recipe_id)   REFERENCES Recipes (id),
  FOREIGN KEY (group_id)    REFERENCES User_Recipe_Groups (id)
);



-- For tracking any modifications to a user's profile.
DROP TABLE IF EXISTS User_Modifications;
		
CREATE TABLE User_Modifications (
  id                INTEGER         NOT NULL AUTO_INCREMENT DEFAULT NULL,
  user_id           INTEGER         NOT NULL DEFAULT NULL,
  date_modified     TIMESTAMP       NOT NULL DEFAULT NULL,
  field_modified    VARCHAR(64)     NOT NULL DEFAULT NULL,
  comment           VARCHAR(1024)   NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)             REFERENCES Users (id)
);



-- For detailing the actual steps involved in making a recipe.
DROP TABLE IF EXISTS Recipe_Steps;
		
CREATE TABLE Recipe_Steps (
  id        INTEGER         NOT NULL AUTO_INCREMENT DEFAULT NULL,
  recipe_id INTEGER         NOT NULL DEFAULT NULL,
  step_id   INT             NOT NULL DEFAULT NULL,
  comment   VARCHAR(1024)   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (recipe_id)   REFERENCES Recipes (id)
);



-- Private information for individual users only.
DROP TABLE IF EXISTS User_PII;
		
CREATE TABLE User_PII (
  id                    INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  user_id               INTEGER     NOT NULL DEFAULT NULL,
  password_sha256       CHAR(256)   NOT NULL DEFAULT NULL,
  security_question_id  INTEGER     NOT NULL DEFAULT NULL,
  security_response     VARCHAR(64) NOT NULL DEFAULT NULL,
  date_modified         TIMESTAMP   NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)              REFERENCES Users (id),
  FOREIGN KEY (security_question_id) REFERENCES Security_Questions (id)
);



-- Modification info for the user's PII.
DROP TABLE IF EXISTS User_PII_Modifications;
		
CREATE TABLE User_PII_Modifications (
  id                INTEGER         NOT NULL AUTO_INCREMENT DEFAULT NULL,
  pii_id            INTEGER         NOT NULL DEFAULT NULL,
  user_id           INTEGER         NOT NULL DEFAULT NULL,
  date_modified     TIMESTAMP       NOT NULL DEFAULT NULL,
  field_modified    VARCHAR(64)     NOT NULL DEFAULT NULL,
  comment           VARCHAR(1024)   NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (pii_id)              REFERENCES User_PII (id),
  FOREIGN KEY (user_id)             REFERENCES Users (id)
);



-- Questions for people who forgot their passwords.
DROP TABLE IF EXISTS Security_Questions;
		
CREATE TABLE Security_Questions (
  id            INTEGER      NOT NULL AUTO_INCREMENT DEFAULT NULL,
  question      VARCHAR(128) NOT NULL DEFAULT NULL,
  PRIMARY KEY (id)
);



-- Mappings for food catefories to the recipes they represent
DROP TABLE IF EXISTS Categories_To_Recipes;
		
CREATE TABLE Categories_To_Recipes (
  id            INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  category_id   INTEGER     NOT NULL DEFAULT NULL,
  recipe_id     INTEGER     NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id)          REFERENCES Food_Categories (id),
  FOREIGN KEY (recipe_id)   REFERENCES Recipes (id)
);


-- Mapping of ingredients with the categories they can belong to.
DROP TABLE IF EXISTS Categories_To_Ingredients;
		
CREATE TABLE Categories_To_Ingredients (
  id                INTEGER     NOT NULL AUTO_INCREMENT DEFAULT NULL,
  category_id       INTEGER     NOT NULL DEFAULT NULL,
  ingredient_id     INTEGER     NOT NULL DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (category_id)     REFERENCES Food_Categories (id),
  FOREIGN KEY (ingredient_id)   REFERENCES Foods (id)
);

