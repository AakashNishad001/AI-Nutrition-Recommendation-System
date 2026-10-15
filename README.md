# AI Nutrition Recommendation System

A machine learning and content-based recommendation system that helps users explore food nutrition information and discover similar foods based on food category, diet type, and meal type. The application is built using Python, Pandas, Scikit-learn, and Streamlit.

## 1. Project Overview

The AI Nutrition Recommendation System provides a simple interface for browsing food records, filtering foods, viewing nutritional information, and finding similar food options.

The project uses a dataset containing approximately 8,000 food records with the following attributes:

- Food_Name
- Category
- Calories
- Protein
- Carbohydrates
- Fat
- Fiber
- Sugar
- Sodium
- Diet_Type
- Meal_Type

## 2. Objectives

- Display food and nutritional information in an easy-to-use interface.
- Allow users to search for foods by name.
- Filter foods by diet type, meal type, and maximum calories.
- Recommend similar foods using content-based similarity.
- Demonstrate the practical application of machine learning and data science.
- Provide a foundation for future personalized nutrition features.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Dataset handling and data manipulation |
| NumPy | Numerical computing |
| Scikit-learn | Feature processing, similarity calculations, and machine learning |
| TF-IDF | Text feature representation |
| Cosine Similarity | Finding similar food records |
| Random Forest | Optional diet-type classification model |
| Streamlit | Web application interface |
| Joblib | Saving and loading trained models |
| SQLite | Optional local database integration |
| Pytest | Automated testing |

## 4. Project Structure

```text
AI_Nutrition_Recommendation/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── raw/
│       └── nutrition_food_records_8000.csv
│
├── src/
│   ├── __init__.py
│   ├── recommender.py
│   └── train_model.py
│
├── models/
│   └── diet_type_model.joblib
│
├── database/
├── notebooks/
├── docs/
│
└── tests/
    └── test_recommender.py
```

The trained model file is created when model training completes. The database, notebooks, and documentation folders are reserved for future modules unless additional files are added.

## 5. Features

### Food Search
Search the dataset by food name.

### Food Filtering
Filter food records according to:
- Diet type
- Meal type
- Maximum calories

### Nutrition Information
View calories, protein, carbohydrates, fat, fiber, sugar, and sodium for a selected food.

### Food Recommendations
Use content-based similarity to suggest foods with similar categories, diet types, and meal types.

### Machine Learning
Train an optional Random Forest classifier using the available dataset features to predict the dataset's `Diet_Type` label.

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Visual Studio Code or another code editor (optional)

### Step 1: Open the Project Folder

Open a terminal in the `AI_Nutrition_Recommendation` directory.

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, you can activate the environment using Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Check Dataset Placement

Make sure the CSV file is located at:

```text
data/raw/nutrition_food_records_8000.csv
```

### Step 6: Run the Application

```powershell
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

## 7. Train the Machine Learning Model

To train the optional diet-type classification model, run this command from the project root:

```powershell
python -m src.train_model
```

After successful training, the model will be saved at:

```text
models/diet_type_model.joblib
```

The current Streamlit application uses content-based recommendations and does not automatically load this classifier.

## 8. Run Tests

To run the recommendation unit test:

```powershell
pytest
```

Run tests from the project root directory.

## 9. Dataset

The application uses the supplied CSV dataset. It is expected to contain the 11 columns listed in the Project Overview section.

The dataset is used for food browsing, filtering, nutrition display, and content-based recommendations. The optional classifier uses `Diet_Type` as its target label.

## 10. Limitations

- Recommendation results depend on the categories and labels present in the dataset.
- The current recommendation method identifies similar records; it does not generate a medically personalized diet plan.
- The optional classifier learns from the supplied `Diet_Type` labels and does not establish whether those labels are correct.
- The current application does not calculate individualized daily nutritional requirements.
- Nutrition values depend on the accuracy and serving-size assumptions of the supplied data.

This application is intended for educational and demonstration purposes, not as a substitute for professional dietary advice.

## 11. Future Enhancements

- User profiles and preference-based recommendations.
- Personalized meal planning.
- Daily nutrition tracking.
- SQLite database integration.
- Improved recommendation algorithms.
- Interactive nutrition charts and dashboards.
- Model evaluation and comparison.
- User authentication and saved recommendations.

## 12. Conclusion

The AI Nutrition Recommendation System demonstrates how data science, machine learning, and content-based recommendation techniques can be combined in a practical web application. It provides a foundation for exploring food data and developing more advanced nutrition recommendation features.

---

**Project:** AI Nutrition Recommendation System  
**Application:** Streamlit  
**Language:** Python  
**Purpose:** College Data Science Project
