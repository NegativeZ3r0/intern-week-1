def generate_predictions(models, X_test):
    """Generates predictions using the trained models."""
    model_rf, model_gb = models

    y_pred_rf = model_rf.predict(X_test) #[cite: 1]
    y_pred_gb = model_gb.predict(X_test) #[cite: 1]

    return y_pred_rf, y_pred_gb
