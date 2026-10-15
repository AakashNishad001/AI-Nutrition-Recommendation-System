import pandas as pd
from src.preprocessing import clean_food_data, encode_activity_level

def test_clean_food_data():
    df = pd.DataFrame({
        "Food_Name":[" Test "], "Category":["grain"], "Calories":["100"],
        "Protein":["5"], "Carbohydrates":["20"], "Fat":["2"], "Fiber":["3"],
        "Sugar":["1"], "Sodium":["10"], "Diet_Type":["vegetarian"], "Meal_Type":["breakfast"]
    })
    out = clean_food_data(df)
    assert out.loc[0, "Food_Name"] == "Test"
    assert out.loc[0, "Diet_Type"] == "Vegetarian"
    assert out.loc[0, "Calories"] == 100

def test_activity_encoding():
    assert encode_activity_level("Moderate") == 2
