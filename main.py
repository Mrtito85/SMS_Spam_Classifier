import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from nltk.data import find

# Safe download checker
def download_nltk_resources():
    try:
        find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Explicitly download NLTK resources on startup
download_nltk_resources()

ps = PorterStemmer()

# Load vectorizer and model
tfidf = pickle.load(open("Vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

# 💖 Animated Background: Always running on loop without fading
st.markdown(
    """
    <style>
    body {
        background-color: #fff0f5;
    }
    .background {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: -1;
        overflow: hidden;
    }

    .floating-text {
        position: absolute;
        color: #ff69b4;
        font-size: 50px;
        font-weight: bold;
        white-space: nowrap;
        animation: floatAnim 100s linear infinite;
    }

    @keyframes floatAnim {
        0% {
            transform: translateX(100vw) translateY(0);
        }
        100% {
            transform: translateX(-100vw) translateY(0);
        }
    }

    .app-name {
        font-size: 50px;
        color: #ff1493;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }

    </style>

    <div class="background">
        <div class="floating-text" style="top:20%; left:10%;">❤️ Bisma ❤️</div>
        <div class="floating-text" style="top:30%; left:30%; animation-delay: 2s;">❤️ Bisma ❤️</div>
        <div class="floating-text" style="top:40%; left:50%; animation-delay: 4s;">❤️ Bisma ❤️</div>
        <div class="floating-text" style="top:50%; left:70%; animation-delay: 6s;">❤️ Bisma ❤️</div>
        <div class="floating-text" style="top:60%; left:90%; animation-delay: 8s;">❤️ Bisma ❤️</div>
        <div class="floating-text" style="top:70%; left:15%; animation-delay: 10s;">❤️ Bisma ❤️</div>
    </div>

    <div class="app-name">BismaInbox</div>
    """,
    unsafe_allow_html=True
)

# App title
st.title("📩 Email/SMS Spam Classifier")

# Input box
input_sms = st.text_input("Enter the Message")

# Preprocessing function
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Predict button
if st.button("Predict"):
    transformed_sms = transform_text(input_sms)
    vector_input = tfidf.transform([transformed_sms])
    result = model.predict(vector_input)[0]

    if result == 1:
        st.header("🚨 Spam!")
    else:
        st.header("✅ Not Spam")
