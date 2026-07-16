# 📊 YouTube Sentiment Analysis Using IndoBERT and Machine Learning

## 📌 Project Overview

This project aims to analyze public sentiment toward the **Free Nutritious Meal Program (Makan Bergizi Gratis - MBG)** based on comments collected from YouTube videos.

Sentiment labels were automatically generated using the **IndoBERT** model, and several Machine Learning algorithms were evaluated to classify the sentiment of user comments. The best-performing model was then deployed as an interactive web application using **Streamlit**.

🌐 **Live Demo:** https://dmvjgtewsynivpksyymkri.streamlit.app/

---

## 🎯 Objectives

- Collect comments from YouTube videos discussing the Free Nutritious Meal (MBG) Program.
- Perform text preprocessing on the collected comments.
- Generate sentiment labels using the IndoBERT model.
- Conduct exploratory data analysis (EDA) on the labeled dataset.
- Build and evaluate sentiment classification models using Machine Learning.
- Deploy the best-performing model as a Streamlit web application.

---

## 📂 Dataset

The dataset was collected from YouTube comments using the following library:

- `youtube-comment-downloader`

The dataset contains approximately **6,000 YouTube comments**.

---

## 🔄 Project Workflow

```text
YouTube Comment Scraping
          │
          ▼
Data Understanding (EDA)
          │
          ▼
Text Preprocessing
          │
          ▼
Sentiment Labeling (IndoBERT)
          │
          ▼
Exploratory Data Analysis (EDA)
          │
          ▼
Feature Engineering (TF-IDF)
          │
          ▼
Machine Learning Models
          │
      ├── Naive Bayes
      └── Logistic Regression
          │
          ▼
Model Evaluation
          │
          ▼
Streamlit Deployment
```

---

## 🧹 Text Preprocessing

The preprocessing pipeline includes:

- Case Folding
- Text Cleaning
- URL Removal
- Mention Removal
- Hashtag Removal
- Emoji Removal
- Number Removal
- Punctuation Removal
- Tokenization
- Slang Word Normalization
- Stopword Removal
- Indonesian Stemming using **Sastrawi**

---

## 🤖 Sentiment Labeling

Sentiment labels were generated using the **IndoBERT** model, resulting in three sentiment categories:

- 😊 Positive
- 😐 Neutral
- 😠 Negative

---

## ⚙️ Feature Engineering

Text data was transformed into numerical features using:

- **TF-IDF Vectorizer**

---

## 🧠 Machine Learning Models

The following classification algorithms were evaluated:

- Multinomial Naive Bayes
- Logistic Regression

---

## 📈 Model Evaluation

The models were evaluated using the following metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

### Evaluation Results

| Model | Accuracy |
|--------|---------:|
| **Logistic Regression** | **0.69** |
| Naive Bayes | 0.66 |

Based on the evaluation results, **Logistic Regression** achieved the highest accuracy and was selected as the final model for deployment.

---

## 🛠️ Technologies Used

- Python
- Google Colab
- Pandas
- NumPy
- Scikit-learn
- Transformers
- IndoBERT
- Sastrawi
- Matplotlib
- WordCloud
- Streamlit

---

## 📁 Project Structure

```text
Mentoring/
│
├── Dataset/
│   └── youtube_comment.csv
│
├── Model/
│   ├── logistic_regression.pkl
│   └── tfidf.pkl
│
├── Notebook/
│   └── Project_Sentiment_Mentoring.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/dzulfi02/BLKPP-Data-Analis.git
```

### Navigate to the project directory

```bash
cd BLKPP-Data-Analis/Mentoring
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

## 📱 Application Features

The Streamlit application provides several interactive features:

- View dataset summary
- Display sentiment distribution
- Explore word clouds for each sentiment class
- Predict the sentiment of custom Indonesian text
- Compare machine learning model performance
- Visualize evaluation metrics

---

## 👨‍💻 Dzulfi Khoiriyah Azzahra

**Dzulfi Khoiriyah Azzahra**

- GitHub: https://github.com/dzulfi02
