import streamlit as st
import pyodbc
import pandas as pd
import requests


## set page configuration, title and description

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
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )


conn = init_connection()


# Perform query.


@st.cache_data
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall(), cur.description


rows, description = run_query("SELECT * FROM dbo.LP2_Telco_churn_first_3000;")


columns = [column[0] for column in description]  # obtain column names.

df_database = pd.DataFrame.from_records(
    rows, columns=columns
)  # create dataframe from db data


url_github = "https://github.com/Azubi-Africa/Career_Accelerator_LP2-Classifcation/blob/main/LP2_Telco-churn-second-2000.csv"


@st.cache_data
def get_github_data(url):
    """This function gets data from github repo and coverts it to a datafraome

    :param url: github link to the source data
    :type url: link
    """
    # make request
    response = requests.get(url_github)

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


df_github = get_github_data(url=url_github)


# url_onedrive = ( "https://azubiafrica-my.sharepoint.com/personal/teachops_azubiafrica_org" +
#                "/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fteachops%5Fazubiafrica%5Forg%" +
#                "2FDocuments%2FCareer%20Accelerator%20Data%5FSets%2FLP2%20Datasets&ga=1" )

# #  make request
# response = requests.get(url_onedrive)

# # check if download was successful

# if response.status_code == 200:  # status code was 403 forbidden
#     pass


# df_onedrive = pd.read_excel("../data/Telco-churn-last-2000.xlsx")
# streamlit will run into error because the home page has a different relative path to the data folder


# concat all dataset
data_train = pd.concat([df_database, df_github])

st.session_state["df"] = data_train

# # save full data frame
# with open("\data\df_train.pkl", "wb") as f:
#      pickle.dump(data_train, f)

tab1, tab2, tab3 = st.tabs(
    ["Data Preview", "Data Surface Properties", "Content And Quality Assessment"]
)

with tab1:
    st.header("Proprietory Data from Vodafone")
    selected_features = st.multiselect(
        "View specific features?",
        options=["All Columns"] + columns,
        default="All Columns",
    )

    (
        st.write(data_train)
        if "All Columns" in selected_features
        else st.write(data_train[selected_features])
    )
    st.write(f"Number of row: {data_train.shape[0]}")
    st.write(f"Number of columns: {data_train.shape[1]}")

with tab2:
    st.header("Data Surface Properties".title())
    st.markdown(
        """
                
    **Data Set Name:** Telco Churn Dataset.

    **Abstract:**  The dataset contains comprehensive information about the characteristics and behaviours of customers, including details about whether or not they churn.

    **Features:** 
    <ul>
  <li>customerID</li>
  <li>gender</li>
  <li>SeniorCitizen</li>
  <li>Partner</li>
  <li>Dependents</li>
  <li>tenure</li>
  <li>PhoneService</li>
  <li>MultipleLines</li>
  <li>InternetService</li>
  <li>OnlineSecurity</li>
  <li>OnlineBackup</li>
  <li>DeviceProtection</li>
  <li>TechSupport</li>
  <li>StreamingTV</li>
  <li>StreamingMovies</li>
  <li>Contract</li>
  <li>PaperlessBilling</li>
  <li>PaymentMethod</li>
  <li>MonthlyCharges</li>
  <li>TotalCharges</li>
  <li>Churn</li>
</ul>

    

    **Target: ** Churn 

    **Data Type:**  Multivariate

    **Format Type:** Matrix

    | Number of instances | Number of Attributes | Attribute types | Contains missing values?
    | -------- | -------- | -------- | -------| 
    |    5045      |  21        |  <ul><li>Categorical</li><li>Float</li><li>Integer</li><li>Boolean</li></ul>   | Yes |   
            
"""
    )

with tab3:
    st.header("Description of the Features are Provided Below!")
