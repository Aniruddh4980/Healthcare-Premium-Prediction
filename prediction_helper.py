import joblib
import pandas as pd


# ==================================================
# Load artifacts
# ==================================================

model_young = joblib.load("artifacts/model_young.joblib")
model_rest = joblib.load("artifacts/model_rest.joblib")

scaler_young_data = joblib.load("artifacts/scaler_young.joblib")
scaler_rest_data = joblib.load("artifacts/scaler_rest.joblib")

scaler_young = scaler_young_data["scaler"]
scaler_rest = scaler_rest_data["scaler"]

cols_to_scale_young = scaler_young_data["cols_to_scale"]
cols_to_scale_rest = scaler_rest_data["cols_to_scale"]


# ==================================================
# Exact model feature order
# ==================================================

MODEL_FEATURES = [
    "age",
    "number_of_dependants",
    "income_lakhs",
    "insurance_plan",
    "genetical_risk",
    "normalized_risk_score",
    "gender_Male",
    "region_Northwest",
    "region_Southeast",
    "region_Southwest",
    "marital_status_Unmarried",
    "bmi_category_Obesity",
    "bmi_category_Overweight",
    "bmi_category_Underweight",
    "smoking_status_Occasional",
    "smoking_status_Regular",
    "employment_status_Salaried",
    "employment_status_Self-Employed"
]


# ==================================================
# Numeric mappings
# ==================================================

INSURANCE_PLAN_MAP = {
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3
}


# ==================================================
# Medical history mapping
# ==================================================

MEDICAL_RISK_MAP = {
    "No Disease": 0,
    "High blood pressure": 6,
    "Diabetes": 6,
    "Thyroid": 5,
    "Heart disease": 8,
    "Diabetes & High blood pressure": 12,
    "Diabetes & Thyroid": 11,
    "Diabetes & Heart disease": 14,
    "High blood pressure & Heart disease": 14
}


def calculate_normalized_risk_score(medical_history):

    risk = MEDICAL_RISK_MAP.get(
        medical_history,
        0
    )

    return risk / 14


# ==================================================
# Preprocessing
# ==================================================

def preprocess_input(input_data):

    df = input_data.copy()

    # --------------------------------------------------
    # Convert categorical numerical features
    # --------------------------------------------------

    df["income_level"] = 0

    df["insurance_plan"] = df["insurance_plan"].map(
        INSURANCE_PLAN_MAP
    )

    # --------------------------------------------------
    # Create normalized risk score
    # --------------------------------------------------

    df["normalized_risk_score"] = df[
        "medical_history"
    ].apply(
        calculate_normalized_risk_score
    )

    # --------------------------------------------------
    # One-hot encoding
    # --------------------------------------------------

    df = pd.get_dummies(
        df,
        columns=[
            "gender",
            "region",
            "marital_status",
            "bmi_category",
            "smoking_status",
            "employment_status"
        ],
        drop_first=False
    )

    # --------------------------------------------------
    # Scale
    #
    # income_level is included here because it exists
    # in the saved scaler.
    # --------------------------------------------------

    age = df["age"].iloc[0]

    if age <= 25:
        scaler = scaler_young
        cols_to_scale = cols_to_scale_young
    else:
        scaler = scaler_rest
        cols_to_scale = cols_to_scale_rest

    df[cols_to_scale] = scaler.transform(
        df[cols_to_scale]
    )

    # --------------------------------------------------
    # Remove non-model columns
    # --------------------------------------------------

    df = df.drop(
        columns=[
            "income_level",
            "medical_history"
        ],
        errors="ignore"
    )

    # --------------------------------------------------
    # Ensure exact feature set and order
    # --------------------------------------------------

    df = df.reindex(
        columns=MODEL_FEATURES,
        fill_value=0
    )

    return df


# ==================================================
# Prediction
# ==================================================

def predict_premium(input_data):

    age = input_data["age"].iloc[0]

    processed_data = preprocess_input(
        input_data
    )

    # --------------------------------------------------
    # Select correct model
    # --------------------------------------------------

    if age <= 25:
        model = model_young
    else:
        model = model_rest

    # --------------------------------------------------
    # Predict
    # --------------------------------------------------

    prediction = model.predict(
        processed_data
    )

    return float(prediction[0])