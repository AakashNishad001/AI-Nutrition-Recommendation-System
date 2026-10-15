"""Content-based food recommendation using cosine similarity."""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

FEATURES = ["Calories", "Protein", "Carbohydrates", "Fat", "Fiber"]


def filter_foods(df: pd.DataFrame, diet_type: str, meal_type: str | None = None,
                 food_preference: str = "") -> pd.DataFrame:
    data = df.copy()
    diet = diet_type.strip().lower()

    if diet:
        allowed = {"vegetarian": ["vegetarian", "vegan"],
                   "vegan": ["vegan"],
                   "non-vegetarian": ["non-vegetarian", "vegetarian", "vegan"]}
        values = allowed.get(diet, [diet])
        data = data[data["Diet_Type"].str.lower().isin(values)]

    if meal_type and meal_type != "All":
        data = data[data["Meal_Type"].str.lower() == meal_type.lower()]

    pref = food_preference.strip().lower()
    if pref:
        mask = (
            data["Food_Name"].str.lower().str.contains(pref, na=False)
            | data["Category"].str.lower().str.contains(pref, na=False)
        )
        # Preference is treated as a ranking signal, not a hard exclusion.
        data["_preference_match"] = mask.astype(int)
    else:
        data["_preference_match"] = 0

    return data.reset_index(drop=True)


def recommend_foods(df: pd.DataFrame, targets: dict, diet_type: str,
                    meal_type: str | None = None, food_preference: str = "",
                    top_n: int = 10) -> pd.DataFrame:
    candidates = filter_foods(df, diet_type, meal_type, food_preference)
    if candidates.empty:
        return candidates

    X = candidates[FEATURES].astype(float)
    target_vector = np.array([[
        targets["calories"], targets["protein"], targets["carbohydrates"],
        targets["fat"], max(1.0, targets["protein"] * 0.20)
    ]])

    scaler = StandardScaler()
    scaled_food = scaler.fit_transform(X)
    scaled_target = scaler.transform(target_vector)

    scores = cosine_similarity(scaled_target, scaled_food)[0]
    candidates["similarity_score"] = scores
    candidates["match_percentage"] = (np.clip(scores, -1, 1) * 50 + 50).round(1)

    # Preference match is a small tie-breaking boost.
    candidates["recommendation_score"] = (
        candidates["similarity_score"] + candidates["_preference_match"] * 0.05
    )
    candidates = candidates.sort_values(
        ["recommendation_score", "similarity_score"],
        ascending=False
    ).head(top_n)

    return candidates.drop(columns=["_preference_match"]).reset_index(drop=True)
