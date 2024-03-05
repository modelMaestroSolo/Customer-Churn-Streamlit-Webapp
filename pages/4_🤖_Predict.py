import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
from typing import List, Tuple
import os
from datetime import datetime


# function to set up page configuration
def set_page_config():
    st.set_page_config(
        page_title="Churn Prediction",
        page_icon="🤖",
        layout="wide",
    )


# function to display title in a streamlit container
def display_title_container():
    with st.container(border=True):
        st.markdown("""     ### Customer Churn Prediction """)
        st.write(
            "Select preferred model and provide values of customer features to make a churn prediction!"
        )

    st.markdown(
        "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
    )


def display_sidebar_form() -> dict:
    with st.sidebar.form("options"):
        # Select Model
        st.subheader("Model Selection")
        selected_model = st.radio(
            label="🚀 Choose A Model",
            options=["Random Forest", "XGBoost Classifier"],
            key="selected_model",
        )

        # Customer Information Section
        st.subheader("Customer Information")
        SeniorCitizen = st.radio("Senior Citizen", ["Yes", "No"])
        Partner = st.radio("Partner", ["Yes", "No"])
        Dependents = st.radio("Dependents", ["Yes", "No"])

        # Service Usage Section
        st.subheader("Service Usage")
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=75, step=1)
        InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

        MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No"])
        OnlineSecurity = st.selectbox(
            "Online Security",
            ["No", "Yes", "No internet service"],
        )
        OnlineBackup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"],
        )
        DeviceProtection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"],
        )
        TechSupport = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"],
        )
        StreamingTV = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"],
        )
        StreamingMovies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"],
        )

        # Billing Information Section
        st.subheader("Billing Information")
        MonthlyCharges = st.number_input(
            "Monthly Charges", min_value=0.0, max_value=200.0, step=1.0
        )
        TotalCharges = st.number_input("Total Charges", min_value=0.0, max_value=8700.0)

        PaymentMethod = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
        PaperlessBilling = st.radio("Paperless Billing", ["Yes", "No"])

        # Contract Details Section
        st.subheader("Contract Details")
        Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

        submitted = st.form_submit_button("Predict")

        input_dict = {
            "selected_model": selected_model,
            "SeniorCitizen": SeniorCitizen,
            "Partner": Partner,
            "Dependents": Dependents,
            "tenure": tenure,
            "InternetService": InternetService,
            "MultipleLines": MultipleLines,
            "OnlineSecurity": OnlineSecurity,
            "OnlineBackup": OnlineBackup,
            "DeviceProtection": DeviceProtection,
            "TechSupport": TechSupport,
            "StreamingTV": StreamingTV,
            "StreamingMovies": StreamingMovies,
            "MonthlyCharges": MonthlyCharges,
            "TotalCharges": TotalCharges,
            "PaymentMethod": PaymentMethod,
            "PaperlessBilling": PaperlessBilling,
            "Contract": Contract,
            "submitted": submitted,
        }

        return input_dict


@st.cache_resource(show_spinner="Please wait! Loading Model Components...")
def get_model_components():
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
        st.spinner("Serialized model with components loaded successfully!")
    else:
        # Handle the case when the request fails
        st.error("Failed to download the serialized model.")

    return loaded_components


def display_options_summary(inputs: dict):
    st.markdown("#### Summary of Selected options")
    customer_info, service_usage = st.columns(2)

    with customer_info:
        # Display the selected values
        st.markdown("####  Customer Info")
        st.write("Senior Citizen:", inputs["SeniorCitizen"])
        st.write("Partner:", inputs["Partner"])
        st.write("Dependents:", inputs["Dependents"])

        st.markdown("#### Billing Info")
        st.write("Monthly Charges:", inputs["MonthlyCharges"])
        st.write("Total Charges:", inputs["TotalCharges"])
        st.write("Paperless Billing:", inputs["PaperlessBilling"])
        st.write("Payment Method:", inputs["PaymentMethod"])

        st.write("Contract:", inputs["Contract"])

    with service_usage:
        st.markdown("""#### Service Usage""")
        st.write("Tenure (months):", inputs["tenure"])
        st.write("Internet Service:", inputs["InternetService"])
        st.write("Multiple Lines:", inputs["MultipleLines"])
        st.write("Online Security:", inputs["OnlineSecurity"])
        st.write("Online Backup:", inputs["OnlineBackup"])
        st.write("Device Protection:", inputs["DeviceProtection"])
        st.write("Tech Support:", inputs["TechSupport"])
        st.write("Streaming TV:", inputs["StreamingTV"])
        st.write("streaming Movies:", inputs["StreamingMovies"])


def make_prediction(loaded_components: List[str], inputs: dict) -> Tuple[str]:

    reference_features = loaded_components["reference_features"]
    cat_preprocessor = loaded_components["cat_preprocessor"]
    transformed_columns = loaded_components["transformed_columns"]
    num_cols = loaded_components["numerical_columns"]
    num_transformer = loaded_components["num_transformer"]
    selected_features = loaded_components["selected_features"]

    input_data = np.array(
        [
            inputs["tenure"],
            inputs["MonthlyCharges"],
            inputs["TotalCharges"],
            inputs["SeniorCitizen"],
            inputs["Partner"],
            inputs["Dependents"],
            inputs["MultipleLines"],
            inputs["InternetService"],
            inputs["OnlineSecurity"],
            inputs["OnlineBackup"],
            inputs["DeviceProtection"],
            inputs["TechSupport"],
            inputs["StreamingTV"],
            inputs["StreamingMovies"],
            inputs["Contract"],
            inputs["PaperlessBilling"],
            inputs["PaymentMethod"],
        ]
    ).reshape(1, -1)
    input_df = pd.DataFrame(data=input_data, columns=reference_features)

    # data preprocessing
    input_df_prepared = pd.DataFrame(
        cat_preprocessor.transform(input_df), columns=transformed_columns
    )

    input_df_prepared[num_cols] = num_transformer.transform(input_df_prepared[num_cols])

    input_df_prepared = input_df_prepared[selected_features]

    selected_model = inputs["selected_model"]

    # make prediction using selected model
    if selected_model == "Random Forest":
        classifier = loaded_components["random_forest_classifier"]
        prediction = classifier.predict(input_df_prepared)
        predict_proba = classifier.predict_proba(input_df_prepared)
        predict_proba = pd.DataFrame(
            predict_proba, columns=["No", "Yes"], index=["Prob"]
        ).T
    else:
        classifier = loaded_components["gradient_boosting_classifier"]
        prediction = classifier.predict(input_df_prepared)
        predict_proba = classifier.predict_proba(input_df_prepared)
        predict_proba = pd.DataFrame(
            predict_proba, columns=["No", "Yes"], index=["Probability"]
        ).T

    prediction = prediction[0]
    return input_df, selected_model, prediction, predict_proba


def display_prediction(prediction: str, predict_proba: float):
    with st.container(border=True):

        col1, col2 = st.columns(2)
        if prediction == "No":
            with col1:
                st.markdown("### 🤖 CHURN PREDICTION")
                st.success("""### ✨🎉 Hurray!\n### The Customer will not Churn!""")
            with col2:
                st.write("### 🎲 PREDICTION PROBABILITY")
                st.table(predict_proba)
        else:
            with col1:
                st.markdown("### 🤖 CHURN PREDICTION")
                st.warning("### ⚠️🚨 Warning!\n### The Customer will Churn!")
            with col2:
                st.write("### 🎲 PREDICTION PROBABILITY")
                st.table(predict_proba)


# function to store prediction history in a csv file
def store_history(input_df: pd.DataFrame, selected_model: str, prediction: str):
    now = datetime.now()
    day_of_prediction = now.strftime("%Y-%m-%d %H:%M")

    input_df["day_of_prediction"] = day_of_prediction
    input_df["ModelUsed"] = selected_model
    input_df["Prediction"] = prediction

    input_df.to_csv(
        "./data/history.csv",
        mode="a",  # append history
        header=not os.path.exists("./data/history.csv"),  # create header once
        index=False,
    )


def main():
    set_page_config()

    display_title_container()

    inputs = display_sidebar_form()
    submitted = inputs["submitted"]

    if submitted:
        loaded_components = get_model_components()
        input_df, selected_model, prediction, predict_proba = make_prediction(
            loaded_components, inputs
        )

        display_prediction(prediction=prediction, predict_proba=predict_proba)

        display_options_summary(inputs=inputs)

        store_history(
            input_df=input_df, selected_model=selected_model, prediction=prediction
        )
    else:
        st.info(
            """ 
            ### Hello there👋! 
            
                To make a prediction:
                    1. head over to the sidebar 
                    2. choose preferred ML model and supply values for the customer features.
                    3. Hit Predict when done! 
            """
        )


if __name__ == "__main__":
    main()
