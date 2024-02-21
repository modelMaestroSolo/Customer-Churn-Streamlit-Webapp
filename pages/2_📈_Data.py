import streamlit as st
import pyodbc
import pandas as pd
import requests
import os


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
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall(), cur.description


rows, description = run_query("SELECT * FROM dbo.LP2_Telco_churn_first_3000;")

columns = [column[0] for column in description] # obtain column names. 

df_database = pd.DataFrame.from_records(rows, columns=columns) #create dataframe from db data


## obtain data from github repo

url_github = "https://github.com/Azubi-Africa/Career_Accelerator_LP2-Classifcation/blob/main/LP2_Telco-churn-second-2000.csv"
response = requests.get(url_github)

# check if download was successful
if response.status_code == 200:
    
    




tab1, tab2, tab3 = st.tabs(["Data Preview", "Data Surface Properties", "Content And Quality Assessment"])

with tab1:
    st.header("Proprietory Data from Vodafone")
    selected_features = st.multiselect(
        "View specific features?",
        options=["All Columns"] + columns,
        default="All Columns",
    )

    (
        st.write(df)
        if "All Columns" in selected_features
        else st.write(df[selected_features])
    )

with tab2:
    st.header("Learn about how the data is organized in the table and format".title())

with tab3:
    st.header("Description of the Features are Provided Below!")
