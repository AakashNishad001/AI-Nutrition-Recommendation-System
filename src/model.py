"""Machine-learning training, persistence and prediction."""

from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

FEATURES = [
    "age", "height_cm", "weight_kg", "activity_level_encoded",
    "calories", "protein", "carbohydrates", "fat"
]

TARGET = "goal_category"


def train_model(df: pd.DataFrame, model_path: str | Path,
                random_state: int = 42):
    X = df[FEATURES]
    y = df[TARGET]

    if y.nunique() < 2:
        raise ValueError("Training data must contain at least two target classes.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200, random_state=random_state, class_weight="balanced"
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, average="weighted", zero_division=0),
        "recall": recall_score(y_test, predictions, average="weighted", zero_division=0),
        "f1": f1_score(y_test, predictions, average="weighted", zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
    }

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return model, metrics


def load_model(model_path: str | Path):
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. Run notebook 05_model_training.ipynb."
        )
    return joblib.load(model_path)


def predict_goal_category(model, profile: dict) -> str:
    row = pd.DataFrame([{key: profile[key] for key in FEATURES}])
    return str(model.predict(row)[0])
