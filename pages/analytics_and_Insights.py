# analysis_insights_page.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Analysis & Insights", layout="wide")
st.title("📊 Analytics & Insights")
st.markdown("Use the sidebar to pick a question. Charts are interactive — hover to inspect values.")

# -----------------------
# Load data (hard-coded path)
# -----------------------
DATA_PATH = Path('Data /Loan_Default_Detection_Prediction.csv')

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(f"🚨 Error loading dataset from {DATA_PATH}: {e}")
    st.stop()

# ensure Total_Income exists
if "Total_Income" not in df.columns:
    df["Total_Income"] = df.get("ApplicantIncome", 0).fillna(0) + df.get("CoapplicantIncome", 0).fillna(0)

# -----------------------
# Sidebar: question selector + final recommendations trigger
# -----------------------
st.sidebar.header("🔎 Analysis Controls")

question = st.sidebar.radio(
    "Choose an analysis question (click to view):",
    (
        "1️⃣ Does gender influence loan approval rates?",
        "2️⃣ Is there a relationship between number of dependents and loan approval?",
        "3️⃣ Does property area affect loan approval?",
        "4️⃣ Are shorter or longer loans more likely to be approved?",
        "5️⃣ How does credit history impact loan approval?",
        "6️⃣ Does total household income affect loan approval?",
        "7️⃣ What is impact of marital status and dependents on loan approval?"
    )
)

# Sidebar control to show final recommendations on the main page
show_reco = st.sidebar.checkbox("Show Final Recommendations on page")

# -----------------------
# Show the selected question prominently on the page
# -----------------------
st.markdown("---")
st.header(f"🔸 Selected Question")
st.subheader(question)
st.markdown("Below you will find the interactive visualization and the summary insight for this question.")
st.markdown("---")

# -----------------------
# Question logic & plots
# -----------------------
if question.startswith("1️⃣"):
    # 1. Gender influence
    fig = px.histogram(df, x="Gender", color="Loan_Status", barmode="group",
                       title="Loan Approval Rate by Gender", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- **Male applicants** have a much higher number of approvals (339) compared to rejections (150).  
- **Female applicants** also have more approvals (75) than rejections (37), but their total applications are far fewer than males.
"""
    )

elif question.startswith("2️⃣"):
    # 2. Dependents
    fig = px.histogram(df, x='Dependents', color='Loan_Status', barmode='group',
                       title='Loan Status by Dependents')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- **Applicants with 0 dependents** have the highest approval counts, likely due to lower financial burdens.
"""
    )

elif question.startswith("3️⃣"):
    # 3. Property area
    fig = px.histogram(df, x='Property_Area', color='Loan_Status', barmode='group',
                       title='Loan Status by Property Area')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- **Semiurban areas** have the highest approval count, followed by rural and urban.
"""
    )

elif question.startswith("4️⃣"):
    st.subheader("4️⃣ Are shorter or longer loans more likely to be approved?")

    fig = px.histogram(
        df,
        x='Loan_Amount_Term',
        color='Loan_Status',
        barmode='group',
        title='Loan Approval by Loan Term Duration'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- **Longer loans are more likely to be approved.**
        """
    )


elif question.startswith("5️⃣"):
    # 5. Credit history
    fig = px.histogram(df, x="Credit_History", color="Loan_Status", barmode="group",
                       title="Loan Approval Rate by Credit History", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- Applicants with a **good credit history (1)** have a very high approval count (378) compared to rejections (97).  
- Applicants with **no/poor credit history (0)** face a significant disadvantage — only 7 approvals vs 82 rejections.  
- **Credit history is a critical factor** in loan approval.
"""
    )

elif question.startswith("6️⃣"):
    # 6. Total household income
    fig = px.box(df, x="Loan_Status", y="Total_Income", color="Loan_Status",
                 title="Total Household Income vs Loan Status")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- The **median total household income** is quite similar for both approved and rejected loans, suggesting income alone isn’t a strong approval driver.  
- There are more high-income outliers among rejected applications, meaning some high earners still face denials — likely due to other factors like credit history or loan-to-income ratio.
"""
    )

elif question.startswith("7️⃣"):
    # 7. Marital status & dependents
    married_dependents = df.groupby(['Married', 'Dependents', 'Loan_Status']).size().reset_index(name='Count')
    fig = px.bar(married_dependents, x='Married', y='Count', color='Loan_Status',
                 facet_col='Dependents', barmode='group',
                 title='Loan Approval by Marital Status & Dependents')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insight")
    st.markdown(
        """
- **Single people with no kids → Highest chance to get loan (best customers)**  
- **Married + 1 child → Also very good chance**  
- **Married + 2 children → Okay, but lower chance than 0 or 1 child**  
- **Married + 3 or more children → Very high chance of rejection**  
- **Single with 3+ kids → Very rare, but when they apply, bank usually says yes**
"""
    )

# -----------------------
# Show Final Recommendations on page if user clicked in sidebar
# -----------------------
if show_reco:
    st.markdown("---")
    st.header("💡 Final Recommendations")
    st.markdown("""
#### 1- Prioritize Credit History
- **Credit history is the strongest predictor of loan approval.** Applicants with good credit should receive priority, while those with poor or missing credit must undergo additional checks.

#### 2- Use Dependents and Marital Status as Stability Indicators
- **Applicants with 0–1 dependents show the highest approval likelihood.** Those with 3+ dependents represent high financial pressure and should be assessed more cautiously.

#### 3- Do Not Rely on Income Alone
- **Median income is similar across approved and rejected groups.** Income should always be evaluated together with loan amount, dependents, and credit history.

#### 4- Encourage Longer Loan Terms
- **Longer loan durations correlate with higher approval rates** because they reduce monthly installment pressure. Consider offering extended terms to borderline applicants.

#### 5- Incorporate Property Area into Risk Assessment
- **Semiurban applicants have the highest approval rates.** Consider slight positive adjustments for semiurban applicants and stricter checks for urban areas as needed.

#### 6- Treat Gender as a Non-Critical Factor
- **Approval differences come from application volume—not approval bias.** Gender should not materially affect model decisions.

#### 7- Investigate High-Income Rejections
- **Some high-income applicants are still rejected,** indicating other strong risk signals (e.g., poor credit history or high loan-to-income ratio). These cases require further review.
""")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Note: Insights are dataset-specific. For production decisions, validate with business rules and further testing.")
