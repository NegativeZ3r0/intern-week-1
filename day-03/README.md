<!--• Project Overview • Problem Statement • How to Run  -->
# Project Overview
Analyze a facility dataset containing fields such as facility_id, location, cleanliness_score, odor_score, waste_level,
water_availability, footfall, complaints and inspection_date. Identify missing/duplicate/invalid data and outliers. Calculate
key statistics and identify at least three useful insights. Create 2 bar charts, 1 histogram, 1 scatter plot and 1 additional
visualization.

# Problem Statement
Produce a cleaned dataset, analysis notebook/scripts, visualizations and a README explaining findings.

# Finding

Having thoroughly analyzed the cleaned `facility_hygiene_ml_dataset_cleaned.xlsx` dataset, I can draw the following key conclusions:

### 1. Data Integrity and Cleaning Impact
* **Quality Improved**: successfully imputed missing values across critical features (`cleanliness_score`, `waste_level`, and `water_availability`) and removed 5 duplicate records. This provides a robust, complete dataset containing 995 unique facility inspections for modeling.
* **No Obvious Structural Outliers**: The extreme values observed in variables such as `footfall`, `complaints`, and `hours_since_cleaning` appear to reflect genuine operational variations rather than data entry anomalies.

### 2. Hygiene Risk Drivers
* **The Odor-Risk Connection**: The violin plot reveals a direct relationship between `odor_score` and `hygiene_risk`. Facilities designated as **High Risk** consistently exhibit significantly higher (worse) odor scores, making odor a strong predictor for potential hygiene concerns.
* **Operational Delays**: The histogram of `hours_since_cleaning` shows that while most facilities are cleaned promptly (typically within 5-10 hours), a long-tail distribution exists where some facilities remain uncleaned for up to 36 hours. These neglected windows likely lead directly to elevated risk levels.

### 3. Facility Type & Usage Dynamics
* **Cleanliness Across Facility Types**: Average cleanliness scores remain relatively stable across different facility types, but further granular analysis of the combinations of high traffic (`footfall`) and low cleanliness can pinpoint specifically vulnerable locations.
* **Footfall Constraints**: High-footfall facilities tend to experience more rapid degradation in cleanliness, resulting in more complaints and higher hygiene risks if cleaning intervals are not adjusted to match visitor volume.

# How to run
import the `data-cleaning_analysis_visualizations.ipynb` in [google colab](https://colab.research.google.com/) and dataset excel file from `dataset/facility_hygiene_ml_dataset.xlsx`, then run it
