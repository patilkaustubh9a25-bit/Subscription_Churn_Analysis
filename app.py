
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database.connection import engine
from sqlalchemy import text


st.set_page_config(
    page_title="Subscription Churn Analytics",
    page_icon="📊",
    layout="wide"
)


# DATABASE CONNECTION
st.title("Subscription Churn and Engagement Investigation")

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    st.success("Connected to Neon PostgreSQL")
except Exception:
    st.error("Database connection failed")



# SIDEBAR
st.sidebar.title("📊 CHURN ANALYTICS")
st.sidebar.caption("Subscription Intelligence Platform")

st.sidebar.divider()

st.sidebar.subheader("Navigation")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Overview",
        "Customer Engagement",
        "Support Analysis",
        "Cancellation Analysis",
        "Churn Risk Analysis"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.caption("Data Analytics Project")
st.sidebar.caption("Powered by Python, PostgreSQL & Streamlit")



# OVERVIEW
if page == "Overview":

    st.header("Project Overview")

    st.write(
        "An analytics application for investigating customer "
        "engagement, support activity, subscription cancellations, "
        "and customer churn risk."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Analysis Modules", "4")
    col2.metric("Database", "Neon PostgreSQL")
    col3.metric("Application", "Streamlit")

    st.subheader("Available Analysis")

    st.markdown("""
    - Customer Engagement Analysis
    - Support Ticket Analysis
    - Subscription Cancellation Analysis
    - Customer Churn Risk Analysis
    """)


# CUSTOMER ENGAGEMENT

# CUSTOMER ENGAGEMENT
elif page == "Customer Engagement":

    st.header("Customer Engagement Dashboard")

    monthly_df = pd.read_csv("data/monthly_engagement.csv")
    customer_df = pd.read_csv("data/customer_engagement.csv")

    # INTERACTIVE FILTERS
    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:
        search_customer = st.text_input(
            "Search Customer ID",
            placeholder="Example: C0001"
        )

        engagement_options = sorted(
            customer_df["engagement_level"].dropna().unique()
        )

        selected_engagement = st.multiselect(
            "Engagement Level",
            options=engagement_options,
            default=engagement_options
        )

    with col2:
        period_options = sorted(
            monthly_df["billing_period"].dropna().unique()
        )

        selected_periods = st.multiselect(
            "Billing Period",
            options=period_options,
            default=period_options
        )

    # APPLY CUSTOMER FILTERS
    filtered_df = customer_df[
        customer_df["engagement_level"].isin(selected_engagement)
    ].copy()

    if search_customer:
        filtered_df = filtered_df[
            filtered_df["customer_id"].str.contains(
                search_customer.strip(),
                case=False,
                na=False
            )
        ]

    # APPLY BILLING PERIOD FILTER
    filtered_monthly_df = monthly_df[
        monthly_df["billing_period"].isin(selected_periods)
    ].copy()

    # METRICS
    high = (filtered_df["engagement_level"] == "High").sum()
    low = (filtered_df["engagement_level"] == "Low").sum()
    inactive = (filtered_df["engagement_level"] == "Inactive").sum()

    total_customers = filtered_df["customer_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Filtered Customers", total_customers)
    col2.metric("High Engagement", high)
    col3.metric("Low Engagement", low)
    col4.metric("Inactive", inactive)

    st.divider()

    # ENGAGEMENT DISTRIBUTION
    st.subheader("Customer Engagement Distribution")

    if not filtered_df.empty:

        fig, ax = plt.subplots(figsize=(8, 4))

        engagement_counts = filtered_df["engagement_level"].value_counts()

        ax.bar(engagement_counts.index, engagement_counts.values)

        ax.set_xlabel("Engagement Level")
        ax.set_ylabel("Number of Customers")
        ax.set_title("Customer Engagement Distribution")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No customers found for the selected filters.")

    # MONTHLY USAGE TREND
    st.subheader("Monthly Usage Trend")

    if not filtered_monthly_df.empty:

        fig, ax = plt.subplots(figsize=(12, 4))

        ax.plot(
            filtered_monthly_df["billing_period"],
            filtered_monthly_df["total_usage_events"],
            marker="o"
        )

        ax.set_xlabel("Billing Period")
        ax.set_ylabel("Total Usage Events")
        ax.set_title("Monthly Customer Usage")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No monthly data found for the selected billing periods.")

    # CUSTOMER DETAILS
    st.subheader("Customer Engagement Details")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# SUPPORT ANALYSIS

elif page == "Support Analysis":

    st.header("Support Analysis Dashboard")

    monthly_df = pd.read_csv("data/monthly_support.csv")
    customer_df = pd.read_csv("data/customer_support.csv")

    # INTERACTIVE FILTERS
    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:
        search_customer = st.text_input(
            "Search Customer ID",
            placeholder="Example: C0001"
        )

        ticket_status = st.multiselect(
            "Ticket Status",
            ["Resolved", "Unresolved"],
            default=["Resolved", "Unresolved"]
        )

    with col2:
        period_options = sorted(
            monthly_df["billing_period"].dropna().unique()
        )

        selected_periods = st.multiselect(
            "Billing Period",
            options=period_options,
            default=period_options
        )

    # FILTER MONTHLY DATA
    filtered_monthly_df = monthly_df[
        monthly_df["billing_period"].isin(selected_periods)
    ].copy()

    # FILTER CUSTOMER DATA
    filtered_df = customer_df.copy()

    if search_customer:
        filtered_df = filtered_df[
            filtered_df["customer_id"].str.contains(
                search_customer.strip(),
                case=False,
                na=False
            )
        ]

    if ticket_status == ["Resolved"]:
        filtered_df = filtered_df[
            filtered_df["resolved_tickets"] > 0
        ]

    elif ticket_status == ["Unresolved"]:
        filtered_df = filtered_df[
            (filtered_df["total_tickets"] - filtered_df["resolved_tickets"]) > 0
        ]

    elif not ticket_status:
        filtered_df = filtered_df.iloc[0:0]

    # METRICS
    total_tickets = filtered_df["total_tickets"].sum()
    resolved = filtered_df["resolved_tickets"].sum()
    unresolved = total_tickets - resolved

    resolution_rate = (
        resolved / total_tickets * 100
        if total_tickets > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tickets", int(total_tickets))
    col2.metric("Resolved Tickets", int(resolved))
    col3.metric("Unresolved Tickets", int(unresolved))
    col4.metric("Resolution Rate", f"{resolution_rate:.2f}%")

    st.divider()

    # MONTHLY SUPPORT TREND
    st.subheader("Monthly Support Ticket Trend")

    if not filtered_monthly_df.empty:

        fig, ax = plt.subplots(figsize=(12, 4))

        ax.plot(
            filtered_monthly_df["billing_period"],
            filtered_monthly_df["total_tickets"],
            marker="o"
        )

        ax.set_xlabel("Billing Period")
        ax.set_ylabel("Total Tickets")
        ax.set_title("Monthly Support Ticket Volume")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No monthly data available for the selected periods.")

    # RESOLUTION STATUS
    st.subheader("Resolved vs Unresolved Tickets")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        ["Resolved", "Unresolved"],
        [resolved, unresolved]
    )

    ax.set_ylabel("Number of Tickets")
    ax.set_title("Ticket Resolution Status")

    st.pyplot(fig)
    plt.close(fig)

    # TOP CUSTOMERS
    st.subheader("Top 10 Customers by Support Tickets")

    top_customers = filtered_df.sort_values(
        "total_tickets",
        ascending=False
    ).head(10)

    if not top_customers.empty:

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.barh(
            top_customers["customer_id"],
            top_customers["total_tickets"]
        )

        ax.set_xlabel("Total Support Tickets")
        ax.set_ylabel("Customer ID")
        ax.invert_yaxis()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No customers found for the selected filters.")

    # CUSTOMER DETAILS
    st.subheader("Customer Support Details")

    st.dataframe(
        filtered_df.sort_values(
            "total_tickets",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# CANCELLATION ANALYSIS

elif page == "Cancellation Analysis":

    st.header("Subscription Cancellation Dashboard")

    monthly_df = pd.read_csv("data/monthly_cancellations.csv")
    customer_df = pd.read_csv("data/customer_cancellations.csv")
    distribution_df = pd.read_csv("data/cancellation_distribution.csv")

    # INTERACTIVE FILTERS
    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:
        search_customer = st.text_input(
            "Search Customer ID",
            placeholder="Example: C0001"
        )

        cancellation_status = st.multiselect(
            "Cancellation Status",
            ["With Cancellations", "Without Cancellations"],
            default=["With Cancellations", "Without Cancellations"]
        )

    with col2:
        max_cancellations = int(
            customer_df["total_cancellations"].max()
        )

        selected_counts = st.multiselect(
            "Cancellation Count",
            options=list(range(max_cancellations + 1)),
            default=list(range(max_cancellations + 1))
        )

    # APPLY FILTERS
    filtered_df = customer_df.copy()

    if search_customer:
        filtered_df = filtered_df[
            filtered_df["customer_id"].str.contains(
                search_customer.strip(),
                case=False,
                na=False
            )
        ]

    filtered_df = filtered_df[
        filtered_df["total_cancellations"].isin(selected_counts)
    ]

    if cancellation_status == ["With Cancellations"]:
        filtered_df = filtered_df[
            filtered_df["total_cancellations"] > 0
        ]

    elif cancellation_status == ["Without Cancellations"]:
        filtered_df = filtered_df[
            filtered_df["total_cancellations"] == 0
        ]

    elif not cancellation_status:
        filtered_df = filtered_df.iloc[0:0]

    # METRICS
    total_cancellations = filtered_df["total_cancellations"].sum()

    customers_with_cancellations = (
        filtered_df["total_cancellations"] > 0
    ).sum()

    customers_without_cancellations = (
        filtered_df["total_cancellations"] == 0
    ).sum()

    total_customers = filtered_df["customer_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Filtered Customers", total_customers)
    col2.metric("Total Cancellations", int(total_cancellations))
    col3.metric("Customers with Cancellations", int(customers_with_cancellations))
    col4.metric("Customers without Cancellations", int(customers_without_cancellations))

    st.divider()

    # MONTHLY CANCELLATION TRENDS
    st.subheader("Monthly Cancellation Trends")

    if search_customer:
        st.info(
            "Monthly trends show overall cancellation activity, "
            "not individual customer activity."
        )

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        monthly_df["billing_period"],
        monthly_df["total_cancellations"],
        marker="o"
    )

    ax.set_xlabel("Billing Period")
    ax.set_ylabel("Total Cancellations")
    ax.set_title("Monthly Cancellation Trends")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    # CUSTOMER CANCELLATION DISTRIBUTION
    st.subheader("Customer Cancellation Distribution")

    if not filtered_df.empty:

        filtered_distribution = (
            filtered_df["total_cancellations"]
            .value_counts()
            .sort_index()
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            filtered_distribution.index.astype(str),
            filtered_distribution.values
        )

        ax.set_xlabel("Number of Cancellations")
        ax.set_ylabel("Number of Customers")
        ax.set_title("Cancellation Distribution")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No customers found for the selected filters.")

    # WITH VS WITHOUT CANCELLATIONS
    st.subheader("Customers With vs Without Cancellations")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        ["With Cancellations", "Without Cancellations"],
        [
            customers_with_cancellations,
            customers_without_cancellations
        ]
    )

    ax.set_ylabel("Number of Customers")

    st.pyplot(fig)
    plt.close(fig)

    # CUSTOMER DETAILS
    st.subheader("Customer Cancellation Details")

    st.dataframe(
        filtered_df.sort_values(
            "total_cancellations",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# CHURN RISK ANALYSIS

elif page == "Churn Risk Analysis":

    st.header("Customer Churn Risk Dashboard")

    customer_df = pd.read_csv("data/customer_churn_risk.csv")

    # INTERACTIVE FILTERS
    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:
        search_customer = st.text_input(
            "Search Customer ID",
            placeholder="Example: C0001"
        )

        risk_options = ["High Risk", "Medium Risk", "Low Risk"]

        selected_risks = st.multiselect(
            "Risk Level",
            options=risk_options,
            default=risk_options
        )

    with col2:
        min_score = int(customer_df["risk_score"].min())
        max_score = int(customer_df["risk_score"].max())

        selected_score = st.slider(
            "Risk Score Range",
            min_value=min_score,
            max_value=max_score,
            value=(min_score, max_score)
        )

    # APPLY FILTERS
    filtered_df = customer_df[
        customer_df["risk_level"].isin(selected_risks)
    ].copy()

    filtered_df = filtered_df[
        filtered_df["risk_score"].between(
            selected_score[0],
            selected_score[1]
        )
    ]

    if search_customer:
        filtered_df = filtered_df[
            filtered_df["customer_id"].str.contains(
                search_customer.strip(),
                case=False,
                na=False
            )
        ]

    # METRICS
    high_risk = (filtered_df["risk_level"] == "High Risk").sum()
    medium_risk = (filtered_df["risk_level"] == "Medium Risk").sum()
    low_risk = (filtered_df["risk_level"] == "Low Risk").sum()

    total_customers = filtered_df["customer_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Filtered Customers", total_customers)
    col2.metric("High Risk", high_risk)
    col3.metric("Medium Risk", medium_risk)
    col4.metric("Low Risk", low_risk)

    st.divider()

    # RISK DISTRIBUTION
    st.subheader("Customer Churn Risk Distribution")

    if not filtered_df.empty:

        risk_counts = (
            filtered_df["risk_level"]
            .value_counts()
            .reindex(risk_options, fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            risk_counts.index,
            risk_counts.values
        )

        ax.set_xlabel("Risk Level")
        ax.set_ylabel("Number of Customers")
        ax.set_title("Customer Churn Risk Distribution")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No customers found for the selected filters.")

    # RISK SCORE DISTRIBUTION
    st.subheader("Risk Score Distribution")

    if not filtered_df.empty:

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.hist(
            filtered_df["risk_score"],
            bins=range(
                int(customer_df["risk_score"].min()),
                int(customer_df["risk_score"].max()) + 2
            ),
            edgecolor="black"
        )

        ax.set_xlabel("Risk Score")
        ax.set_ylabel("Number of Customers")
        ax.set_title("Customer Risk Score Distribution")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No risk scores available for the selected filters.")

    # HIGH-RISK CUSTOMERS
    st.subheader("High-Risk Customers")

    high_risk_customers = filtered_df[
        filtered_df["risk_level"] == "High Risk"
    ].sort_values(
        "risk_score",
        ascending=False
    )

    st.dataframe(
        high_risk_customers,
        use_container_width=True,
        hide_index=True
    )

    # ALL CUSTOMER DETAILS
    st.subheader("All Customer Risk Details")

    st.dataframe(
        filtered_df.sort_values(
            "risk_score",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Risk categories are exploratory, rule-based classifications. "
        "They are not machine-learning predictions."
    )




