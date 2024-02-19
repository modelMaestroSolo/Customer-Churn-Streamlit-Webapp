import streamlit as st

## page configuration settings
st.set_page_config(page_title="customer-churn", page_icon="🔁👋", layout="wide")


## put title element in container
with st.container(border=True):
    st.markdown(
        "<h1 style='text-align: center; color: yellow; font-size: 36px;'>Welcome to our Customer Churn Prediction App! 🔄👋</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        """
       Our app utilizes trained machine learning model to analyze customer characteristics 
       and predict which customers are likely to churn. 
       
    """
    )
    st.write(
        """
       Simply input the relevant customer information, and let our model provide insights
       into potential churn risks. _Start exploring now!_
       
       """
    )

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.header("Key Features")
    st.markdown(
        """
                - 
                
        """
    )

    st.header("User Benefits")
    st.markdown(
        """
                - Make data-driven decisions by leveraging the power of predictive analytics
                - Free to Select from a list classification models
                - Simple and straight forward. 
                """
    )

with col2:
    st.header("Instructions ")
    st.header("Contact Info")
    st.header("Feedback")
    st.write("Your feedbacks are welcomed. contact me at modelmaestrosolo@gmail.com")
