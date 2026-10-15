"""Approximate nutrition requirement calculations.

Important: These are educational estimates for the college project,
not medical or dietary prescriptions.
"""

ACTIVITY_FACTORS = {
    "Sedentary": 1.20,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725,
    "Very Active": 1.90,
}

GOAL_ADJUSTMENTS = {
    "Lose Weight": -300,
    "Maintain Weight": 0,
    "Gain Weight": 300,
}


def validate_profile(age, height_cm, weight_kg, activity_level, goal):
    errors = []
    if age < 13 or age > 100:
        errors.append("Age must be between 13 and 100.")
    if height_cm < 100 or height_cm > 250:
        errors.append("Height must be between 100 and 250 cm.")
    if weight_kg < 25 or weight_kg > 300:
        errors.append("Weight must be between 25 and 300 kg.")
    if activity_level not in ACTIVITY_FACTORS:
        errors.append("Select a valid activity level.")
    if goal not in GOAL_ADJUSTMENTS:
        errors.append("Select a valid nutrition goal.")
    return errors


def calculate_bmr(age, gender, height_cm, weight_kg):
    """Mifflin-St Jeor estimate used as a project assumption."""
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if str(gender).lower() == "male":
        return base + 5
    if str(gender).lower() == "female":
        return base - 161
    return base - 78


def calculate_nutrition_targets(age, gender, height_cm, weight_kg,
                                activity_level, goal):
    errors = validate_profile(age, height_cm, weight_kg, activity_level, goal)
    if errors:
        raise ValueError(" ".join(errors))

    bmr = calculate_bmr(age, gender, height_cm, weight_kg)
    maintenance = bmr * ACTIVITY_FACTORS[activity_level]
    calories = max(1200, maintenance + GOAL_ADJUSTMENTS[goal])

    # Project assumption for a simple educational macronutrient target.
    protein = 1.6 * weight_kg
    fat = (0.25 * calories) / 9
    carbohydrates = max(0, (calories - protein * 4 - fat * 9) / 4)

    return {
        "bmr": round(bmr, 1),
        "maintenance_calories": round(maintenance),
        "calories": round(calories),
        "protein": round(protein, 1),
        "carbohydrates": round(carbohydrates, 1),
        "fat": round(fat, 1),
    }
