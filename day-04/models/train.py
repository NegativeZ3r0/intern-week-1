from sklearn.ensemble import (  #[cite: 1]
    GradientBoostingClassifier,
    RandomForestClassifier,
)


def train_models(X_train, y_train):
    """Trains Random Forest and Gradient Boosting models."""

    # Model 1: Random Forest Classifier
    model_rf = RandomForestClassifier(random_state=42, n_estimators=100) #[cite: 1]
    model_rf.fit(X_train, y_train) #[cite: 1]

    # Model 2: Gradient Boosting Classifier
    model_gb = GradientBoostingClassifier(random_state=42) #[cite: 1]
    model_gb.fit(X_train, y_train) #[cite: 1]

    return model_rf, model_gb
