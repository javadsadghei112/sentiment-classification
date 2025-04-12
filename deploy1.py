import streamlit as st
import joblib
from googletrans import Translator
from langdetect import detect, LangDetectException

# Load the model
@st.cache_resource
def load_model():
    return joblib.load("model (1).pkl")

model = load_model()

# Initialize the translator
translator = Translator()

# Mapping model output to labels
label_map = {
    0: "Bad Sentiment",
    1: "Good Sentiment",
    2: "Withdraw"
}

# Streamlit UI
st.title("🧠 NLP Text Classification")
st.markdown("Created by: Javad sadghei")
st.write("Enter text (in English or Farsi), and the model will predict its sentiment.")

# Text input
text_input = st.text_area("Enter your text here:")

if st.button("Classify"):
    if text_input.strip() == "":
        st.warning("Please enter some text first.")
    else:
        try:
            # Detect the language
            lang = detect(text_input)

            if lang == 'en':
                # Text is already English
                prediction = model.predict([text_input])[0]
                label = label_map.get(prediction, "Unknown")
                st.success(f"Predicted class: **{label}**")

            elif lang == 'fa':
                # Translate Farsi to English
                translated = translator.translate(text_input, dest='en')
                english_text = translated.text
                st.info(f"Translated to English: _{english_text}_")

                prediction = model.predict([english_text])[0]
                label = label_map.get(prediction, "Unknown")
                st.success(f"Predicted class: **{label}**")

            else:
                st.error("Unknown or unsupported language detected.")

        except LangDetectException:
            st.error("Language detection failed. Please try different text.")
        except Exception as e:
            st.error(f"Translation or prediction failed: {e}")
