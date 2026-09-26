import pandas as pd


def run_eda(file_path):
    """Loads the dataset and performs initial structural inspection."""
    df = pd.read_excel(file_path) #[cite: 1]

    print("Dataset Shape:", df.shape) #[cite: 1]
    print(df.info()) #[cite: 1]
    print(df.head()) #[cite: 1]

    print(df.describe(include='all')) #[cite: 1]

    print("Missing values per column:") #[cite: 1]
    print(df.isnull().sum()) #[cite: 1]
    print("\nAvailable Columns:", df.columns.tolist()) #[cite: 1]

if __name__ == "__main__":
    run_eda('../dataset/facility_hygiene_ml_dataset_cleaned.xlsx')
