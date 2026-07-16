# 📞 Project 3 – Telco Customer Churn Prediction

## 📖 Project Overview

Customer churn is one of the biggest challenges in the telecommunications industry. Losing existing customers can significantly impact company revenue and increase customer acquisition costs.

This project develops a machine learning model to predict whether a customer is likely to churn based on demographic information, subscribed services, contract details, and billing history. The project follows an end-to-end data science workflow, including data preprocessing, exploratory data analysis (EDA), feature engineering, model development, evaluation, and deployment using Streamlit.

---

## 🎯 Objectives

- Analyze customer characteristics and subscription behavior.
- Identify factors contributing to customer churn.
- Build a machine learning model to predict customer churn.
- Evaluate classification model performance.
- Deploy the model as an interactive Streamlit web application.

---

## 📂 Project Structure

```
Project-3-Telco/
│
├── Dataset/
│   └── Telco-Customer-Churn.csv
│
├── Notebook/
│   ├── Data_Preprocessing.ipynb
│   ├── EDA.ipynb
│   ├── Modeling.ipynb
│   └── Evaluation.ipynb
│
├── Model/
│   ├── model.pkl
│   └── scaler.pkl
│
├── app.py
├── requirements.txt
├── README.md
└── images/
```

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Streamlit
- Joblib

---

## 📊 Dataset

The dataset contains customer information from a telecommunications company, including:

- Customer demographics
- Account information
- Contract type
- Internet services
- Payment method
- Monthly charges
- Total charges
- Customer churn status

**Target Variable**

- **Churn**
  - Yes
  - No

---

## 🔄 Machine Learning Workflow

### 1. Business Understanding

- Define churn prediction as a binary classification problem.
- Understand business impacts of customer retention.

### 2. Data Understanding

- Explore dataset structure.
- Analyze feature distributions.
- Identify missing values.
- Detect duplicate records.

### 3. Data Preparation

- Handle missing values.
- Encode categorical variables.
- Feature scaling.
- Feature selection.
- Train-test split.

### 4. Modeling

The project evaluates several classification algorithms, such as:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)

The best-performing model is selected based on evaluation metrics.

---

## 📈 Model Evaluation

Performance is evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Confusion Matrix

---

## 📊 Exploratory Data Analysis

The analysis includes:

- Customer demographics
- Contract distribution
- Internet service usage
- Payment methods
- Monthly charges
- Total charges
- Churn distribution
- Correlation analysis

---

## 🚀 Streamlit Application

The deployed application allows users to:

- Input customer information.
- Predict churn probability.
- Display prediction results.
- Show customer risk classification.

Run locally:

```bash
pip install -r requirements.txt

streamlit run app.py
```

---

## 📷 Application Preview

Add your application screenshot here.

```markdown
![Dashboard](images/dashboard.png)
```

---

## 📚 Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Data Visualization
- Machine Learning Classification
- Model Evaluation
- Streamlit Deployment

---

## 📬 Author

**Dzulfi Khoiriyah Azzahra**

- GitHub: https://github.com/dzulfi02

---

## 📄 License

This project is developed for educational and portfolio purposes.
