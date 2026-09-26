import matplotlib.pyplot as plt  #[cite: 1]
import numpy as np  #[cite: 1]
import seaborn as sns  #[cite: 1]
from sklearn.metrics import accuracy_score, classification_report  #[cite: 1]


def evaluate_and_plot(y_test, predictions, class_names, models, features):
    """Calculates accuracy, prints reports, and plots feature importance."""
    y_pred_rf, y_pred_gb = predictions
    model_rf, _ = models

    # Accuracy evaluation
    print(f"Random Forest Classifier Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}") #[cite: 1]
    print(f"Gradient Boosting Classifier Accuracy: {accuracy_score(y_test, y_pred_gb):.4f}\n") #[cite: 1]

    # Classification reports
    print("--- Random Forest Classification Report ---") #[cite: 1]
    print(classification_report(y_test, y_pred_rf, target_names=class_names)) #[cite: 1]
    print("--- Gradient Boosting Classification Report ---") #[cite: 1]
    print(classification_report(y_test, y_pred_gb, target_names=class_names)) #[cite: 1]

    # Feature Importance Plot
    importances = model_rf.feature_importances_ #[cite: 1]
    indices = np.argsort(importances)[::-1] #[cite: 1]

    plt.figure(figsize=(10, 6)) #[cite: 1]
    plt.title("Feature Importances (Random Forest Model)") #[cite: 1]
    sns.barplot(x=importances[indices], y=[features[i] for i in indices], hue=[features[i] for i in indices], palette="viridis", legend=False) #[cite: 1]
    plt.xlabel("Relative Importance") #[cite: 1]
    plt.tight_layout() #[cite: 1]
    # plt.show() #[cite: 1] to avoid UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
