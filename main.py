import streamlit as st
import pandas as pd

# ================== PAGE SETUP ==================
st.set_page_config(
    page_title="Loan Approval — Project Overview",
    layout="wide"
)

# ================== HERO SECTION ==================
st.title(" Loan Default Detection & Prediction")
st.markdown(
    "A supervised machine learning project that predicts whether a loan application will be **approved or rejected**, "
    "using an **SVM model** with **84% accuracy** and **96% recall**."
)
st.divider()

# ================== KEY METRICS ROW ==================
st.subheader(" Project at a Glance")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Model",       "SVM Classifier")
k2.metric("Accuracy",    "84%")
k3.metric("Recall",      "96%")
k4.metric("Validation",  "ML Pipeline + CV (5-Fold)")

st.divider()

# ================== LOAD DATA ==================
data_path = '/Users/mohammedmahmood/Desktop/Data projects/Projects/Data science/Supervised /Loan Default Detection Prediction/2.Data /Loan_Default_Detection_Prediction.csv'

try:
    df = pd.read_csv(data_path)
except Exception as e:
    st.error(f" Error loading dataset: {e}")
    st.stop()

# ================== DATASET OVERVIEW ==================
st.header("1️⃣ Dataset Overview")

tab1, tab2, tab3 = st.tabs(["📄 Preview", "📐 Shape & Types", "📊 Statistics"])

with tab1:
    st.caption("First 10 rows of the dataset.")
    st.dataframe(df.head(10), use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Rows:** `{df.shape[0]}`   |   **Columns:** `{df.shape[1]}`")
        st.dataframe(
            pd.DataFrame({"Column": df.columns, "Type": df.dtypes.values}).reset_index(drop=True),
            use_container_width=True
        )
    with c2:
        missing = df.isnull().sum().reset_index()
        missing.columns = ["Column", "Missing Values"]
        missing["Missing %"] = (missing["Missing Values"] / len(df) * 100).round(2)
        st.caption("Missing values per column:")
        st.dataframe(missing, use_container_width=True)

with tab3:
    st.dataframe(df.describe(), use_container_width=True)

st.divider()

# ================== COLUMN DESCRIPTIONS ==================
st.header("2️⃣ Feature Descriptions")
st.caption("What each column in the dataset represents.")

column_info = {
    "ApplicantIncome":   ("💵", "Income of the loan applicant"),
    "CoapplicantIncome": ("💵", "Income of the co-applicant (spouse or partner)"),
    "LoanAmount":        ("💰", "Requested loan amount in thousands"),
    "Loan_Amount_Term":  ("📅", "Duration of the loan in days"),
    "Credit_History":    ("📋", "1 = Good credit history  |  0 = Bad credit history"),
    "Married":           ("💍", "Marital status of the applicant"),
    "Dependents":        ("👨‍👩‍👧", "Number of people financially dependent on the applicant"),
    "Property_Area":     ("🏘️", "Area type of the applicant's property (Urban / Rural / Semiurban)"),
    "Loan_Status":       ("🎯", "Target variable — Approved (Y) or Rejected (N)"),
}

col_a, col_b = st.columns(2)
items = list(column_info.items())
half = len(items) // 2 + len(items) % 2

with col_a:
    for col, (icon, desc) in items[:half]:
        st.markdown(f"{icon} **{col}**  \n{desc}")
        st.write("")

with col_b:
    for col, (icon, desc) in items[half:]:
        st.markdown(f"{icon} **{col}**  \n{desc}")
        st.write("")

st.divider()

# ================== PROJECT CYCLE ==================
st.header("3️⃣ Project Cycle")
st.caption("The end-to-end steps followed to build this model.")

steps = [
    ("🔍", "Data Cleaning",
     "Checked for missing values and removed duplicate rows. Nulls are handled later inside the ML pipeline to avoid data leakage."),
    ("📊", "Univariate Analysis",
     "Inspected each feature individually to understand its distribution, detect outliers, and spot any anomalies."),
    ("🔗", "Bivariate Analysis",
     "Examined the relationship between each feature and the target variable (Loan Status) to identify the most informative patterns."),
    ("⚙️", "Feature Engineering",
     "Created new derived features such as Total Income, Monthly Loan Payment, Income-to-Loan Ratio, and log-transformed versions to help the model learn better."),
    ("🏆", "Feature Importance",
     "Used Pearson correlation and ExtraTreesClassifier to rank features and understand which factors most influence loan approval."),
    ("🔧", "ML Pipelines",
     "Built separate pipelines for numeric and categorical features covering imputation, scaling, encoding, and class imbalance handling (SMOTE Tomek Links)."),
    ("🔁", "Model Training & Cross-Validation",
     "Trained multiple classifiers (Logistic Regression, Decision Tree, Random Forest, SVM) using cross-validation and pipelined preprocessing to get unbiased performance estimates and prevent data leakage."),
    ("🥇", "Model Selection",
     "Selected SVM as the best model with 84% accuracy and 96% recall — minimizing false rejections is the priority in a loan use case."),
    ("⚡", "Hyperparameter Tuning",
     "Skipped extensive tuning since the dataset is small and grid search actually reduced performance — the default SVM configuration was optimal."),
]

for i, (icon, title, detail) in enumerate(steps, 1):
    with st.expander(f"**Step {i} — {icon} {title}**"):
        st.write(detail)

st.divider()
st.caption("💡 Use the sidebar to navigate to the **Prediction Page** and try the model live.")