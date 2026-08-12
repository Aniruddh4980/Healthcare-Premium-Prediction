# Healthcare Premium Prediction

This project is a Machine Learning application designed to predict healthcare insurance premiums based on various customer demographics, lifestyle choices, and medical history.

## Project Structure

The project is organized into the following main directories and files:

- **`data/`**: Contains Jupyter notebooks for exploratory data analysis (EDA), data preprocessing, and model training. It also includes the datasets (`.xlsx` files) used for training and testing.
    - Notebooks like `ml_premium_prediction.ipynb`, `model_segmentation.ipynb`, `ML_premium_Prediction_young.ipynb`, and `ML_premium_Prediction_rest.ipynb` detail the data science workflow.
    - Datasets like `premiums.xlsx`, `premiums_young.xlsx`, and `premiums_rest.xlsx`.
- **`data/app/`**: Contains the Streamlit web application code.
    - `main.py`: The main entry point for the Streamlit application. Provides an interactive UI for users to input their data.
    - `prediction_helper.py`: Helper functions for loading the saved models and making predictions based on user input.
- **`data/app/artifacts/`**: Stores the serialized machine learning models and scalers.
    - `model_young.joblib`, `model_rest.joblib`: The trained predictive models, segmented by age groups.
    - `scaler_young.joblib`, `scaler_rest.joblib`: The scalers used to normalize input data before prediction.

## Features

The prediction model takes into account several features, including:
- **Personal Information**: Age, Gender, Region, Marital Status, BMI Category, Smoking Status.
- **Employment & Financial Information**: Employment Status, Income (Lakhs), Number of Dependants.
- **Medical Information**: Medical History (e.g., Diabetes, High blood pressure, Heart disease, Thyroid) and Genetical Risk score.
- **Insurance Information**: Desired Insurance Plan (Silver, Bronze, Gold).

## Model Segmentation

The project employs a segmented modeling approach to improve prediction accuracy:
- A specific model (`model_young.joblib`) is trained and used for younger customers where features like 'Genetical Risk' might play a more significant role.
- A separate model (`model_rest.joblib`) handles predictions for the rest of the age groups.

## How to Run the Application

1. **Prerequisites**: Ensure you have Python installed along with the required libraries such as `streamlit`, `pandas`, `scikit-learn`, and `joblib`. You can install the general requirements using pip (you may want to create a virtual environment first):
   ```bash
   pip install streamlit pandas scikit-learn joblib openpyxl
   ```

2. **Navigate to the app directory**:
   ```bash
   cd data/app
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run main.py
   ```

4. **Access the Web Interface**: Open your browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

## Usage

Once the application is running, fill in the customer details in the form provided on the web interface and click on "**🔮 Predict Premium**" to get the estimated insurance premium amount in INR (₹).
