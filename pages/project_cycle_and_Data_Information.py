import streamlit as st
import pandas as pd

# ================== PAGE SETUP ==================
st.set_page_config(
    page_title="Project Cycle & Data Info",
    layout="wide"
)

st.title("📊 Project Cycle & Data Information")

# ================== HARD-CODED DATA PATH ==================
data_path ='Data /Loan_Default_Detection_Prediction.csv'

# ================== LOAD DATA ==================
try:
    df = pd.read_csv(data_path)
    st.success("✅ Dataset loaded successfully!")
except Exception as e:
    st.error(f"🚨 Error loading dataset: {e}")
    st.stop()

# ================== DATA INFORMATION ==================
st.header("1️⃣ Dataset Overview")
st.write("Below is a preview of the dataset:")
st.dataframe(df.head(10))  # عرض أول 10 صفوف

st.subheader("Column Descriptions & Meaning")
column_info = {
    "ApplicantIncome": "Income of the applicant",
    "CoapplicantIncome": "Income of the co-applicant",
    "LoanAmount": "Requested loan amount in thousands",
    "Loan_Amount_Term": "Loan term in days",
    "Credit_History": "1 = good history, 0 = bad history",
    "Married": "Applicant marital status",
    "Dependents": "Number of dependents",
    "Property_Area": "Area type of property",
    "Loan_Status": "Target variable: Approved/Rejected"
}

for col, desc in column_info.items():
    st.markdown(f"**{col}**: {desc}")

st.subheader("Numeric Columns Description")
st.write(df.describe())

# ================== PROJECT CYCLE ==================
st.header("2️⃣ Project Cycle")
st.markdown("""
### Steps of the Project

1. **Check missing and duplicate values**  
   Checked missing values and removed duplicate rows. Nulls handled in ML pipeline.

2. **Univariate Analysis**  
   Inspected each column individually to check distributions and detect anomalies.

3. **Bivariate Analysis**  
   Analyzed relationship of each feature with the target to identify important patterns.

4. **Feature Extraction**  
   Created new features to help the model learn better and improve accuracy.

5. **Feature Importance**  
   Used correlation and ExtraTreesClassifier to identify important factors affecting loan approval.

6. **ML Pipelines**  
   Created pipelines for numeric and categorical features to handle missing values, scaling, encoding, and imbalanced classes.

7. **Model Training with Cross-Validation**  
   Trained multiple models using pipelines and cross-validation to prevent data leakage and get fair results.

8. **Choose Best Model**  
   Selected **SVM** with **84% accuracy** and **96% recall** after comparing results.

9. **Tuning**  
   Skipped parameter tuning since the dataset is small and tuning reduced performance.
""")
