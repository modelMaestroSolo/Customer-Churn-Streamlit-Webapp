import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# import pyodbc
import pandas as pd
import numpy as np
import requests
from typing import List, Tuple, Union


def login():
    with open("./config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )
    authenticator.login(location="main")
    if st.session_state["authentication_status"]:
        authenticator.logout(location="sidebar", key="logout")
        st.write(f'Welcome *{st.session_state["name"]}*')

    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")

    else:
        st.warning("Please enter your username and password")


## set page configuration, title and description
def set_page_config() -> None:
    st.set_page_config(page_title="Churn Data", page_icon=":chart_with_upwards_trend:")
    st.title(":chart_with_upwards_trend: Customer Churn Data")
    st.markdown(
        "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
    )

    st.write(
        """
        Explore a summary of the customer data used in our churn prediction model. 
        Gain insights into key customer characteristics that influence churn predictions. 
        """
    )

    st.write(
        """
        Use this preview to understand the data behind our predictions and 
        make informed decisions about customer retention strategies.
        
        """
    )


## obtain data from data base
# Initialize connection.
# Uses st.cache_resource to only run once.

#################### extracting data from database #####################################

# @st.cache_resource(show_spinner="Establishing connection to Database...")
# def init_connection() -> pyodbc.Connection:
#     return pyodbc.connect(
#         "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
#         + st.secrets["server"]
#         + ";DATABASE="
#         + st.secrets["database"]
#         + ";UID="
#         + st.secrets["username"]
#         + ";PWD="
#         + st.secrets["password"]
#     )


# # Perform query.
# @st.cache_data(show_spinner="Retrieving Data from Database...")
# def run_query(query: str, _conn: pyodbc.Connection):
#     with _conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall(), cur.description


# # def function to create dataframe with data from database
# def create_dataframe_db(rows: List[Tuple], description) -> Union[pd.DataFrame, List]:
#     columns = [column[0] for column in description]  # obtain column names.
#     df_database = pd.DataFrame.from_records(rows, columns=columns)  # create dataframe

#     return df_database


@st.cache_data(show_spinner="Pulling Data from Github...")
def get_github_data(url):
    """This function gets data from github repo and coverts it to a datafraome

    :param url: github link to the source data
    :type url: link
    """
    # make request
    response = requests.get(url)

    # check if download was successful
    if response.status_code == 200:

        data_github = (
            response.json()
        )  # deserialize JSON string received from the HTTP response
        data_github = data_github["payload"]["blob"][
            "csv"
        ]  # access main data from csv key

        df = pd.DataFrame(data_github[1:], columns=data_github[0])
    else:
        st.error("Failed to download data from Github")

    return df


@st.cache_data(show_spinner="Cleaning Retrieved Data...")
def clean_data(data_db, data_github):

    dtypes = {"tenure": "int32", "MonthlyCharges": "float64", "TotalCharges": "float64"}

    smart_features = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]
    data_db[smart_features] = data_db[smart_features].fillna("No internet service")
    data_db["MultipleLines"] = data_db["MultipleLines"].fillna("No phone service")
    data_db["TotalCharges"] = data_db["TotalCharges"].fillna(
        data_db["TotalCharges"].mean()
    )
    data_db = data_db.dropna(subset=["Churn"])
    data_db = data_db.replace({True: "Yes", False: "No"})

    data_github["SeniorCitizen"] = data_github["SeniorCitizen"].replace(
        {1: "Yes", 0: "No"}
    )

    cleaned_data = pd.concat([data_db, data_github], axis=0).reset_index(drop=True)

    cleaned_data["TotalCharges"] = cleaned_data["TotalCharges"].replace({" ": np.nan})
    cleaned_data = cleaned_data.astype(dtypes)
    cleaned_data["TotalCharges"] = cleaned_data["TotalCharges"].fillna(
        cleaned_data["TotalCharges"].median()
    )
    cleaned_data["Churn"] = cleaned_data["Churn"].astype("category")

    return cleaned_data


def main():
    set_page_config()

    # conn = init_connection()  # establish connection

    # rows, description = run_query(
    #     query="SELECT * FROM dbo.LP2_Telco_churn_first_3000;", _conn=conn
    # )

    # df_database = create_dataframe_db(rows=rows, description=description)
    df_database = pd.read_csv("./data/Telco-churn-first-3000.csv")
    url_github = (
        "https://github.com/Azubi-Africa/Career_Accelerator_LP2-Classifcation/"
        + "blob/main/LP2_Telco-churn-second-2000.csv"
    )

    df_github = get_github_data(url=url_github)

    cleaned_data = clean_data(data_db=df_database, data_github=df_github)
    st.session_state["df"] = (
        cleaned_data  # helps to pass cleaned data to dashbaord page
    )

    tab1, tab2, tab3 = st.tabs(
        ["Data Preview", "Data Surface Properties", "Feature Description"]
    )

    with tab1:
        st.header("Proprietory Data from Vodafone")
        selected_features = st.selectbox(
            "View specific features?",
            options=["All Columns", "Numeric Features", "Categorical Features"],
            index=0,
        )

        numerical_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
        categorical_cols = [
            "SeniorCitizen",
            "Partner",
            "Dependents",
            "InternetService",
            "MultipleLines",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "PaymentMethod",
            "PaperlessBilling",
            "Contract",
        ]

        if selected_features == "Numeric Features":
            st.write(cleaned_data[numerical_cols])
        elif selected_features == "Categorical Features":
            st.write(cleaned_data[categorical_cols])
        else:
            st.write(cleaned_data)

    with tab2:
        st.markdown("**Data Set Name:** Telco Churn Dataset")
        st.markdown(
            "**Abstract:**  The dataset contains comprehensive information about the characteristics and behaviours of customers, including details about whether or not they churn."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Target:** Churn")
        with col2:
            st.markdown("**Data Type:**  Multivariate")
        with col3:
            st.markdown("**Format Type:** Matrix")

        st.markdown(
            """
        | Number of instances | Number of Attributes | Attribute types | Contains missing values?
        | -------- | -------- | -------- | -------| 
        |    5045      |  21        |  <ul><li>Categorical</li><li>Float</li><li>Integer</li><li>Boolean</li></ul>   | Yes |   
                
    """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown("**Features:**")
        with st.container(border=True):

            f1, f2, f3 = st.columns(3)

            with f1:
                st.markdown(
                    """<ul>
                <li>customerID</li>
                <li>gender</li>
                <li>SeniorCitizen</li>
                <li>Partner</li>
                <li>Dependents</li>
                <li>tenure</li>
                <li>PhoneService</li>
                </ul>
                """,
                    unsafe_allow_html=True,
                )

            with f2:
                st.markdown(
                    """<ul>
                <li>MultipleLines</li>
                <li>InternetService</li>
                <li>OnlineSecurity</li>
                <li>OnlineBackup</li>
                <li>DeviceProtection</li>
                <li>TechSupport</li>
                <li>StreamingTV</li>
                </ul>
            """,
                    unsafe_allow_html=True,
                )

            with f3:
                st.markdown(
                    """<ul>
                <li>StreamingMovies</li>
                <li>Contract</li>
                <li>PaperlessBilling</li>
                <li>PaymentMethod</li>
                <li>MonthlyCharges</li>
                <li>TotalCharges</li>
                <li>Churn</li>
                </ul>
            """,
                    unsafe_allow_html=True,
                )
        st.markdown("#### The following describes the columns present in the data:")
        st.markdown(
            """
    **Gender** -- Whether the customer is a male or a female

    **SeniorCitizen** -- Whether a customer is a senior citizen or not

    **Partner** -- Whether the customer has a partner or not (Yes, No)

    **Dependents** -- Whether the customer has dependents or not (Yes, No)

    **Tenure** -- Number of months the customer has stayed with the company

    **Phone Service** -- Whether the customer has a phone service or not (Yes, No)

    **MultipleLines** -- Whether the customer has multiple lines or not

    **InternetService** -- Customer's internet service provider (DSL, Fiber Optic, No)

    **OnlineSecurity** -- Whether the customer has online security or not (Yes, No, No Internet)

    **OnlineBackup** -- Whether the customer has online backup or not (Yes, No, No Internet)

    **DeviceProtection** -- Whether the customer has device protection or not (Yes, No, No internet service)

    **TechSupport** -- Whether the customer has tech support or not (Yes, No, No internet)

    **StreamingTV** -- Whether the customer has streaming TV or not (Yes, No, No internet service)

    **StreamingMovies** -- Whether the customer has streaming movies or not (Yes, No, No Internet service)

    **Contract** -- The contract term of the customer (Month-to-Month, One year, Two year)

    **PaperlessBilling** -- Whether the customer has paperless billing or not (Yes, No)

    **Payment Method** -- The customer's payment method (Electronic check, mailed check, Bank transfer(automatic), Credit card(automatic))

    **MonthlyCharges** -- The amount charged to the customer monthly

    **TotalCharges** -- The total amount charged to the customer

    **Churn** -- Whether the customer churned or not (Yes or No)
    """
        )


if __name__ == "__main__":

    if not st.session_state.get("authentication_status", False):
        login()
    else:
        main()
