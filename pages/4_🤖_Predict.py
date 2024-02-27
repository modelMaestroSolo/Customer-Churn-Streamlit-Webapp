import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests


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


with st.container(border=True):
    st.markdown("""     ### Customer Churn Prediction """)
    st.write(
        "Select preferred model and provide values of customer features to make a churn prediction!"
    )

st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)


@st.cache_resource(show_spinner="loading model")
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
        print("Serialized model with components loaded successfully!")
    else:
        # Handle the case when the request fails
        print("Failed to download the serialized model.")

    return loaded_components


st.markdown("#### Summary of Selected options")
summary, display_prediction = st.columns([3, 1])

with summary:
    customer_info, service_usage = st.columns(2)

    with customer_info:
        # Display the selected values
        st.markdown("####  Customer Info")
        st.write("Senior Citizen:", SeniorCitizen)
        st.write("Partner:", Partner)
        st.write("Dependents:", Dependents)

        st.markdown("#### Billing Info")
        st.write("Monthly Charges:", MonthlyCharges)
        st.write("Total Charges:", TotalCharges)
        st.write("Paperless Billing:", PaperlessBilling)
        st.write("Payment Method:", PaymentMethod)

        st.write("Contract:", Contract)

    with service_usage:
        st.markdown("""#### Service Usage""")
        st.write("Tenure (months):", tenure)
        st.write("Internet Service:", InternetService)
        st.write("Multiple Lines:", MultipleLines)
        st.write("Online Security:", OnlineSecurity)
        st.write("Online Backup:", OnlineBackup)
        st.write("Device Protection:", DeviceProtection)
        st.write("Tech Support:", TechSupport)
        st.write("Streaming TV:", StreamingTV)
        st.write("streaming Movies:", StreamingMovies)


def make_prediction(loaded_components, selected_model, submitted):

    reference_features = loaded_components["reference_features"]
    cat_preprocessor = loaded_components["cat_preprocessor"]
    transformed_columns = loaded_components["transformed_columns"]
    num_cols = loaded_components["numerical_columns"]
    num_transformer = loaded_components["num_transformer"]
    selected_features = loaded_components["selected_features"]

    if submitted:
        # prepare data
        input_data = np.array(
            [
                tenure,
                MonthlyCharges,
                TotalCharges,
                SeniorCitizen,
                Partner,
                Dependents,
                MultipleLines,
                InternetService,
                OnlineSecurity,
                OnlineBackup,
                DeviceProtection,
                TechSupport,
                StreamingTV,
                StreamingMovies,
                Contract,
                PaperlessBilling,
                PaymentMethod,
            ]
        ).reshape(1, -1)
        input_df = pd.DataFrame(data=input_data, columns=reference_features)

        # data preprocessing
        input_df_prepared = pd.DataFrame(
            cat_preprocessor.transform(input_df), columns=transformed_columns
        )

        input_df_prepared[num_cols] = num_transformer.transform(
            input_df_prepared[num_cols]
        )

        input_df_prepared = input_df_prepared[selected_features]

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
                predict_proba, columns=["No", "Yes"], index=["Prob"]
            ).T
    else:
        return None, None

    return prediction, predict_proba


loaded_components = get_model_components()

with display_prediction:
    with st.container(height=450, border=True):
        st.markdown("#### Churn Prediction")
        prediction, predict_proba = make_prediction(
            loaded_components=loaded_components,
            selected_model=selected_model,
            submitted=submitted,
        )
        st.write("Will Customer Churn?")
        if prediction == "No":
            st.success("No")
            st.write("With Prediction Probability:")
            st.table(predict_proba)
        elif prediction == "Yes":
            st.warning("Yes")
            st.write("With Prediction Probability:")
            st.table(predict_proba)
        else:
            st.info("Enter feature values and hit Predict in the sidebar to predict!")
