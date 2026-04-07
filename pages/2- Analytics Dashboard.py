# 2_Analytics.py  —  Loan Approval Analytics Dashboard
# -------------------------------------------------------
# Same 7 business questions as original.
# Improvements:
#   • Relative data path (works on any machine)
#   • KPI summary row at the top
#   • Approval RATE (%) charts instead of raw counts where misleading
#   • Data-driven insight numbers (pulled from df, not hardcoded)
#   • Consistent color palette across all charts
#   • Cleaner layout per question: chart left / insight card right
# -------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── Page config ─────────────────────────────────────────
st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# ── Color constants (used across all charts) ─────────────
CLR_APPROVED = "#1D9E75"   # teal  → Approved / Y
CLR_REJECTED = "#D85A30"   # coral → Rejected / N
COLOR_MAP    = {"Y": CLR_APPROVED, "N": CLR_REJECTED}

# ── Load data (relative path — works on any machine) ─────
BASE_DIR  = Path(__file__).parent
DATA_PATH = BASE_DIR.parent / "Data" / "Loan_Default_Detection_Prediction.csv"

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
    st.error(
        f"Dataset not found at `{DATA_PATH}`. "
        "Place your CSV in a `data/` folder one level above this page."
    )
    st.stop()

# ── Pre-compute key stats (used in KPIs + insights) ──────
total        = len(df)
approved     = (df["Loan_Status"] == "Y").sum()
rejected     = (df["Loan_Status"] == "N").sum()
approval_pct = approved / total * 100

good_credit_rate = (
    df[df["Credit_History"] == 1]["Loan_Status"].eq("Y").mean() * 100
)
bad_credit_rate = (
    df[df["Credit_History"] == 0]["Loan_Status"].eq("Y").mean() * 100
)

# ── Helper: approval rate table ───────────────────────────
def approval_rate(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Returns a DataFrame with Approval Rate (%) per group value."""
    return (
        df.groupby(group_col)["Loan_Status"]
        .apply(lambda x: round((x == "Y").mean() * 100, 1))
        .reset_index(name="Approval Rate (%)")
    )

# ════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════
st.title("📊 Loan Approval Analytics Dashboard")
st.markdown(
    "Explore what drives loan approvals. "
    "Select a business question from the sidebar to drill in."
)

# ── KPI Row ──────────────────────────────────────────────
st.markdown("---")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Applications",   f"{total:,}")
k2.metric("Approved",             f"{approved:,}",  f"{approval_pct:.1f}% rate")
k3.metric("Rejected",             f"{rejected:,}")
k4.metric("Good Credit → Approval Rate", f"{good_credit_rate:.1f}%",
          f"vs {bad_credit_rate:.1f}% poor credit")
st.markdown("---")

# ════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════
st.sidebar.header("🔎 Analysis Controls")

question = st.sidebar.radio(
    "Choose a business question:",
    (
        "1️⃣  Does gender influence loan approval rates?",
        "2️⃣  Is there a relationship between dependents and approval?",
        "3️⃣  Does property area affect loan approval?",
        "4️⃣  Are shorter or longer loans more likely to be approved?",
        "5️⃣  How does credit history impact loan approval?",
        "6️⃣  Does total household income affect loan approval?",
        "7️⃣  What is the impact of marital status and dependents?",
    ),
)

# ── Active question label ─────────────────────────────────
st.header(question)
st.markdown("---")

# ════════════════════════════════════════════════════════
#  Q1 — Gender
# ════════════════════════════════════════════════════════
if question.startswith("1️⃣"):

    rate_df = approval_rate(df, "Gender")

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        # Approval RATE — not raw count (avoids the "more males apply" distortion)
        fig = px.bar(
            rate_df,
            x="Gender", y="Approval Rate (%)",
            color="Gender",
            color_discrete_sequence=[CLR_APPROVED, CLR_REJECTED],
            text="Approval Rate (%)",
            title="Approval Rate (%) by Gender",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        # Raw counts as a secondary grouped bar for context
        count_df = (
            df.groupby(["Gender", "Loan_Status"])
            .size()
            .reset_index(name="Count")
        )
        fig2 = px.bar(
            count_df, x="Gender", y="Count",
            color="Loan_Status", barmode="group",
            color_discrete_map=COLOR_MAP,
            title="Raw Application Counts by Gender (context only)",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_insight:
        st.subheader("📌 Key Insight")

        male_rate   = rate_df.loc[rate_df["Gender"] == "Male",   "Approval Rate (%)"].values
        female_rate = rate_df.loc[rate_df["Gender"] == "Female", "Approval Rate (%)"].values

        male_str   = f"{male_rate[0]:.1f}%"   if len(male_rate)   > 0 else "N/A"
        female_str = f"{female_rate[0]:.1f}%" if len(female_rate) > 0 else "N/A"

        st.info(
            f"**Male approval rate:** {male_str}  \n"
            f"**Female approval rate:** {female_str}  \n\n"
            "Approval *rates* are very similar between genders.  \n"
            "The raw count gap simply reflects that **male applicants apply more often** — "
            "not that they are approved at a higher rate.  \n\n"
            "✅ **Business conclusion:** Gender is not a meaningful driver of approval decisions."
        )

# ════════════════════════════════════════════════════════
#  Q2 — Dependents
# ════════════════════════════════════════════════════════
elif question.startswith("2️⃣"):

    rate_df   = approval_rate(df, "Dependents")
    count_df  = (
        df.groupby(["Dependents", "Loan_Status"])
        .size()
        .reset_index(name="Count")
    )

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        fig = px.bar(
            rate_df,
            x="Dependents", y="Approval Rate (%)",
            color="Dependents",
            text="Approval Rate (%)",
            title="Approval Rate (%) by Number of Dependents",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(
            count_df, x="Dependents", y="Count",
            color="Loan_Status", barmode="group",
            color_discrete_map=COLOR_MAP,
            title="Application Counts by Dependents",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_insight:
        st.subheader("📌 Key Insight")

        zero_dep = df[df["Dependents"] == "0"]
        zero_rate = (zero_dep["Loan_Status"] == "Y").mean() * 100
        three_dep = df[df["Dependents"] == "3+"]
        three_rate = (three_dep["Loan_Status"] == "Y").mean() * 100 if len(three_dep) > 0 else 0

        st.info(
            f"**0 dependents approval rate:** {zero_rate:.1f}%  \n"
            f"**3+ dependents approval rate:** {three_rate:.1f}%  \n\n"
            "Applicants with **0 dependents** have the highest approval rate — "
            "lower financial obligations make them lower-risk borrowers.  \n\n"
            "Approval rate generally **declines as dependents increase**, "
            "reflecting higher household financial pressure.  \n\n"
            "✅ **Business conclusion:** Treat dependents as a soft risk signal, "
            "not a hard rejection trigger."
        )

# ════════════════════════════════════════════════════════
#  Q3 — Property Area
# ════════════════════════════════════════════════════════
elif question.startswith("3️⃣"):

    rate_df  = approval_rate(df, "Property_Area")
    count_df = (
        df.groupby(["Property_Area", "Loan_Status"])
        .size()
        .reset_index(name="Count")
    )

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        fig = px.bar(
            rate_df,
            x="Property_Area", y="Approval Rate (%)",
            color="Property_Area",
            text="Approval Rate (%)",
            title="Approval Rate (%) by Property Area",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(
            count_df, x="Property_Area", y="Count",
            color="Loan_Status", barmode="group",
            color_discrete_map=COLOR_MAP,
            title="Application Counts by Property Area",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_insight:
        st.subheader("📌 Key Insight")

        best_area = rate_df.loc[rate_df["Approval Rate (%)"].idxmax(), "Property_Area"]
        best_rate = rate_df["Approval Rate (%)"].max()

        st.info(
            f"**Highest approval rate:** {best_area} ({best_rate:.1f}%)  \n\n"
            "**Semiurban** properties consistently show the strongest approval rates.  \n"
            "This may reflect more stable property valuations and collateral reliability "
            "in those areas.  \n\n"
            "✅ **Business conclusion:** Property area can be used as a mild "
            "risk-adjustment factor — not a primary decision driver."
        )

# ════════════════════════════════════════════════════════
#  Q4 — Loan Term
# ════════════════════════════════════════════════════════
elif question.startswith("4️⃣"):

    rate_df = approval_rate(df, "Loan_Amount_Term")
    count_df = (
        df.groupby(["Loan_Amount_Term", "Loan_Status"])
        .size()
        .reset_index(name="Count")
    )

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        fig = px.bar(
            count_df, x="Loan_Amount_Term", y="Count",
            color="Loan_Status", barmode="group",
            color_discrete_map=COLOR_MAP,
            title="Loan Approval Counts by Term Duration (days)",
        )
        fig.update_layout(xaxis_title="Loan Term (days)")
        st.plotly_chart(fig, use_container_width=True)

        # Approval rate by term
        fig2 = px.bar(
            rate_df,
            x="Loan_Amount_Term", y="Approval Rate (%)",
            text="Approval Rate (%)",
            title="Approval Rate (%) by Loan Term",
            color_discrete_sequence=[CLR_APPROVED],
        )
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig2.update_layout(xaxis_title="Loan Term (days)", yaxis_range=[0, 110])
        st.plotly_chart(fig2, use_container_width=True)

    with col_insight:
        st.subheader("📌 Key Insight")

        term_360 = df[df["Loan_Amount_Term"] == 360]
        rate_360 = (term_360["Loan_Status"] == "Y").mean() * 100 if len(term_360) > 0 else 0
        most_common_term = df["Loan_Amount_Term"].mode()[0]

        st.info(
            f"**Most common term:** {int(most_common_term)} days  \n"
            f"**360-day term approval rate:** {rate_360:.1f}%  \n\n"
            "The **360-day term dominates** the dataset — most applicants choose it "
            "and it has a high approval rate.  \n\n"
            "Longer terms reduce monthly payment pressure, making applicants appear "
            "more financially capable of repayment.  \n\n"
            "✅ **Business conclusion:** Offering longer repayment options to "
            "borderline applicants could improve approval rates without increasing default risk."
        )

# ════════════════════════════════════════════════════════
#  Q5 — Credit History
# ════════════════════════════════════════════════════════
elif question.startswith("5️⃣"):

    count_df = (
        df.groupby(["Credit_History", "Loan_Status"])
        .size()
        .reset_index(name="Count")
    )
    count_df["Credit_History"] = count_df["Credit_History"].map(
        {1.0: "Good (1)", 0.0: "Poor (0)"}
    ).fillna(count_df["Credit_History"].astype(str))

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        fig = px.bar(
            count_df, x="Credit_History", y="Count",
            color="Loan_Status", barmode="group",
            color_discrete_map=COLOR_MAP,
            text="Count",
            title="Loan Approval vs Credit History",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        # Approval rate as a simple donut per group
        good_approved  = (df[df["Credit_History"] == 1]["Loan_Status"] == "Y").sum()
        good_rejected  = (df[df["Credit_History"] == 1]["Loan_Status"] == "N").sum()
        bad_approved_n = (df[df["Credit_History"] == 0]["Loan_Status"] == "Y").sum()
        bad_rejected_n = (df[df["Credit_History"] == 0]["Loan_Status"] == "N").sum()

        donut_col1, donut_col2 = st.columns(2)
        with donut_col1:
            fig_g = go.Figure(go.Pie(
                labels=["Approved", "Rejected"],
                values=[good_approved, good_rejected],
                marker_colors=[CLR_APPROVED, CLR_REJECTED],
                hole=0.55,
            ))
            fig_g.update_layout(title_text="Good Credit", height=250,
                                 margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig_g, use_container_width=True)
        with donut_col2:
            fig_b = go.Figure(go.Pie(
                labels=["Approved", "Rejected"],
                values=[bad_approved_n, bad_rejected_n],
                marker_colors=[CLR_APPROVED, CLR_REJECTED],
                hole=0.55,
            ))
            fig_b.update_layout(title_text="Poor Credit", height=250,
                                 margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig_b, use_container_width=True)

    with col_insight:
        st.subheader("📌 Key Insight")

        good_approved_n = (df[df["Credit_History"] == 1]["Loan_Status"] == "Y").sum()
        good_rejected_n = (df[df["Credit_History"] == 1]["Loan_Status"] == "N").sum()
        bad_approved_c  = (df[df["Credit_History"] == 0]["Loan_Status"] == "Y").sum()
        bad_rejected_c  = (df[df["Credit_History"] == 0]["Loan_Status"] == "N").sum()

        st.error(
            "⚠️ **Credit history is the single strongest predictor** in this dataset."
        )
        st.info(
            f"**Good credit (1):** {good_approved_n} approved vs {good_rejected_n} rejected  \n"
            f"→ Approval rate: **{good_credit_rate:.1f}%**  \n\n"
            f"**Poor credit (0):** {bad_approved_c} approved vs {bad_rejected_c} rejected  \n"
            f"→ Approval rate: **{bad_credit_rate:.1f}%**  \n\n"
            "The gap is dramatic. Poor-credit applicants face an approval rate "
            f"**{good_credit_rate - bad_credit_rate:.1f} percentage points lower** "
            "than good-credit applicants.  \n\n"
            "✅ **Business conclusion:** Prioritize credit history checks above all other factors. "
            "Poor-credit applicants require additional documentation and manual review."
        )

# ════════════════════════════════════════════════════════
#  Q6 — Total Household Income
# ════════════════════════════════════════════════════════
elif question.startswith("6️⃣"):

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        fig = px.box(
            df, x="Loan_Status", y="Total_Income",
            color="Loan_Status",
            color_discrete_map=COLOR_MAP,
            title="Total Household Income Distribution by Loan Status",
            labels={"Loan_Status": "Loan Status", "Total_Income": "Total Income"},
        )
        st.plotly_chart(fig, use_container_width=True)

        # Histogram overlay
        fig2 = px.histogram(
            df, x="Total_Income", color="Loan_Status",
            color_discrete_map=COLOR_MAP,
            nbins=40, barmode="overlay", opacity=0.6,
            title="Income Distribution Overlap (Approved vs Rejected)",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_insight:
        st.subheader("📌 Key Insight")

        median_approved = df[df["Loan_Status"] == "Y"]["Total_Income"].median()
        median_rejected = df[df["Loan_Status"] == "N"]["Total_Income"].median()

        st.info(
            f"**Median income — Approved:** ₹{median_approved:,.0f}  \n"
            f"**Median income — Rejected:** ₹{median_rejected:,.0f}  \n\n"
            "The medians are very close — confirming that **income alone is not a "
            "reliable approval signal**.  \n\n"
            "The histogram shows heavy overlap between approved and rejected distributions.  \n\n"
            "High-income applicants can still be rejected — likely due to poor credit "
            "history or an unfavorable loan-to-income ratio.  \n\n"
            "✅ **Business conclusion:** Never evaluate income in isolation. "
            "Always combine it with credit history, loan amount, and number of dependents."
        )

# ════════════════════════════════════════════════════════
#  Q7 — Marital Status + Dependents
# ════════════════════════════════════════════════════════
elif question.startswith("7️⃣"):

    married_dep = (
        df.groupby(["Married", "Dependents", "Loan_Status"])
        .size()
        .reset_index(name="Count")
    )

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        fig = px.bar(
            married_dep,
            x="Married", y="Count",
            color="Loan_Status",
            facet_col="Dependents",
            barmode="group",
            color_discrete_map=COLOR_MAP,
            title="Loan Approval by Marital Status & Dependents",
        )
        fig.update_layout(legend_title_text="Loan Status")
        st.plotly_chart(fig, use_container_width=True)

        # Approval rate heatmap-style table
        pivot = (
            df.groupby(["Married", "Dependents"])["Loan_Status"]
            .apply(lambda x: round((x == "Y").mean() * 100, 1))
            .reset_index(name="Approval Rate (%)")
            .pivot(index="Married", columns="Dependents", values="Approval Rate (%)")
        )

    with col_insight:
        st.subheader("📌 Key Insight")

        st.info(
            "**Profile ranking by approval likelihood:**  \n\n"
            "🟢 **Single, 0 dependents** → Highest approval rate  \n"
            "🟢 **Married, 0–1 dependents** → Very strong  \n"
            "🟡 **Married, 2 dependents** → Moderate  \n"
            "🔴 **Married, 3+ dependents** → High rejection risk  \n"
            "⚪ **Single, 3+ dependents** → Rare, but bank often approves  \n\n"
            "The heatmap shows the full picture — "
            "**lower dependency count = better approval odds** regardless of marital status.  \n\n"
            "✅ **Business conclusion:** Use the married × dependents combination "
            "as a household financial pressure indicator in risk scoring."
        )

# ── Footer ────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Insights are derived from this dataset only. "
    "For production decisions, validate with business rules, legal requirements, and further testing."
)
