from evaluation.evaluate import evaluate_and_plot
from models.train import train_models
from predictions.predict import generate_predictions
from preprocessing.eda import run_eda
from preprocessing.preprocess import load_and_preprocess


def main():
    # Define relative path to the dataset
    dataset_path = 'dataset/facility_hygiene_ml_dataset_cleaned.xlsx'

    # 1. Exploratory Data Analysis
    # Reason: Validates dataset integrity and structure before allocating memory for downstream processing.
    print("--- Running EDA ---")
    run_eda(dataset_path)

    # 2. Preprocessing
    # Reason: Transforms raw data into the numerical, standardized tensor formats strictly required by sklearn algorithms.
    print("\n--- Preprocessing Data ---")
    X_train, X_test, y_train, y_test, class_names, features = load_and_preprocess(dataset_path)

    # 3. Model Training
    # Reason: Instantiates and fits the Random Forest and Gradient Boosting classifiers to the training distribution.
    print("\n--- Training Models ---")
    models = train_models(X_train, y_train)

    # 4. Prediction
    # Reason: Isolates the inference step, generating outputs solely from the unseen test set to prevent data leakage.
    print("\n--- Generating Predictions ---")
    predictions = generate_predictions(models, X_test)

    # 5. Evaluation
    # Reason: Quantifies statistical performance (accuracy, F1) and generates visual feature importance metrics.
    print("\n--- Evaluating Models ---")
    evaluate_and_plot(y_test, predictions, class_names, models, features)

if __name__ == "__main__":
    main()
