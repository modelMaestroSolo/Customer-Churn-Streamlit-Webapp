import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Tuple


# function to set up page configuration
def set_page_config():
    st.set_page_config(
        page_title="Customer-Churn-Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
    )
    st.header(":bar_chart: Churn Insights: Understanding Customer Retention")
    st.markdown(
        "<style>div.block-container{padding-top:1.5rem;}</style>",
        unsafe_allow_html=True,
    )

    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)


# func to access data from session state


def access_data():
    if "df" not in st.session_state:
        st.info("Visit the Data page to automatically load data for the dashbaord!")
        st.stop()
    else:
        cleaned_data = st.session_state["df"]
    return cleaned_data


# define function for filters input widget. values to be used for filtering data
def display_sidebar(data: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:

    st.sidebar.header("Choose Filters")

    selected_churn = st.sidebar.multiselect(
        label="Churn Status",
        options=["Yes", "No"],
        default=["Yes", "No"],
        format_func=lambda x: "Churners" if x == "Yes" else "Non-churners",
    )

    internet_services = sorted(data["InternetService"].unique())
    selected_internet_services = st.sidebar.multiselect(
        label="Internet Service", options=internet_services, default=internet_services
    )

    contracts = sorted(data["Contract"].unique())
    selected_contracts = st.sidebar.multiselect(
        label="Contract", options=contracts, default=contracts
    )

    payment_methods = sorted(data["PaymentMethod"].unique())
    selected_payment_methods = st.sidebar.multiselect(
        label="Payment Method", options=payment_methods, default=payment_methods
    )

    return (
        selected_churn,
        selected_internet_services,
        selected_contracts,
        selected_payment_methods,
    )


# define function to filter data
def filter_data(data: pd.DataFrame, column: str, values: List[str]):
    return data[data[column].isin(values)] if values else data


### EXPLORATORY DATA ANALYSIS DASHBOARD


# define function for histograms and distribution plots
def display_hist(data: pd.DataFrame):

    st.subheader("Histogram Plots")
    w = 450
    h = 400
    fig1 = px.histogram(
        data,
        x="tenure",
        nbins=35,
        color="Churn",
        title="Distribution of Tenure by Churn Status",
        width=w,
        height=h,
    )
    st.plotly_chart(fig1)

    fig2 = px.histogram(
        data,
        x="MonthlyCharges",
        nbins=30,
        color="Churn",
        title="Distribution of Monthly Charges by Churn Status",
        width=w,
        height=h,
    )
    st.plotly_chart(fig2)

    fig3 = px.histogram(
        data,
        x="TotalCharges",
        nbins=80,
        color="Churn",
        title="Distribution of Total Charges by Churn Status",
        width=w,
        height=h,
    )
    st.plotly_chart(fig3)


def display_boxplot(data: pd.DataFrame):

    st.subheader("Box Plots")
    w = 450
    h = 400
    cols = ["tenure", "MonthlyCharges", "TotalCharges"]

    # Create an empty list to store the box plot figures
    boxplot_figs = []

    # Iterate over each numerical column
    for num_var in cols:
        # Create a box plot figure using Plotly Express
        fig = px.box(
            data,
            x="Churn",
            y=num_var,
            title=f"Boxplot of {num_var}",
            width=w,
            height=h,
        )

        # Append the figure to the list
        boxplot_figs.append(fig)

    # Display the box plot figures using Streamlit
    for fig in boxplot_figs:
        st.plotly_chart(fig)


def display_corr_heatmap(data: pd.DataFrame):
    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    correlation_matrix = data[["tenure", "MonthlyCharges", "TotalCharges"]].corr()
    fig = px.imshow(
        correlation_matrix,
        color_continuous_scale="Viridis",
        width=400,
        height=400,
    )

    # Update the y-axis tick orientation
    fig.update_yaxes(tickangle=75)
    fig.update_xaxes(tickangle=0)
    st.plotly_chart(fig)


# define pair plot function
def display_pairplot(data: pd.DataFrame):
    # Pair Plots
    st.subheader("Pair Plots")
    fig8 = px.scatter_matrix(
        data,
        dimensions=["tenure", "MonthlyCharges", "TotalCharges"],
        color="Churn",
        width=450,
        height=400,
    )
    st.plotly_chart(fig8)


# define function to display pie charts
def display_pie(data: pd.DataFrame):

    # Pie Charts
    st.subheader("Pie Chart")
    fig = px.pie(
        data,
        hole=0.5,
        names="Churn",
        title="Proportion of Churned vs. Non-Churned Customers",
        width=350,
        height=400,
    )
    st.plotly_chart(fig)


def display_barchart_PaymentMethod(data: pd.DataFrame):

    # Pie Charts
    st.subheader("Barplot")
    fig = px.bar(
        data,
        x="PaymentMethod",
        color="Churn",
        title="Barplot of Payment Methods",
        width=350,
        height=450,
    )

    st.plotly_chart(fig)

    # # Add more pie charts for other categorical variables...


def display_barchart_IS_Contract(data: pd.DataFrame):
    w, h = 450, 350
    internet, contract = st.columns(2)
    with internet:
        st.subheader("Barplot")
        fig = px.bar(
            data,
            y="InternetService",
            color="Churn",
            title="Barplot of Internet Service",
            width=w,
            height=h,
        )
        st.plotly_chart(fig)

    with contract:
        st.subheader("Barplot")
        fig = px.bar(
            data,
            y="Contract",
            color="Churn",
            title="Barplot of Contract",
            width=w,
            height=h,
        )
        st.plotly_chart(fig)


def display_summary_stats(data: pd.DataFrame, numerical: bool):

    if numerical:
        st.subheader("Summary statistics of numerical variables")
        st.write(data.describe().round(1))
    else:
        st.subheader("Summary statistics of selected categorical variables")
        summary_stats = data[
            ["Churn", "InternetService", "Contract", "PaymentMethod"]
        ].describe()
        st.write(summary_stats)


### KPI DASHBOARD


# define function to calculate and return kpis values
def calculate_kpis(filtered_data: pd.DataFrame, full_data: pd.DataFrame) -> List[float]:

    # overall kpis
    total_active_customers = f"{(full_data['Churn'] == 'No').sum() / 1000:.2f}K"
    total_churned_customers = (full_data["Churn"] == "Yes").sum()
    overall_churn_rate = (
        f'{full_data["Churn"].value_counts(normalize=True)["Yes"] * 100:.2f}%'
    )
    overall_total_charges = f"{ full_data['TotalCharges'].sum() / 1000000:.2f}M"

    # filtered kpis: numeric
    if (filtered_data["Churn"].isin(["Yes"])).sum() > 1:
        churn_rate = (
            f'{filtered_data["Churn"].value_counts(normalize=True)["Yes"] * 100:.2f}%'
        )
    else:
        churn_rate = f"{0.00}%"
    average_tenure = round(filtered_data["tenure"].mean(), 2)
    average_monthly_charges = round(filtered_data["MonthlyCharges"].mean(), 2)
    average_total_charges = f"{filtered_data['TotalCharges'].mean() / 1000:.2f}K"

    kpis = [
        total_active_customers,
        total_churned_customers,
        overall_churn_rate,
        overall_total_charges,
        churn_rate,
        average_tenure,
        average_monthly_charges,
        average_total_charges,
    ]

    kpi_names = [
        "Total Active Customers",
        "Total Churned Customers",
        "Overall Churn Rate",
        "Overall Total Charges",
        "Churn Rate",
        "Avg Tenure",
        "Avg Monthly Charges",
        "Avg Total Charges",
    ]

    return kpis, kpi_names


# define function to display kpis
def display_kpi(kpis: List[float], kpi_names: List[str]):

    col1 = st.columns(4)
    for i in range(4):
        col1[i].metric(label=kpi_names[i], value=kpis[i])

    st.markdown("By filters:")
    col2 = st.columns(4)
    for i in range(4):
        col2[i].metric(label=kpi_names[i + 4], value=kpis[i + 4])


def display_data_table(data: pd.DataFrame):

    st.subheader("Top 10 Customers by:")
    table1, table2, table3 = st.columns(3)
    with table1:
        st.subheader("Tenure")
        top_custombers_tenure = (
            data[["customerID", "tenure"]]
            .nlargest(10, columns="tenure")
            .round(1)
            .reset_index(drop=True)
        )
        st.write(top_custombers_tenure)

    with table2:
        st.subheader("Monthly Charges")
        top_customers_monthlyCharges = (
            data[["customerID", "MonthlyCharges"]]
            .nlargest(10, columns="MonthlyCharges")
            .round(1)
            .reset_index(drop=True)
        )
        st.write(top_customers_monthlyCharges)

    with table3:
        st.subheader("Total Charges")
        top_customers_totalCharges = (
            data[["customerID", "TotalCharges"]]
            .nlargest(10, columns="TotalCharges")
            .round(1)
            .reset_index(drop=True)
        )
        st.write(top_customers_totalCharges)


def main():
    set_page_config()  # set page configuration

    cleaned_data = access_data()  # access data from session state

    (
        selected_churn,
        selected_internet_services,
        selected_contracts,
        selected_payment_methods,
    ) = display_sidebar(data=cleaned_data)

    filtered_data = cleaned_data.copy()
    filtered_data = filter_data(
        data=filtered_data, column="Churn", values=selected_churn
    )
    filtered_data = filter_data(
        data=filtered_data,
        column="InternetService",
        values=selected_internet_services,
    )
    filtered_data = filter_data(
        data=filtered_data, column="Contract", values=selected_contracts
    )
    filtered_data = filter_data(
        filtered_data, column="PaymentMethod", values=selected_payment_methods
    )

    tab1, tab2 = st.tabs(["Exploratory Analysis", "KPI Metrics"])

    with tab1:
        hist, box = st.columns(2)
        with hist:
            display_hist(data=filtered_data)

        with box:
            display_boxplot(data=filtered_data)

        heatmap, pairplot = st.columns(2)

        with heatmap:
            display_corr_heatmap(data=filtered_data)
        with pairplot:
            display_pairplot(data=filtered_data)

        pie, bar = st.columns(2)

        with pie:
            display_pie(data=filtered_data)

        with bar:
            display_barchart_PaymentMethod(data=filtered_data)

        display_barchart_IS_Contract(data=filtered_data)

        num_stats, cat_stats = st.columns(2)

        with num_stats:
            display_summary_stats(filtered_data, numerical=True)
        with cat_stats:
            display_summary_stats(data=filtered_data, numerical=False)

    with tab2:
        st.subheader("Key Performance Indicators (KPIs)")

        kpis, kpi_names = calculate_kpis(
            filtered_data=filtered_data, full_data=cleaned_data
        )

        display_kpi(kpis=kpis, kpi_names=kpi_names)

        st.divider()

        display_data_table(data=filtered_data)


if __name__ == "__main__":
    main()
