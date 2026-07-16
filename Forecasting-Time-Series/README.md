# 🐔 National Chicken Meat Price Forecasting Using Time Series Analysis

This project aims to forecast **national chicken meat prices in Indonesia** using **Time Series Forecasting** techniques. Several forecasting models were evaluated and compared to identify the best-performing model based on **MAE**, **RMSE**, and **MAPE** evaluation metrics. The selected model was then deployed as an interactive web application using **Streamlit**.

🌐 **Live Demo:** https://4je82smkdfyydznwsgftdg.streamlit.app/

---

## 📌 Background

Chicken meat is one of Indonesia's most important food commodities, and its price frequently fluctuates due to various factors such as market demand, seasonal trends, distribution, and economic conditions. Accurate price forecasting can help businesses, policymakers, and consumers make better planning and informed decisions.

---

## 🎯 Objectives

- Analyze historical national chicken meat price data.
- Compare multiple time series forecasting models.
- Select the best-performing model based on evaluation metrics.
- Develop an interactive forecasting application using Streamlit.

---

## 📂 Dataset

- **Dataset:** National Chicken Meat Prices
- **Source:** National Strategic Food Price Information Center (PIHPS)
- **Period:** July 2022 – July 2026

The dataset contains daily chicken meat prices used as historical data for the forecasting process.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Statsmodels
- Prophet
- Scikit-learn
- Matplotlib
- Plotly
- Streamlit

---

## 📈 Forecasting Models

The following forecasting models were evaluated and compared:

- ARIMA
- SARIMA
- Holt-Winters Exponential Smoothing
- Prophet

---

## 📊 Model Evaluation

| Model | MAE | RMSE | MAPE (%) |
|--------|-------:|-------:|-------:|
| ARIMA | 2409.26 | 3044.95 | 5.86 |
| SARIMA | 2409.26 | 3044.95 | 5.86 |
| Prophet | 1666.01 | 1993.54 | 4.26 |
| **Holt-Winters** | **1589.87** | **1851.21** | **3.97** |

### 🏆 Best Model

Among the evaluated models, **Holt-Winters Exponential Smoothing** achieved the best performance, producing the lowest **MAE**, **RMSE**, and **MAPE** values. Therefore, it was selected as the final forecasting model for deployment.

---

## 📷 Streamlit Dashboard

The application provides several interactive features, including:

- Dataset overview
- Best model summary
- Historical price visualization
- Forecast visualization
- Forecast horizon selection (7, 14, and 30 days)
- Model performance comparison
- CSV download for forecasting results

---

## 📁 Project Structure

```text
Forecasting-Time-Series/
│
├── app.py
├── requirements.txt
├── README.md
├── Notebook/
└── Dataset/
    └── harga_ayam.csv
```

---

## ▶️ Getting Started

### Clone the repository

```bash
git clone https://github.com/dzulfi02/BLKPP-Data-Analis.git
```

### Navigate to the project directory

```bash
cd BLKPP-Data-Analis/Forecasting-Time-Series
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit application

```bash
streamlit run app.py
```

---

## 📌 Forecast Output

Users can select one of the available forecasting horizons:

- 7 Days
- 14 Days
- 30 Days

The application displays:

- Historical price chart
- Forecast chart
- Predicted values
- Forecast results table

---

## 📚 Evaluation Metrics

The forecasting models were evaluated using the following metrics:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**
- **MAPE (Mean Absolute Percentage Error)**

Lower values indicate better forecasting performance.

---

## 👤 Dzulfi Khoiriyah Azzahra

**Dzulfi Khoiriyah Azzahra**

- GitHub: https://github.com/dzulfi02
