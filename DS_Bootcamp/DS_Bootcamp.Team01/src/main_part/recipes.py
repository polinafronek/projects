import pandas as pd
import joblib
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecipeAnalyzer:
    def __init__(self, recipes_path, percentages_path, nutrients_path, menus_path, model_path):
        self.recipes_df = pd.read_csv(recipes_path)
        self.percentages_df = pd.read_csv(percentages_path, index_col=0)
        self.nutrients_df = pd.read_csv(nutrients_path)
        self.model = joblib.load(model_path)
        self.all_ingridients = pd.read_csv('../data/epi_r.csv')
        self.combinations =  joblib.load(menus_path)

        self.ingredient_columns = [col for col in self.recipes_df.columns
                                   if col not in ["title", "rating", "URLs"]]

    def forecast_rating(self, ingredients):        
        all_ingridients = self.all_ingridients.drop(columns=['title', 'rating', 'calories', 'protein', 'fat', 'sodium', '#cakeweek', '#wasteless', '22-minute meals', '3-ingredient recipes', '30 days of groceries', 'advance prep required', 'alabama', 'alaska', 'alcoholic', 'leftovers', 'california', 'dominican republic', 'low cholesterol', 'pan-fry', 'fruit', 'stew', 'rating'], axis=1)
        ingredient_list = [ing.strip().lower() for ing in ingredients.split(",")]
    
        input_dict = {feat: 0 for feat in all_ingridients}
        for ing in ingredient_list:
            if ing in input_dict:
                input_dict[ing] = 1

        input_df = pd.DataFrame([input_dict])

        if input_df.sum(axis=1).iloc[0] == 0:
            return "so-so"  

        prediction = self.model.predict(input_df)[0]
        return prediction  


    def get_nutrition_facts(self, ingredients):
        if not hasattr(np, 'float'):
            np.float = float
        facts = {}
        for ingredient in [ing.strip().lower() for ing in ingredients.split(",")]:
            if ingredient in self.percentages_df.columns:
                nutrient_values = self.percentages_df[ingredient].apply(
                    lambda x: float(str(x).replace('%', '').strip()) if pd.notna(x) and str(x).replace('%', '').strip().replace('.', '', 1).isdigit() else 0
                )
                facts[ingredient] = nutrient_values.to_dict()
        return facts

    def find_similar_recipes(self, ingredients, top_n=3):
        input_ings = [ing.strip().lower() for ing in ingredients.split(",")]
        input_vector = pd.Series(0, index=self.ingredient_columns)

        for ing in input_ings:
            if ing in input_vector.index:
                input_vector[ing] = 1

        recipe_matrix = self.recipes_df[self.ingredient_columns].values
        similarities = cosine_similarity([input_vector.values], recipe_matrix)[0]

        top_indices = similarities.argsort()[-top_n:][::-1]

        results = []
        for i in top_indices:
            row = self.recipes_df.iloc[i]
            title = row["title"]
            url = row.get("URLs", "N/A")
            rating = row.get("rating", "N/A")
            results.append((title, rating, url))
        return results

    def day_menu(self):
        breakfast_recipes = self.recipes_df[self.recipes_df['breakfast'] == 1]
        lunch_recipes = self.recipes_df[self.recipes_df['lunch'] == 1]
        dinner_recipes = self.recipes_df[self.recipes_df['dinner'] == 1]
        self.recipes_df = self.recipes_df.drop(columns=['breakfast', 'lunch', 'dinner'])

        menu = np.random.choice(self.combinations)
        print("\nBREAKFAST\n---------------------")
        breakfast = self.recipes_df.iloc[menu['Breakfast_recipe']]
        breakfast_nutrients = self.nutrients_df.iloc[menu['Breakfast_recipe']]
        breakfast_nutrients = breakfast_nutrients[breakfast_nutrients > 0][1:]
        breakfast_ingredients = breakfast[breakfast == 1].index.to_list()
        print(f"{breakfast['title']} (rating: {breakfast['rating']})")
        print("Ingredients:")
        for i in breakfast_ingredients:
            print(f"- {i}")
        print("Nutrients:")
        for nut, val in breakfast_nutrients.items():
            print(f"- {nut}: {val:.2%}")
        print(f"URL: {breakfast['URLs']}")

        print("\nLUNCH\n---------------------")
        lunch = self.recipes_df.iloc[menu['Lunch_recipe']]
        lunch_nutrients = self.nutrients_df.iloc[menu['Lunch_recipe']]
        lunch_nutrients = lunch_nutrients[lunch_nutrients > 0][1:]
        lunch_ingredients = lunch[lunch == 1].index.to_list()
        print(f"{lunch['title']} (rating: {lunch['rating']})")
        print("Ingredients:")
        for i in lunch_ingredients:
            print(f"- {i}")
        print("Nutrients:")
        for nut, val in lunch_nutrients.items():
            print(f"- {nut}: {val:.2%}")
        print(f"URL: {lunch['URLs']}")

        print("\nDINNER\n---------------------")
        dinner = self.recipes_df.iloc[menu['Dinner_recipe']]
        dinner_nutrients = self.nutrients_df.iloc[menu['Dinner_recipe']]
        dinner_nutrients = dinner_nutrients[dinner_nutrients > 0][1:]
        dinner_ingredients = dinner[dinner == 1].index.to_list()
        print(f"{dinner['title']} (rating: {dinner['rating']})")
        print("Ingredients:")
        for i in dinner_ingredients:
            print(f"- {i}")
        print("Nutrients:")
        for nut, val in dinner_nutrients.items():
            print(f"- {nut}: {val:.2%}")
        print(f"URL: {dinner['URLs']}")

        return 0