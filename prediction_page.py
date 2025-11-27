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

st.title("🏦 Loan Approval Prediction App")
st.markdown("""
Welcome! This app helps you **estimate the likelihood of your loan being approved** based on the information you provide.  

We use a machine learning model trained on real loan data to give you an instant prediction.  
**How it works:**  

1. Fill in your income, loan amount, and other details below.  
2. Review the auto-calculated features (like monthly payment and income ratio).  
3. Click **Predict Loan Approval** to see the result.  

💡 *This is an estimation. Final loan approval depends on the bank's policies and documentation.*
""")


# ================== LOAD MODEL ==================
model_file = 'model/Final_model_SVM.joblib'
try:
    loaded = joblib.load(model_file)
    model = loaded if not isinstance(loaded, tuple) else loaded[0]
except Exception as e:
    st.error(f"🚨 Error loading model: {e}")
    st.stop()

# ================== USER INPUTS ==================
st.header("👤 Applicant Information")

# Main inputs as sliders
col_main1, col_main2 = st.columns(2)
with col_main1:
    applicant_income = st.slider("Applicant Income", min_value=0.0, max_value=100000.0, value=5000.0, step=100.0)
    coapplicant_income = st.slider("Coapplicant Income", min_value=0.0, max_value=50000.0, value=1500.0, step=50.0)
    total_income = applicant_income + coapplicant_income
    loan_amount = st.slider("Loan Amount (in thousands)", min_value=0.0, max_value=1000.0, value=150.0, step=5.0)
with col_main2:
    loan_term = st.slider("Loan Term (in days)", min_value=1.0, max_value=600.0, value=360.0, step=1.0)
    log_ratio = st.slider("log_Income_to_LoanRatio", min_value=0.0, max_value=10.0, value=3.0, step=0.01)
    credit_history = st.selectbox("Credit History", options=[1.0, 0.0], index=0)
    married = st.selectbox("Married", options=["Yes", "No"])
    property_area = st.selectbox("Property Area", options=["Urban", "Rural", "Semiurban"])
    dependents = st.selectbox("Dependents", options=['0', '1', '2', '3+'])

#---------------------------------------------------------------------------------------------------------
# ================== FEATURE ENGINEERING ==================
loan_monthly_paid = loan_amount * 1000 / loan_term if loan_term > 0 else 0
income_to_loan_ratio = total_income / (loan_amount * 1000) if loan_amount > 0 else 0
income_after_loan = total_income - loan_monthly_paid
#---------------------------------------------------------------------------------------------------------

# Log transforms (avoid log(0) error)
log_applicant_income = np.log(applicant_income + 1)
log_coapplicant_income = np.log(coapplicant_income + 1)
log_total_income = np.log(total_income + 1)
log_loan_amount = np.log(loan_amount + 1)
log_loan_monthly_paid = np.log(loan_monthly_paid + 1)
log_income_after_loan = np.log(max(income_after_loan, 0) + 1)

# ================== DISPLAY AUTO-CALCULATED FEATURES ==================
st.subheader("💡 Auto-calculated Features")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income= ApplicantIncome + CoapplicantIncome", f"{total_income:.2f}")
col2.metric("Monthly Loan Payment= LoanAmount / Loan_Amount_Term", f"{loan_monthly_paid:.2f}")
col3.metric("Income to Loan Ratio= Total_Income / LoanAmount", f"{income_to_loan_ratio:.2f}")
st.metric("Income After Loan= Total_Income - Monthly Loan Payment", f"{income_after_loan:.2f}")

# ================== PREDICTION ==================
if st.button("Predict Loan Approval"):
    input_data = pd.DataFrame([{
        'ApplicantIncome': applicant_income,
        'CoapplicantIncome': coapplicant_income,
        'LoanAmount': loan_amount,
        'Loan_Amount_Term': loan_term,
        'Credit_History': credit_history,
        'Married': married,
        'Property_Area': property_area,
        'Dependents': dependents,
        'Total_Income': total_income,
        'Loan_Monthly_Paid': loan_monthly_paid,
        'Income_to_LoanRatio': income_to_loan_ratio,
        'log_ApplicantIncome': log_applicant_income,
        'log_CoapplicantIncome': log_coapplicant_income,
        'log_Total_Income': log_total_income,
        'log_LoanAmount': log_loan_amount,
        'log_Loan_Monthly_Paid': log_loan_monthly_paid,
        'log_Income_After_Loan': log_income_after_loan,
        'log_Income_to_LoanRatio': log_ratio
    }])

    try:
        prediction = model.predict(input_data)
        if prediction[0] == 1:
            st.success("✅ Loan is likely to be APPROVED based on provided information.")
        else:
            st.error("❌ Loan is likely to be REJECTED based on provided information.")
    except Exception as e:
        st.error(f"🚨 Error making prediction: {e}")
