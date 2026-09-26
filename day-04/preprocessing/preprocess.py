import pandas as pd
from sklearn.model_selection import train_test_split  #[cite: 1]
from sklearn.preprocessing import LabelEncoder, StandardScaler  #[cite: 1]


def load_and_preprocess(file_path):
    """Handles missing values, encoding, scaling, and train/test splits."""
    df = pd.read_excel(file_path) #[cite: 1]

    features = ['cleanliness_score', 'odor_score', 'waste_level', 'complaints', 'footfall', 'hours_since_cleaning'] #[cite: 1]
    target_col = "hygiene_risk" #[cite: 1]

    # Drop rows where target or key features are missing
    data_cleaned = df.dropna(subset=features + [target_col]).copy() #[cite: 1]

    X = data_cleaned[features] #[cite: 1]
    y = data_cleaned[target_col] #[cite: 1]

    # Encode categorical target
    label_encoder = LabelEncoder() #[cite: 1]
    y_encoded = label_encoder.fit_transform(y.astype(str)) #[cite: 1]
    class_names = label_encoder.classes_ #[cite: 1]

    # Standardize features
    scaler = StandardScaler() #[cite: 1]
    X_scaled = scaler.fit_transform(X) #[cite: 1]

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42) #[cite: 1]

    return X_train, X_test, y_train, y_test, class_names, features
