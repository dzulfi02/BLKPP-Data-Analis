import streamlit as st
import joblib

# Load model
model = joblib.load("model/logistic_regression.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="💬"
)

st.title("💬 Sentiment Analysis YouTube Comments")

st.write("Masukkan komentar yang ingin dianalisis.")

text = st.text_area("Komentar")

if st.button("Prediksi"):

    if text.strip() == "":
        st.warning("Masukkan komentar terlebih dahulu.")
    else:

        vector = vectorizer.transform([text])

        prediction = model.predict(vector)[0]

        confidence = model.predict_proba(vector).max()*100

        if prediction == "Positive":
            st.success(f"😊 Sentimen : {prediction}")

        elif prediction == "Negative":
            st.error(f"😠 Sentimen : {prediction}")

        else:
            st.info(f"😐 Sentimen : {prediction}")

        st.write(f"Confidence Score : **{confidence:.2f}%**")