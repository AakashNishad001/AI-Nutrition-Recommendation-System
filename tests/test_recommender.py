import pandas as pd
from src.recommender import filter_foods, recommend_foods

def sample_df():
    return pd.DataFrame([
        ["Oats","Grain",389,16.9,66.3,6.9,10.6,0.9,2,"Vegetarian","Breakfast"],
        ["Chicken Breast","Meat",165,31,0,3.6,0,0,74,"Non-Vegetarian","Lunch"],
        ["Tofu","Soy",76,8,1.9,4.8,0.3,0.6,7,"Vegan","Dinner"],
    ], columns=["Food_Name","Category","Calories","Protein","Carbohydrates",
                "Fat","Fiber","Sugar","Sodium","Diet_Type","Meal_Type"])

def test_vegetarian_filter():
    out = filter_foods(sample_df(), "Vegetarian")
    assert "Chicken Breast" not in out["Food_Name"].tolist()

def test_recommendation_ranking():
    targets = {"calories":2000,"protein":100,"carbohydrates":250,"fat":60}
    out = recommend_foods(sample_df(), targets, "Vegetarian", top_n=2)
    assert len(out) == 2
    assert "similarity_score" in out.columns
