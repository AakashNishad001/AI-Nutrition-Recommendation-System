import sys
from pathlib import Path

import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.preprocessing import load_food_data, clean_food_data, encode_activity_level
from src.nutrition import calculate_nutrition_targets
from src.model import load_model, predict_goal_category
from src.recommender import recommend_foods
from src.meal_planner import generate_meal_plan
from src.database import initialize_database, save_feedback
from src.utils import recommendation_reason

DATA_PATH = ROOT / "data" / "processed" / "food_nutrition_clean.csv"
FALLBACK_DATA_PATH = ROOT / "data" / "sample" / "sample_food_nutrition.csv"
MODEL_PATH = ROOT / "models" / "nutrition_model.joblib"
DB_PATH = ROOT / "database" / "app.db"

st.set_page_config(page_title="AI Nutrition Recommendation", page_icon="🥗", layout="wide")


@st.cache_data
def get_food_data():
    path = DATA_PATH if DATA_PATH.exists() else FALLBACK_DATA_PATH
    return clean_food_data(load_food_data(path))


@st.cache_resource
def get_model():
    return load_model(MODEL_PATH)


initialize_database(DB_PATH)

st.title("AI-Based Personalized Nutrition Recommendation System")
st.caption("General nutrition estimates and food recommendations for a college project.")

with st.sidebar:
    st.header("User Profile")
    age = st.number_input("Age", min_value=13, max_value=100, value=21)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=25.0, max_value=300.0, value=65.0)
    activity = st.selectbox("Activity Level",
                            ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    goal = st.selectbox("Nutrition Goal",
                        ["Lose Weight", "Maintain Weight", "Gain Weight"])
    diet = st.selectbox("Dietary Preference",
                        ["Vegetarian", "Non-Vegetarian", "Vegan"])
    food_pref = st.text_input("Food Preference (optional)", placeholder="e.g. oats, rice, Indian")
    meal = st.selectbox("Meal Type", ["All", "Breakfast", "Lunch", "Snack", "Dinner"])
    top_n = st.slider("Number of food recommendations", 3, 15, 8)
    generate = st.button("Generate Recommendations", type="primary", use_container_width=True)

st.info("Nutrition values are estimates for educational use and are not medical prescriptions.")

if generate:
    try:
        targets = calculate_nutrition_targets(
            age, gender, height, weight, activity, goal
        )

        profile = {
            "age": age,
            "height_cm": height,
            "weight_kg": weight,
            "activity_level_encoded": encode_activity_level(activity),
            **{k: targets[k] for k in ["calories", "protein", "carbohydrates", "fat"]},
        }

        try:
            model = get_model()
            prediction = predict_goal_category(model, profile)
        except FileNotFoundError:
            prediction = "Model not trained yet"
            st.warning("The saved ML model is missing. Recommendations still work, but run notebook 05 to enable ML prediction.")

        food_df = get_food_data()
        recs = recommend_foods(
            food_df, targets, diet, None if meal == "All" else meal,
            food_pref, top_n
        )

        st.subheader("Estimated Nutrition Profile")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Calories / day", f"{targets['calories']} kcal")
        c2.metric("Protein", f"{targets['protein']} g")
        c3.metric("Carbohydrates", f"{targets['carbohydrates']} g")
        c4.metric("Fat", f"{targets['fat']} g")

        st.write(f"**Predicted nutrition/goal category:** {prediction}")

        st.subheader("Recommended Foods")
        if recs.empty:
            st.warning("No matching foods were found. Try another dietary preference or meal type.")
        else:
            display_cols = [
                "Food_Name", "Category", "Calories", "Protein", "Carbohydrates",
                "Fat", "Fiber", "Diet_Type", "Meal_Type", "match_percentage"
            ]
            table = recs[display_cols].rename(columns={"match_percentage": "Match %"})
            st.dataframe(table, use_container_width=True, hide_index=True)

            st.subheader("Why these foods?")
            for _, row in recs.head(5).iterrows():
                st.write(
                    f"**{row['Food_Name']}** — {recommendation_reason(row)} "
                    f"(similarity: {row['similarity_score']:.2f})"
                )

        st.subheader("Meal Suggestions")
        plan = generate_meal_plan(food_df, targets, diet, food_pref, items_per_meal=2)
        cols = st.columns(4)
        for col, meal_name in zip(cols, ["Breakfast", "Lunch", "Snack", "Dinner"]):
            with col:
                st.markdown(f"### {meal_name}")
                meal_df = plan[meal_name]
                if meal_df.empty:
                    st.write("No matching item.")
                else:
                    for _, row in meal_df.iterrows():
                        st.write(f"- {row['Food_Name']} ({row['Calories']:.0f} kcal)")

        st.subheader("Nutrition Summary")
        chart_df = pd.DataFrame({
            "Nutrient": ["Protein (g)", "Carbohydrates (g)", "Fat (g)"],
            "Target": [targets["protein"], targets["carbohydrates"], targets["fat"]],
        }).set_index("Nutrient")
        st.bar_chart(chart_df)

        st.subheader("Feedback")
        if not recs.empty:
            selected_food = st.selectbox(
                "Food to rate", recs["Food_Name"].tolist()
            )
            rating = st.slider("Rating", 1, 5, 4)
            comment = st.text_input("Comment (optional)")
            if st.button("Save Feedback"):
                save_feedback(selected_food, rating, comment, DB_PATH)
                st.success("Feedback saved locally.")

    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"Something went wrong: {exc}")
else:
    st.subheader("How the system works")
    st.write(
        "User Profile → Validation → Nutrition Estimation → ML Prediction → "
        "Food Filtering → Cosine Similarity Ranking → Meal Recommendation → Dashboard"
    )
    st.write("Enter your profile in the sidebar and click **Generate Recommendations**.")
