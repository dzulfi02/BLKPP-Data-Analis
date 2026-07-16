# 🛒 Retail Sales Prediction using XGBoost

## 📖 Project Overview

This project aims to predict retail store sales using Machine Learning. Historical store information, promotional activities, holidays, and customer-related features are utilized to build a regression model capable of estimating daily sales.

The project follows an end-to-end data science workflow, including data preprocessing, exploratory data analysis (EDA), feature engineering, model development, evaluation, and deployment using Streamlit. The chosen model is **XGBoost Regressor**, which demonstrated the best predictive performance among the evaluated algorithms.

---

## 🎯 Objectives

- Analyze historical retail sales data.
- Identify factors affecting daily sales.
- Build a regression model for sales prediction.
- Evaluate model performance using regression metrics.
- Deploy the trained model into an interactive Streamlit web application.

---

## 📂 Project Structure

```
Project-1-Retail/
│
├── Dataset/
│   ├── train.csv
│   ├── test.csv
│   └── store.csv
│
├── Notebook/
│   └── Retail_Sales_Prediction.ipynb
│
├── Model-Regresi-XGb/
│   └── model_xgb.pkl
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
- Plotly
- Scikit-Learn
- XGBoost
- Joblib
- Streamlit

---

## 📊 Machine Learning Workflow

### 1. Business Understanding

- Understand the retail sales forecasting problem.
- Define prediction target (Sales).

### 2. Data Understanding

- Explore dataset structure.
- Analyze feature distributions.
- Check missing values.
- Identify outliers.

### 3. Data Preparation

- Handle missing values.
- Feature engineering.
- Date transformation.
- One-hot encoding.
- Feature selection.

### 4. Modeling

Several regression models were evaluated, including:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting
- XGBoost Regressor

The best-performing model was selected based on evaluation metrics.

---

## 📈 Model Performance

| Metric | Value |
|---------|-------|
| R² Score | **0.80** |
| MAPE | **21%** |
| RMSE | **1717.23** |

---

## 🚀 Streamlit Application

The web application allows users to:

- Input store information.
- Select promotional conditions.
- Configure holiday information.
- Predict estimated daily sales.
- Display prediction results interactively.

Run locally:

```bash
pip install -r requirements.txt

streamlit run app.py
```

---

## 📷 Dashboard Preview

Add your Streamlit screenshot here.

```
images/dashboard.png
```

Example:

```markdown
![Dashboard](images/dashboard.png)
```

---

## 📌 Features Used

- Store
- DayOfWeek
- Promo
- SchoolHoliday
- Month
- Day of Month
- Week of Year
- Is Weekend
- Payday Period
- Average Customer per Store
- State Holiday (One-Hot Encoding)

---

## 📁 Model

The trained model is stored as:

```
Model-Regresi-XGb/model_xgb.pkl
```

The model is loaded using Joblib inside the Streamlit application.

---

## 📬 Author

**Dzulfi Khoiriyah Azzahra**

- GitHub: https://github.com/dzulfi02

---

## ⭐ Future Improvements

- Hyperparameter tuning.
- Feature importance visualization.
- Forecast visualization.
- Batch prediction using CSV upload.
- Cloud deployment.

---

## 📄 License

This project is developed for educational and portfolio purposes.
