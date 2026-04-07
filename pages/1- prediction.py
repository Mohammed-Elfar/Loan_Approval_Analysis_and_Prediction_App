import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ================== PAGE SETUP ==================
st.set_page_config(
    page_title="Loan Approval Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(" Loan Approval Prediction")
st.caption("Fill in the applicant details below to get an instant prediction from our ML model.")
st.divider()

# ================== LOAD MODEL ==================
model_file = '/Users/mohammedmahmood/Desktop/Data projects/Projects/Data science/Supervised /Loan Default Detection Prediction/4.model/Final_model_SVM.joblib'
try:
    loaded = joblib.load(model_file)
    model = loaded if not isinstance(loaded, tuple) else loaded[0]
except Exception as e:
    st.error(f"🚨 Error loading model: {e}")
    st.stop()

# ================== SECTION 1: FINANCIAL DETAILS ==================
st.subheader("1- Financial Details")

col1, col2, col3 = st.columns(3)
with col1:
    applicant_income = st.slider("Applicant Income", min_value=0.0, max_value=100000.0, value=5000.0, step=100.0)
with col2:
    coapplicant_income = st.slider("Coapplicant Income", min_value=0.0, max_value=50000.0, value=1500.0, step=50.0)
with col3:
    loan_amount = st.slider("Loan Amount (thousands)", min_value=0.0, max_value=1000.0, value=150.0, step=5.0)

total_income = applicant_income + coapplicant_income

st.divider()

# ================== SECTION 2: LOAN DETAILS ==================
st.subheader("2- Loan Details")

col4, col5, col6 = st.columns(3)
with col4:
    loan_term = st.slider("Loan Term (days)", min_value=1.0, max_value=600.0, value=360.0, step=1.0)
with col5:
    log_ratio = st.slider("Income to Loan Ratio (log)", min_value=12.09, max_value=396.370, value=300.0, step=0.1)
with col6:
    credit_history = st.selectbox("Credit History", options=[1.0, 0.0], index=0,
                                  help="1 = Good credit history | 0 = Bad credit history")

st.divider()

# ================== SECTION 3: PERSONAL DETAILS ==================
st.subheader("3- Personal Details")

col7, col8, col9 = st.columns(3)
with col7:
    married = st.selectbox("Married", options=["Yes", "No"])
with col8:
    dependents = st.selectbox("Dependents", options=['0', '1', '2', '3+'])
with col9:
    property_area = st.selectbox("Property Area", options=["Urban", "Rural", "Semiurban"])

st.divider()

# ================== FEATURE ENGINEERING (unchanged logic) ==================
loan_monthly_paid = loan_amount * 1000 / loan_term if loan_term > 0 else 0
income_to_loan_ratio = total_income / (loan_amount * 1000) if loan_amount > 0 else 0
income_after_loan = total_income - loan_monthly_paid

log_applicant_income    = np.log(applicant_income + 1)
log_coapplicant_income  = np.log(coapplicant_income + 1)
log_total_income        = np.log(total_income + 1)
log_loan_amount         = np.log(loan_amount + 1)
log_loan_monthly_paid   = np.log(loan_monthly_paid + 1)
log_income_after_loan   = np.log(max(income_after_loan, 0) + 1)
log_Income_to_LoanRatio = np.log(income_to_loan_ratio + 1)

# ================== AUTO-CALCULATED FEATURES ==================
st.subheader("🔢 Auto-Calculated Features")
st.caption("These values are derived automatically from your inputs above.")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Income",          f"{total_income:,.2f}",        help="Applicant Income + Coapplicant Income")
m2.metric("Monthly Loan Payment",  f"{loan_monthly_paid:,.2f}",   help="Loan Amount × 1000 ÷ Loan Term")
m3.metric("Income to Loan Ratio",  f"{income_to_loan_ratio:.4f}", help="Total Income ÷ Loan Amount")
m4.metric("Income After Loan",     f"{income_after_loan:,.2f}",   help="Total Income − Monthly Loan Payment")

st.divider()

# ================== PREDICTION ==================
col_btn, _ = st.columns([1, 3])
with col_btn:
    predict_clicked = st.button("🔍 Predict Loan Approval", use_container_width=True, type="primary")

if predict_clicked:
    input_data = pd.DataFrame([{
        'ApplicantIncome':        applicant_income,
        'CoapplicantIncome':      coapplicant_income,
        'LoanAmount':             loan_amount,
        'Loan_Amount_Term':       loan_term,
        'Credit_History':         credit_history,
        'Married':                married,
        'Property_Area':          property_area,
        'Dependents':             dependents,
        'Total_Income':           total_income,
        'Loan_Monthly_Paid':      loan_monthly_paid,
        'Income_to_LoanRatio':    income_to_loan_ratio,
        'log_ApplicantIncome':    log_applicant_income,
        'log_CoapplicantIncome':  log_coapplicant_income,
        'log_Total_Income':       log_total_income,
        'log_LoanAmount':         log_loan_amount,
        'log_Loan_Monthly_Paid':  log_loan_monthly_paid,
        'log_Income_After_Loan':  log_income_after_loan,
        'log_Income_to_LoanRatio': log_ratio
    }])

    try:
        prediction = model.predict(input_data)
        st.divider()
        if prediction[0] == 1:
            st.success("✅  **Loan Likely APPROVED**  — The model predicts this application meets approval criteria.")
        else:
            st.error("❌  **Loan Likely REJECTED**  — The model predicts this application does not meet approval criteria.")

        st.caption("⚠️ This is a model estimate only. Final approval depends on the bank's policies and documentation.")

    except Exception as e:
        st.error(f"🚨 Error making prediction: {e}")