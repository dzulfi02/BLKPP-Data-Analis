# 📊 Store Sales Prediction Dashboard

Web application for predicting retail store sales using a Machine Learning Regression model, built with **Streamlit** and supported by business insights from exploratory data analysis.

🔗 **Live Demo:** [https://sales-prediction-app-fzbunyz5s82j2qem7wb6rr.streamlit.app/]

---

## 📌 About the Project

This project aims to predict daily store sales and identify key business factors that influence sales performance.

The analysis focuses on promotional activities, customer traffic, holiday periods, seasonal trends, and store characteristics to support data-driven decision-making.

### Model Performance

| Metric   | Value   |
| -------- | ------- |
| R² Score | 0.89    |
| MAE      | 850.12  |
| RMSE     | 1325.45 |
| MAPE     | 15.8%   |

> Replace the metrics above with your actual model evaluation results.

---

## 🎯 Business Objective

The company experiences fluctuations in sales performance throughout the year. This project helps answer several business questions:

* What factors most influence store sales?
* How much impact do promotions have on revenue?
* Which periods generate the highest sales?
* How can future sales be estimated more accurately?

---

## 📂 Dataset

The dataset contains historical sales records and store-related information, including:

| Feature             | Description                    |
| ------------------- | ------------------------------ |
| Store               | Store ID                       |
| Sales               | Daily sales value              |
| Customers           | Number of customers            |
| Promo               | Promotion status               |
| StateHoliday        | Public holiday indicator       |
| SchoolHoliday       | School holiday indicator       |
| CompetitionDistance | Distance to nearest competitor |
| Date                | Transaction date               |

---

## 📈 Key Insights

### Promotion Impact

Stores running promotional campaigns consistently generated higher sales compared to non-promotional periods.

### Payday Effect

Sales tended to increase during payday periods, indicating stronger purchasing activity from customers.

### Seasonal Trends

Holiday seasons and special events contributed significantly to sales growth.

### Customer Influence

Customer volume showed a strong positive correlation with sales performance.

---

## 🗂️ Project Structure

sales-regresi-app/
├── app.py              # Streamlit App
├── model_xgb.pkl        # Model XGBoost (joblib)
├── requirements.txt     # Dependency List
└── README.md
```

---

## ⚙️ Application Features

| Feature               | Description                 |
| --------------------- | --------------------------- |
| Sales Prediction      | Predict future store sales  |
| Interactive Dashboard | Visualize sales performance |
| Business Insights     | Display key findings        |
| Performance Metrics   | Evaluate model accuracy     |

---

## 🚀 Run Locally

```bash
# Clone repository
git clone https://github.com/yourusername/BLKPP-Data-Analis.git

# Move into project folder
cd BLKPP-Data-Analis

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🌐 Deployment

The application is deployed using Streamlit Community Cloud.

Each update pushed to the main branch automatically triggers a redeployment.

---

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost / Linear Regression
* SQL
* Streamlit
* Power BI
* Plotly
* Matplotlib
* Seaborn

---

## 💡 Business Recommendations

* Optimize promotional strategies during high-performing periods.
* Improve inventory planning using sales forecasts.
* Focus marketing campaigns around payday periods and seasonal events.
* Monitor underperforming stores and replicate successful strategies from top-performing stores.

---

## 👨‍💻 Author

**Dzulfi**

LinkedIn: [https://linkedin.com/in/your-linkedin](https://www.linkedin.com/in/dzulfi-khoiriyah-azzahra-269934417/)

GitHub: https://github.com/dzulfi02
