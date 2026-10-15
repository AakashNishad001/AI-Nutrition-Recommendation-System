# AI-Based Personalized Nutrition Recommendation System

A third-year college Data Science project using Python, Pandas, NumPy,
Scikit-learn Random Forest, content-based filtering with Cosine Similarity,
Streamlit and optional SQLite feedback storage.

## 1. Setup

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. Dataset

Put the original approved dataset in:
`data/raw/food_nutrition_raw.csv`

Required columns:
Food_Name, Category, Calories, Protein, Carbohydrates, Fat, Fiber,
Sugar, Sodium, Diet_Type, Meal_Type

Run notebook 02 to create:
`data/processed/food_nutrition_clean.csv`

A small demonstration dataset is included at:
`data/sample/sample_food_nutrition.csv`

## 3. Train the ML model

Run:
`notebooks/05_model_training.ipynb`

The notebook creates:
`models/nutrition_model.joblib`

The model predicts a nutrition/goal category. Do not report performance
numbers until they are calculated on the actual project dataset.

## 4. Run the application

```bash
streamlit run app.py
```

## 5. Workflow

User Profile -> Validation -> Nutrition Estimation -> ML Prediction ->
Food Filtering -> Content-Based Recommendation -> Cosine Similarity ->
Meal Recommendation -> Dashboard.

## Important note

Nutrition calculations are approximate educational estimates. They are not
medical prescriptions and should not be used to diagnose, treat or prevent
medical conditions.

The project documents specify that structured dataset values are the source
of actual food nutrition values. An LLM, if added later, should only explain
results and should not invent nutrition values.
