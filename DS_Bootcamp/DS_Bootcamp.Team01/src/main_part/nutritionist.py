from recipes import RecipeAnalyzer
import pandas as pd
import numpy as np

def main():
    import sys
    if len(sys.argv) >= 2:
        ingredients = sys.argv[1:]
        ingredients = ", ".join(ingredients)
    else:
        print('The number of ingredients is not enough')
        sys.exit(1)
    
    analyzer = RecipeAnalyzer(
        recipes_path="../data/recipes.csv",
        percentages_path="../data/percentages.csv",
        nutrients_path="../data/nutrients_per_meal.csv",
        menus_path="../data/valid_combinations.joblib",
        model_path="../data/best_model.joblib"
    )
    
    forecast = analyzer.forecast_rating(ingredients)
    print("I. OUR FORECAST")
    if forecast == "bad":
        print("You might find it tasty, but in our opinion, it is a bad idea to have a dish with that list of ingredients.")
    elif forecast == "so-so":
        print("You might find it decent, but it could be better with different ingredients.")
    elif forecast == "great":
        print("Great choice! This combination should be tasty and healthy.")

    print("\nII. NUTRITION FACTS")
    nutrition_facts = analyzer.get_nutrition_facts(ingredients)
    if not nutrition_facts:
        print("No nutrition facts available for the given ingredients.")
    for ingredient, facts in nutrition_facts.items():
        print(f"\n{ingredient}")
        for nutrient, value in facts.items():
            if pd.notna(value) and value > 0:
                print(f"{nutrient} - {value:.1f}% of Daily Value")

    print("\nIII. TOP-3 SIMILAR RECIPES:")
    similar_recipes = analyzer.find_similar_recipes(ingredients)
    if not similar_recipes:
        print("No similar recipes found.")
    for title, rating, url in similar_recipes:
        print(f"- {title}, rating: {rating}, URL: {url}")

    print('\n\nMENU FOR A DAY')
    analyzer.day_menu()

if __name__ == "__main__":
    main()
