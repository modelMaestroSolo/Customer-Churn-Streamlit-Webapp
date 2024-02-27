import streamlit as st
import pickle
import requests


st.sidebar.radio(
    label="🚀 Choose A Model",
    options=["Random Forest", "XGBoost Classifier"],
    key="selected_model",
)


outer_col1, outer_col2 = st.columns([3, 1])

with outer_col1:

    with st.form("Input values of features".title()):
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            st.header("Customer & Billing Info")
            st.selectbox("Senior Citizen", options=["Yes", "No"], key="SeniorCitizen")
            st.selectbox("Partner", options=["Yes", "No"], key="Partner")
            st.selectbox("Dependents", options=["Yes", "No"], key="Dependents")
            st.selectbox(
                "Paperless Billing", options=["Yes", "No"], key="PaperlessBilling"
            )
            st.selectbox(
                "Payment Method",
                options=[
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
                key="PaymentMethod",
            )
            st.selectbox(
                "Contract",
                options=["Month-to-month" "One year" "Two year"],
                key="Contract",
            )
            st.number_input(
                "Monthly Charges",
                min_value=18.00,
                max_value=120.00,
                key="MonthlyCharges",
            )
            st.number_input(
                "Total Charges", min_value=0.00, max_value=8675.00, key="TotalCharges"
            )

        with inner_col2:
            st.header("Service Usage")
            st.number_input("Tenure", min_value=0, max_value=75)
            st.selectbox("Multiple Lines", options=["Yes", "No"], key="MultipleLines")
            st.selectbox(
                "Internet Service",
                options=["DSL" "Fiber optic" "No"],
                key="InternetService",
            )
            st.selectbox(
                "Online Security",
                options=["No" "Yes" "No internet service"],
                key="OnlineSecurity",
            )
            st.selectbox(
                "Online Backup",
                options=["Yes" "No" "No internet service"],
                key="OnlineBackup",
            )
            st.selectbox(
                "Device Protection",
                options=["Yes" "No" "No internet service"],
                key="DeviceProtection",
            )
            st.selectbox(
                "Tech Support",
                options=["Yes" "No" "No internet service"],
                key="TechSupport",
            )
            st.selectbox(
                "Streaming TV",
                options=["Yes" "No" "No internet service"],
                key="StreamingTV",
            )
            st.selectbox(
                "Streaming Movies",
                options=["Yes" "No" "No internet service"],
                key="StreamingMovies",
            )

        st.form_submit_button("Predict")


@st.cache_resource(show_spinner="loading model")
def get_model_componens():
    xgb_url = "https://github.com/modelMaestroSolo/Customer_churn_classification/raw/main/export/ml.pkl"

    # Download the serialized model
    response = requests.get(xgb_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the serialized model
        serialized_model = response.content

        # Deserialize the model using pickle
        loaded_components = pickle.loads(serialized_model)

        # Print a message to confirm successful loading
        print("Serialized model with components loaded successfully!")
    else:
        # Handle the case when the request fails
        print("Failed to download the serialized model.")

    return (
        loaded_components["numerical_columns"],
        loaded_components["num_transformer"],
        loaded_components["categorical_columns"],
        loaded_components["cat_preprocessor"],
        loaded_components["random_forest_classifier"],
        loaded_components["gradient_boosting_classifier"],
    )


def make_prediction():
    pass


if "__name__" == "__main__":
    pass
