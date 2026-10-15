"""Data loading, cleaning and feature preparation."""

from pathlib import Path
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Food_Name", "Category", "Calories", "Protein", "Carbohydrates",
    "Fat", "Fiber", "Sugar", "Sodium", "Diet_Type", "Meal_Type"
]

NUMERIC_COLUMNS = [
    "Calories", "Protein", "Carbohydrates", "Fat", "Fiber", "Sugar", "Sodium"
]

RECOMMENDER_FEATURES = ["Calories", "Protein", "Carbohydrates", "Fat", "Fiber"]


def load_food_data(path: str | Path) -> pd.DataFrame:
    """Load the approved food dataset from CSV."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Food dataset not found: {path}")
    return pd.read_csv(path)


def clean_food_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the food dataset using the project's required fields."""
    data = df.copy()
    data.columns = [str(c).strip() for c in data.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required dataset columns: {missing}")

    for col in ["Food_Name", "Category", "Diet_Type", "Meal_Type"]:
        data[col] = data[col].astype("string").str.strip()

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.drop_duplicates()
    data = data.dropna(subset=["Food_Name", "Diet_Type", "Meal_Type"])
    data[NUMERIC_COLUMNS] = data[NUMERIC_COLUMNS].fillna(
        data[NUMERIC_COLUMNS].median(numeric_only=True)
    )

    for col in NUMERIC_COLUMNS:
        data[col] = data[col].clip(lower=0)

    data["Diet_Type"] = data["Diet_Type"].str.title()
    data["Meal_Type"] = data["Meal_Type"].str.title()
    data["Category"] = data["Category"].str.title()

    return data.reset_index(drop=True)


def prepare_recommender_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return numeric features used by cosine-similarity recommendation."""
    missing = [c for c in RECOMMENDER_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing recommender features: {missing}")
    return df[RECOMMENDER_FEATURES].astype(float)


def encode_activity_level(level: str) -> int:
    mapping = {
        "Sedentary": 0,
        "Light": 1,
        "Moderate": 2,
        "Active": 3,
        "Very Active": 4,
    }
    if level not in mapping:
        raise ValueError(f"Unknown activity level: {level}")
    return mapping[level]


def encode_goal(goal: str) -> int:
    mapping = {
        "Lose Weight": 0,
        "Maintain Weight": 1,
        "Gain Weight": 2,
    }
    if goal not in mapping:
        raise ValueError(f"Unknown goal: {goal}")
    return mapping[goal]
