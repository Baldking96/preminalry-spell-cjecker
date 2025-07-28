import streamlit as st
import pytesseract
from PIL import Image
import requests
import json

# Local spelling correction using pyspellchecker
from spellchecker import SpellChecker

# Function to extract text and confidence from the uploaded image using OCR
def extract_text_from_image(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    text = ''
    word_confidences = []

    for i in range(len(data['text'])):
        word = data['text'][i]
        if word.strip():
            text += word + ' '
            word_confidences.append((word, None))  # Confidence is not used

    return text.strip(), word_confidences

# Function to correct spelling using Gemini API
def correct_spelling_with_gemini(text):
    spell = SpellChecker()
    words = text.split()
    corrected_words = []
    for word in words:
        suggestion = spell.correction(word)
        if suggestion is not None:
            corrected_words.append(suggestion)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)


# Streamlit App
def main():
    st.title('Image Text Error Detection')

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        extracted_text, word_confidences = extract_text_from_image(image)

        # Show extracted words as a list
        words_list = [w for w in extracted_text.split() if w.strip()]
        st.subheader("Extracted Words:")
        for idx, word in enumerate(words_list, 1):
            st.write(f"{idx}. {word}")

        if words_list:
            # Spell check each word and show only changed words
            spell = SpellChecker()
            corrected_pairs = []
            for word in words_list:
                suggestion = spell.correction(word)
                if suggestion is not None and suggestion != word:
                    corrected_pairs.append((word, suggestion))
            if corrected_pairs:
                st.subheader("Corrected Words:")
                for idx, (orig, corr) in enumerate(corrected_pairs, 1):
                    st.write(f"{idx}. {orig} → {corr}")
            else:
                st.subheader("Corrected Words:")
                st.write("No corrections needed.")
        else:
            st.write("No text extracted to correct.")

if __name__ == "__main__":
    main()
