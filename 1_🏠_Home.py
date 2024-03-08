import streamlit as st
from utils import login


## page configuration settings
def set_page_config():
    st.set_page_config(
        page_title="customer-churn", page_icon=":repeat: :wave:", layout="wide"
    )


def display_contact():
    st.sidebar.write("# Contact Information")
    st.sidebar.write(
        """
    Let's connect. Your feedbacks are welcomed!
    """
    )

    # columns = st.sidebar.columns(6)

    # with columns[1]:
    #     st.write(
    #         """<div style="width:100%;text-align:center;"><a href="https://streamlit.io" style="float:center"><img src="http://www.doigtdecole.com/wp-content/uploads/2020/03/logo-rond-twitter.png" width="22px"></img></a></div>""",
    #         unsafe_allow_html=True,
    #     )

    # with columns[2]:
    #     st.write(
    #         """<div style="width:100%;text-align:center;"><a href="https://streamlit.io" style="float:center"><img src="http://www.doigtdecole.com/wp-content/uploads/2020/03/logo-rond-twitter.png" width="22px"></img></a></div>""",
    #         unsafe_allow_html=True,
    #     )

    # with columns[3]:
    #     st.write(
    #         """<div style="width:100%;text-align:center;"><a href="https://streamlit.io" style="float:center"><img src="http://www.doigtdecole.com/wp-content/uploads/2020/03/logo-rond-twitter.png" width="22px"></img></a></div>""",
    #         unsafe_allow_html=True,
    #     )

    st.sidebar.write(
        """<div style="width:100%;text-align:center;">
        <a href="https://github.com/modelMaestroSolo" style="float:center">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="35px"></img></a>
        <a href="https://twitter.com/modelmaestroSol" style="float:center">
        <img src="https://static.toiimg.com/thumb/msid-102075304,width-400,resizemode-4/102075304.jpg" width="35px"></img></a>
        <a href="https://www.linkedin.com/in/yebsolomon" style="float:center">
        <img src="https://i.pinimg.com/736x/96/8e/a6/968ea62882943e88bbd318ae5fa67429.jpg" width="35px"></img></a>
        <a href="mailto:modelmaestrosolo@gmail.com" style="float:center">
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" width="35px"></img></a>
        </div>""",
        unsafe_allow_html=True,
    )


## put title element in container


def display_home_title():
    with st.container(border=True):
        st.markdown(
            "<h1 style='text-align: center;  font-size: 36px;'>Welcome to The Customer Churn Prediction App! 🔄👋</h1>",
            unsafe_allow_html=True,
        )  # color: yellow; incklude option to change color
        st.markdown(
            "<style>div.block-container{padding-top:1rem;}</style>",
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


def display_home_body():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Key Features")
        st.markdown(
            """     
                    - **A Data Page:** explore the content of proprietory data loaded in real-time form the remote server
                    - **A Dashboard Page:** presents visualizations on both the exploratory data and the KPIs
                    - **A Predict Page:** predict customer churn using a selected model of choice
                    - **A History Page:** contains saved predictions for further analysis later. Users can view the history of their prediction input values
            """
        )

    with col2:
        st.subheader("User Benefits")
        st.markdown(
            """
                    - Make data-driven decisions by leveraging the power of predictive analytics
                    - Free to Select from a list classification models
                    - Simple and straight forward. 
                    """
        )
        st.subheader("Instruction")
        st.markdown(
            """
                    - Use the side bar to navigate the pages of the App
                    - Follow instructions on each page to interact with the App
                    """
        )


def main():
    display_contact()

    display_home_title()

    display_home_body()


if __name__ == "__main__":

    set_page_config()

    login(main=main)
