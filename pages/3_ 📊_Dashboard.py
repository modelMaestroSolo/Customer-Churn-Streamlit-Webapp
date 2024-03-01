import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Tuple

st.set_page_config(
    page_title="Customer-Churn-Dashboard", page_icon=":bar_chart:", layout="wide"
)

st.title(":bar_chart: Churn Insights: Understanding Customer Retention")
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)

if "df" not in st.session_state:
    st.warning("Visit the Data page to automatically load data for the dashbaord!")
    st.stop()
else:
    cleaned_data = st.session_state["df"]

tab1, tab2 = st.tabs(["Exploratory Analysis", "KPI Metrics"])

with tab1:
    # Histograms and Distribution Plots
    st.subheader("Histograms and Distribution Plots")
    fig1 = px.histogram(
        cleaned_data,
        x="tenure",
        nbins=30,
        color="Churn",
        title="Distribution of Tenure by Churn Status",
    )
    st.plotly_chart(fig1)

    fig2 = px.histogram(
        cleaned_data,
        x="MonthlyCharges",
        color="Churn",
        title="Distribution of Monthly Charges by Churn Status",
    )
    st.plotly_chart(fig2)

    fig3 = px.histogram(
        cleaned_data,
        x="TotalCharges",
        color="Churn",
        title="Distribution of Total Charges by Churn Status",
    )
    st.plotly_chart(fig3)

    # Add more bar plots for other categorical variables...

    # Pie Charts
    st.subheader("Pie Charts")
    fig5 = px.pie(
        cleaned_data,
        names="Churn",
        title="Proportion of Churned vs. Non-Churned Customers",
    )
    st.plotly_chart(fig5)

    # Add more pie charts for other categorical variables...

    # Box Plots
    st.subheader("Box Plots")
    fig6 = px.box(
        cleaned_data,
        x="Churn",
        y="MonthlyCharges",
        points="all",
        title="Monthly Charges by Churn Status",
    )
    st.plotly_chart(fig6)

    # Add more box plots for other numerical variables...

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    correlation_matrix = cleaned_data[
        ["tenure", "MonthlyCharges", "TotalCharges"]
    ].corr()
    fig7 = px.imshow(
        correlation_matrix,
        color_continuous_scale="Viridis",
        title="Correlation Heatmap",
    )
    st.plotly_chart(fig7)

    # Pair Plots
    st.subheader("Pair Plots")
    fig8 = px.scatter_matrix(
        cleaned_data,
        dimensions=["tenure", "MonthlyCharges", "TotalCharges"],
        color="Churn",
    )
    st.plotly_chart(fig8)

    # Add more pair plots for other numerical variables...


with tab2:
    st.title("Key Performance Indicators (KPIs)")

    # define function for filters input widgets
    def display_sidebar(data: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:
        st.sidebar.header("Choose Filters")

        internet_services = sorted(data["InternetService"].unique())
        selected_internet_services = st.sidebar.multiselect(
            label="Internet Service", options=internet_services
        )

        contracts = sorted(data["Contract"].unique())
        selected_contracts = st.sidebar.multiselect(
            label="Contract", options=contracts, default=contracts
        )

        payment_methods = sorted(data["PaymentMethod"].unique())
        selected_payment_methods = st.sidebar.multiselect(
            label="Payment Method", options=payment_methods, default=payment_methods
        )
        return selected_internet_services, selected_contracts, selected_payment_methods

    # c1, c2, c3 = st.columns(3)
    # # KPIs
    # st.subheader("Key Performance Indicators (KPIs)")
    # # with c1:
    # #     churn_rate = cleaned_data["Churn"].value_counts(normalize=True)["Yes"] * 100
    # #     st.info(f"Churn Rate\n\n{churn_rate:.2f}%")
    # c1.metric(
    #     "Churn rate",
    #     value=cleaned_data["Churn"].value_counts(normalize=True)["Yes"] * 100,
    # )

    # average_tenure_churned = cleaned_data[cleaned_data["Churn"] == "Yes"][
    #     "tenure"
    # ].mean()
    # average_tenure_non_churned = cleaned_data[cleaned_data["Churn"] == "No"][
    #     "tenure"
    # ].mean()
    # st.write(f"Average Tenure for Churned Customers: {average_tenure_churned:.2f}")
    # st.write(
    #     f"Average Tenure for Non-Churned Customers: {average_tenure_non_churned:.2f}"
    # )

# Add more KPIs...
