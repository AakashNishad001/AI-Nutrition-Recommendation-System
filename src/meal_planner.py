"""Basic meal-category recommendation."""

import pandas as pd
from .recommender import recommend_foods


MEAL_TYPES = ["Breakfast", "Lunch", "Snack", "Dinner"]


def generate_meal_plan(df: pd.DataFrame, targets: dict, diet_type: str,
                       food_preference: str = "", items_per_meal: int = 3):
    plan = {}
    for meal in MEAL_TYPES:
        plan[meal] = recommend_foods(
            df, targets, diet_type, meal_type=meal,
            food_preference=food_preference, top_n=items_per_meal
        )
    return plan
