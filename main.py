import streamlit as st
import pandas as pd

from prediction_helper import predict_premium


# ==================================================
# Page configuration
# ==================================================

st.set_page_config(
    page_title="Premium Price Predictor",
    page_icon="💰",
    layout="centered"
)


# ==================================================
# Custom CSS
# ==================================================

st.markdown(
    """
    <style>

        .main {
            padding-top: 2rem;
        }

        .title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #777;
            font-size: 18px;
            margin-bottom: 30px;
        }

        .prediction-box {
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            background: transparent;
            border: 1px solid black;
            margin-top: 25px;
        }

        .prediction-label {
            font-size: 18px;
            color: #555;
        }

        .prediction-value {
            font-size: 40px;
            font-weight: 700;
            margin-top: 5px;
        }

        div.stButton > button {
            width: 100%;
            height: 50px;
            font-size: 18px;
            font-weight: 600;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# Header
# ==================================================

st.markdown(
    '<div class="title">💰 Premium Price Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Enter the customer details to predict the insurance premium.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# Input form
# ==================================================

with st.form("prediction_form"):

    # --------------------------------------------------
    # Personal Information
    # --------------------------------------------------

    st.subheader("Personal Information")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )


    col1, col2 = st.columns(2)

    with col1:

        region = st.selectbox(
            "Region",
            [
                "Northeast",
                "Northwest",
                "Southeast",
                "Southwest"
            ]
        )

    with col2:

        marital_status = st.selectbox(
            "Marital Status",
            [
                "Unmarried",
                "Married"
            ]
        )


    col1, col2 = st.columns(2)

    with col1:

        bmi_category = st.selectbox(
            "BMI Category",
            [
                "Overweight",
                "Underweight",
                "Normal",
                "Obesity"
            ]
        )

    with col2:

        smoking_status = st.selectbox(
            "Smoking Status",
            [
                "Regular",
                "No Smoking",
                "Occasional"
            ]
        )


    # --------------------------------------------------
    # Employment & Financial Information
    # --------------------------------------------------

    st.subheader(
        "Employment & Financial Information"
    )

    employment_status = st.selectbox(
        "Employment Status",
        [
            "Self-Employed",
            "Freelancer",
            "Salaried"
        ]
    )


    col1, col2 = st.columns(2)

    with col1:

        income_lakhs = st.number_input(
            "Income (Lakhs)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.1,
            format="%.2f"
        )

    with col2:

        number_of_dependants = st.number_input(
            "Number of Dependants",
            min_value=0,
            max_value=5,
            value=0,
            step=1
        )


    # --------------------------------------------------
    # Medical Information and Genetical Risk Info
    # --------------------------------------------------

    st.subheader("Medical Information and Genetical Risk")

    col1, col2 = st.columns(2)

    with col1:

        medical_history = st.selectbox(
            "Medical History",
            [
                "No Disease",
                "High blood pressure",
                "Diabetes",
                "Thyroid",
                "Heart disease",
                "Diabetes & High blood pressure",
                "Diabetes & Thyroid",
                "Diabetes & Heart disease",
                "High blood pressure & Heart disease"
            ]
        )

    with col2:

        genetical_risk = st.number_input(
            "Genetical Risk",
            min_value=0,
            max_value=5,
            value=0,
            step=1,
            help=(
                "Genetic risk score used by the model. "
                "This feature is especially important for "
                "customers aged 18–25."
            )
        )


    # --------------------------------------------------
    # Insurance Information
    # --------------------------------------------------

    st.subheader("Insurance Information")

    insurance_plan = st.selectbox(
        "Insurance Plan",
        [
            "Silver",
            "Bronze",
            "Gold"
        ]
    )


    # --------------------------------------------------
    # Submit
    # --------------------------------------------------

    submitted = st.form_submit_button(
        "🔮 Predict Premium"
    )


# ==================================================
# Prediction
# ==================================================

if submitted:

    input_data = pd.DataFrame({
        "age": [age],
        "gender": [gender],
        "region": [region],
        "marital_status": [marital_status],
        "bmi_category": [bmi_category],
        "smoking_status": [smoking_status],
        "employment_status": [employment_status],
        "medical_history": [medical_history],
        "insurance_plan": [insurance_plan],
        "income_lakhs": [income_lakhs],
        "number_of_dependants": [number_of_dependants],
        "genetical_risk": [genetical_risk]
    })

    try:

        premium = predict_premium(input_data)

        st.markdown(
            f"""
            <div class="prediction-box">
                <div class="prediction-label">
                    Estimated Insurance Premium
                </div>
                <div class="prediction-value">
                    ₹{premium:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(
            "Unable to make the prediction."
        )

        st.exception(e)