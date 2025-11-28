## Note
**For Interactive notebook & full analysis (plots + code) are hosted on Kaggle.**  
🔗 **Kaggle Notebook (interactive):** 
https://www.kaggle.com/code/mohammadelfar/loan-approval-prediction-84-acc-95-recall/edit

# Loan Approval Analysis & Prediction App

- The goal is to predict loan approval based on applicant financial and customer information, deployed the model using Streamlit, allowing users to input new order details and instantly get a prediction on whether the product is likely to be returned.
I also added an Analytics & Insights page, where users can view all the analysis, insights, and final recommendations extracted from the data.

- I chose this dataset because it presents several challenges: it is relatively small with about 615 rows, and contains many missing values and outliers.
I addressed these issues through data preprocessing and was able to achieve an accuracy of 81%, which is a strong result given the limited size of the data.

Link of the app: https://loan-approval-analysis-and-prediction-app.streamlit.app/

### Approach & Steps:

1️⃣ Data Quality Check
Review data types, missing values, and duplicates.

2️⃣ Univariate Analysis
Explore each column individually to understand distributions and detect issues.

3️⃣ Bivariate & Multivariate Analysis
Examine feature interactions to reveal deeper patterns.

4️⃣ Feature Engineering
Create new features to improve model performance.

5️⃣ Feature Importance
Identify the most impactful features using correlation and ExtraTreesClassifier.

6️⃣ ML Pipelines
Build pipelines for preprocessing, encoding, scaling, and handling class imbalance.

7️⃣ Model Training
Train multiple ML models with cross-validation.

8️⃣ Model Selection
Choose the best model based on performance metrics (XGBoost here).

9️⃣ Hyperparameter Tuning
Optimize the model using GridSearchCV.

🔟 Deployment
Deploy the model using Streamlit for real-time return prediction.
