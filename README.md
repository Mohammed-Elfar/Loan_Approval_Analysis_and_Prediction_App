Loan Approval Analysis & Prediction App

The goal is to predict loan approval based on applicant financial and customer information, deployed the model using Streamlit, allowing users to input new order details and instantly get a prediction on whether the product is likely to be returned.
I also added an Analytics & Insights page, where users can view all the analysis, insights, and final recommendations extracted from the data.

I chose this dataset because it presents several challenges: it is relatively small with about 615 rows, and contains many missing values and outliers.
I addressed these issues through data preprocessing and was able to achieve an accuracy of 81%, which is a strong result given the limited size of the data.

Link of the app: Loan Approval Analysis & Prediction App

Approach & Steps:

1️⃣ Data Cleaning
I started with a complete data cleaning process: checking missing values, fixing data types, and removing duplicates — until the dataset was clean and ready for analysis and ML.

2️⃣ Univariate Analysis
I went through each column individually to identify any issues, studied distributions, checked outliers, and performed EDA to gain a deeper understanding of every feature.

3️⃣ Detailed Exploratory Analysis (Bivariate & Multivariate Analysis)
I explored relationships between variables, which helped me identify valuable patterns such as:
– which product categories have the highest return rates
– which customer segments tend to return items more
– how different features like taxes, rating, payment method, and price affect return probability

From this analysis, I generated strong insights and created clear recommendations for the business based on data-driven patterns.

4️⃣ Feature Engineering
I created new features that improved the model’s ability to capture hidden patterns.
I also used a Correlation Matrix + ExtraTreesClassifier to identify the most important features and remove weak ones.

5️⃣ ML Pipelines
I built clean and automated ML pipelines for both numerical and categorical data — including encoding, scaling, and handling class imbalance — all without any data leakage.

6️⃣ Model Training & Tuning
I trained multiple models using full cross-validation to choose the best one and then applied hyperparameter tuning.
XGBoost turned out to be the most stable and best-performing model.

Final Model Results after tuning:
• Train Accuracy: 0.9784
• Test Accuracy: 0.9755
• Train Recall: 0.8917
• Test Recall: 0.8793
• Train Precision: 0.9015
• Test Precision: 0.8867

7️⃣ Deployment
I deployed the model using Streamlit, allowing users to input new order details and instantly get a prediction on whether the product is likely to be returned.
I also added an Analytics & Insights page, where users can view all the analysis, insights, and final recommendations extracted from the data.
