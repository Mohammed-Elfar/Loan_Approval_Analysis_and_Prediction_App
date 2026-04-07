# 3_Recommendations.py  —  Final Recommendations Page
# ------------------------------------------------------

import streamlit as st
import pandas as pd
from pathlib import Path

# ── Page config ─────────────────────────────────────────
st.set_page_config(page_title="Final Recommendations", layout="wide")

# ── Load data (for live numbers) ─────────────────────────
BASE_DIR  = Path(__file__).parent
DATA_PATH = BASE_DIR.parent / "data" / 'Data /Loan_Default_Detection_Prediction.csv'

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "Total_Income" not in df.columns:
        df["Total_Income"] = (
            df.get("ApplicantIncome", pd.Series(0)).fillna(0)
            + df.get("CoapplicantIncome", pd.Series(0)).fillna(0)
        )
    return df

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error("Dataset not found. Place your CSV at `data/Loan_Default_Detection_Prediction.csv`.")
    st.stop()

# ── Pre-compute stats ─────────────────────────────────────
total        = len(df)
approved     = (df["Loan_Status"] == "Y").sum()
approval_pct = approved / total * 100

good_credit_rate = df[df["Credit_History"] == 1]["Loan_Status"].eq("Y").mean() * 100
bad_credit_rate  = df[df["Credit_History"] == 0]["Loan_Status"].eq("Y").mean() * 100

median_approved  = df[df["Loan_Status"] == "Y"]["Total_Income"].median()
median_rejected  = df[df["Loan_Status"] == "N"]["Total_Income"].median()

term_360     = df[df["Loan_Amount_Term"] == 360]
rate_360     = (term_360["Loan_Status"] == "Y").mean() * 100 if len(term_360) > 0 else 0

# ── Header ────────────────────────────────────────────────
st.title("💡 Final Recommendations")
st.markdown(
    "Actionable conclusions for the lending team based on the full dataset analysis. "
    "All numbers are computed live from the data."
)
st.markdown("---")

# ════════════════════════════════════════════════════════
#  RECOMMENDATION CARDS  (2-column grid)
# ════════════════════════════════════════════════════════

recommendations = [
    {
        "icon": "🏆",
        "title": "1. Prioritize Credit History Above Everything",
        "priority": "Critical",
        "priority_color": "error",
        "body": (
            f"Good credit applicants are approved at **{good_credit_rate:.1f}%**, "
            f"while poor credit applicants are approved at only **{bad_credit_rate:.1f}%** — "
            f"a gap of **{good_credit_rate - bad_credit_rate:.1f} percentage points**.  \n\n"
            "Credit history is the single strongest predictor in the dataset. "
            "Applicants with poor or missing credit must go through manual review "
            "and provide additional supporting documentation before approval."
        ),
    },
    {
        "icon": "👨‍👩‍👧",
        "title": "2. Use Dependents as a Financial Pressure Signal",
        "priority": "High",
        "priority_color": "warning",
        "body": (
            "Applicants with **0–1 dependents** show the highest approval likelihood. "
            "Those with **3+ dependents** represent significantly higher household financial pressure "
            "and face the highest rejection rates.  \n\n"
            "Use dependent count as a soft risk-adjustment factor in scoring — "
            "not as a hard rejection trigger, but as a flag for deeper income-to-obligation review."
        ),
    },
    {
        "icon": "💰",
        "title": "3. Never Rely on Income Alone",
        "priority": "High",
        "priority_color": "warning",
        "body": (
            f"Median total income for **approved** applicants: ₹{median_approved:,.0f}  \n"
            f"Median total income for **rejected** applicants: ₹{median_rejected:,.0f}  \n\n"
            "The difference is minimal — confirming that income alone does not drive approval. "
            "High earners are still rejected when credit history or loan-to-income ratio is unfavorable.  \n\n"
            "Always evaluate income together with credit history, loan amount, and number of dependents."
        ),
    },
    {
        "icon": "📅",
        "title": "4. Encourage Longer Loan Terms for Borderline Cases",
        "priority": "Medium",
        "priority_color": "info",
        "body": (
            f"The 360-day term dominates the dataset and carries a **{rate_360:.1f}%** approval rate.  \n\n"
            "Longer repayment periods reduce monthly installment burden, making applicants "
            "appear more financially capable on paper.  \n\n"
            "For borderline applicants who are otherwise qualified, "
            "offering an extended term is a low-cost way to improve approval outcomes "
            "without meaningfully increasing default risk."
        ),
    },
    {
        "icon": "🏠",
        "title": "5. Factor Property Area Into Risk Assessment",
        "priority": "Medium",
        "priority_color": "info",
        "body": (
            "**Semiurban** applicants consistently show the highest approval rates, "
            "likely reflecting more stable property valuations and stronger collateral reliability.  \n\n"
            "Property area should be used as a mild risk-adjustment signal — "
            "a slight positive weight for semiurban and a flag for additional checks in "
            "high-density urban areas where property risk is more variable."
        ),
    },
    {
        "icon": "⚖️",
        "title": "6. Do Not Let Gender Influence Decisions",
        "priority": "Low",
        "priority_color": "success",
        "body": (
            "Approval *rates* between male and female applicants are nearly identical. "
            "The count difference in raw data comes from application frequency, not approval bias.  \n\n"
            "Gender must not materially influence model scores or manual review decisions. "
            "This finding should be documented to support fairness and compliance reporting."
        ),
    },
    {
        "icon": "🔍",
        "title": "7. Audit High-Income Rejections Separately",
        "priority": "Medium",
        "priority_color": "info",
        "body": (
            "A subset of high-income applicants are still rejected — "
            "indicating overriding risk signals such as poor credit history, "
            "an unfavorable loan-to-income ratio, or high dependent count.  \n\n"
            "Flag these cases for a dedicated review pipeline. "
            "Understanding why high earners are rejected can reveal underwriting "
            "rules that may be overly conservative or incorrectly calibrated."
        ),
    },
]

# ── Render in 2-column grid ───────────────────────────────
left_col, right_col = st.columns(2)

for i, rec in enumerate(recommendations):
    col = left_col if i % 2 == 0 else right_col
    with col:
        # Priority badge + title
        badge_fn = {
            "error":   st.error,
            "warning": st.warning,
            "info":    st.info,
            "success": st.success,
        }.get(rec["priority_color"], st.info)

        st.markdown(f"### {rec['icon']} {rec['title']}")
        badge_fn(f"Priority: **{rec['priority']}**")
        st.markdown(rec["body"])
        st.markdown("---")

# ── Summary callout ───────────────────────────────────────
st.subheader("📋 Quick Reference Priority Order")

priority_table = pd.DataFrame({
    "Recommendation":  [r["title"].split(". ", 1)[1] for r in recommendations],
    "Priority":        [r["priority"] for r in recommendations],
})
st.dataframe(priority_table, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Recommendations are derived from this dataset only. "
    "Validate with business rules, legal requirements, and further testing before production use."
)
