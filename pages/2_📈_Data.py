import streamlit as st
import pyodbc
import pandas as pd


st.title("Customer Churn Data")


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


rows, description = run_query("SELECT TOP 50 * FROM dbo.LP2_Telco_churn_first_3000;")

columns = [column[0] for column in description]

tab1, tab2, tab3 = st.tabs(["Data Preview", "Data Structure", "Learn About Features"])

with tab1:
    st.header("Proprietory Data from Vodafone")
    df = pd.DataFrame.from_records(rows, columns=columns)
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
