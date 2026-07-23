# 🪪 AI KTP OCR - Document Recognition System

## 📌 Overview

AI KTP OCR is an AI-based document processing application designed to automatically identify Indonesian Identity Cards (KTP), extract information using OCR (Optical Character Recognition), validate extracted data, store results into a database, and export processed data into CSV format.

This application uses **AI Vision technology** to perform document classification and information extraction from KTP images.

Link Demo : [https://hd5wggxufgmwqhmntjsiv7.streamlit.app/]
---

# 🎯 Project Objectives

The objectives of this project are:

- Automatically classify uploaded documents whether they are Indonesian KTP documents or not.
- Extract important information from KTP images using AI Vision OCR.
- Validate extracted information to ensure data completeness.
- Store OCR results into a database.
- Provide CSV export functionality for further processing.

---

# ✨ Features

## 1. Image Upload

Users can upload KTP images in:

- JPG
- JPEG
- PNG

The uploaded image will be displayed as a preview before processing.

---

## 2. AI Document Classification

The system uses AI Vision to classify uploaded images.

Output:

```
✅ KTP Indonesia

or

❌ Not a KTP Document
```

---

## 3. AI Vision OCR Extraction

After successful classification, the system extracts KTP information including:

- NIK
- Name
- Place and Date of Birth
- Gender
- Blood Type
- Address
- RT/RW
- Village
- District
- Religion
- Marital Status
- Occupation
- Citizenship
- Validity Period

---

## 4. OCR Data Validation

The extracted data is validated based on:

- NIK availability
- NIK digit length
- Name availability
- Address availability

Example:

```
✅ NIK valid
✅ Name detected
✅ Address detected
```

---

## 5. Database Storage

Processed KTP data is automatically stored using:

```
SQLite Database
```

Stored information includes:

- NIK
- Name
- Birth information
- Gender
- Address
- Religion
- Occupation
- Processing timestamp

---

## 6. CSV Export

Users can download extracted KTP information into CSV format for further analysis or reporting.

---

# 🏗️ System Workflow

```
User Upload Image

        |
        v

AI Vision Classification

        |
        |
        +----------------+
        |                |
        v                v

     KTP              Not KTP

        |
        v

AI Vision OCR Extraction

        |
        v

Data Validation

        |
        v

SQLite Database Storage

        |
        v

CSV Export
```

---

# 🛠️ Technology Stack

## Programming Language

- Python

## Framework

- Streamlit

## AI Model

- OpenAI Vision Model through OpenRouter API

## Database

- SQLite

## Libraries

- Streamlit
- OpenAI SDK
- Pillow
- Pandas
- Python-dotenv

---

# 📂 Project Structure

```
AI-KTP-Project/

│
├── app.py
│
├── requirements.txt
│
├── .env
│
├── ktp_database.db
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/dzulfi02/BLKPP-Data-Analis.git
```

Go to project folder:

```bash
cd BLKPP-Data-Analis/AI-KTP-Project
```

---

## 2. Install Dependencies

Create virtual environment (optional):

```bash
python -m venv env
```

Activate environment:

Windows:

```bash
env\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

## 3. Setup API Key

Create a file:

```
.env
```

Add OpenRouter API Key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## 4. Run Application

Run Streamlit:

```bash
streamlit run app.py
```

Application will run on:

```
http://localhost:8501
```

---

# 📊 Application Output

The application provides:

### Classification Result

```
Document Type:
KTP Indonesia
```

### OCR Result

Example:

| Field | Value |
|---|---|
| NIK | Extracted NIK |
| Name | Extracted Name |
| Address | Extracted Address |

### Validation Result

```
✅ Data Valid
```

### Export

```
Download CSV
```

---

# 🔒 Security Note

The `.env` file contains sensitive API credentials and should not be uploaded to public repositories.

Add:

```
.env
ktp_database.db
```

to `.gitignore`.

---

# 🚀 Future Improvements

Possible future improvements:

- Add user authentication
- Add cloud database integration
- Improve OCR accuracy using image preprocessing
- Add dashboard analytics
- Deploy application using Streamlit Cloud

---

# 👤 Author

**Dzulfi Khoiriyah Azzahra**
