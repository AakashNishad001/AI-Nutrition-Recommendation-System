import pandas as pd
from src.model import FEATURES

def test_model_features():
    expected = {
        "age", "height_cm", "weight_kg", "activity_level_encoded",
        "calories", "protein", "carbohydrates", "fat"
    }
    assert set(FEATURES) == expected
