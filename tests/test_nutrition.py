import pytest
from src.nutrition import calculate_nutrition_targets, validate_profile

def test_nutrition_targets():
    result = calculate_nutrition_targets(21, "Male", 170, 65, "Moderate", "Maintain Weight")
    assert result["calories"] > 0
    assert result["protein"] > 0

def test_invalid_age():
    errors = validate_profile(5, 170, 65, "Moderate", "Maintain Weight")
    assert errors

def test_invalid_weight():
    with pytest.raises(ValueError):
        calculate_nutrition_targets(21, "Male", 170, 10, "Moderate", "Maintain Weight")
