import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from spellchecker import SpellChecker

# Function to call OCR.Space API and extract text
def extract_text_from_image(image):
    api_key = 'K84350751588957'  # Replace with your key if you have one

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={'filename': img_bytes},
        data={'apikey': api_key, 'language': 'eng'}
    )

    result = response.json()
    if result['IsErroredOnProcessing']:
        st.error("OCR API Error: " + result.get('ErrorMessage', ['Unknown error'])[0])
        return "", []

    parsed_text = result['ParsedResults'][0]['ParsedText']
    words = parsed_text.split()
    return parsed_text, [(w, None) for w in words]

# Spell correction function remains unchanged
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

# Streamlit app logic
def main():
    st.title('Image Text Error Detection (OCR via API)')

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        extracted_text, word_confidences = extract_text_from_image(image)

        words_list = [w for w in extracted_text.split() if w.strip()]
        st.subheader("Extracted Words:")
        for idx, word in enumerate(words_list, 1):
            st.write(f"{idx}. {word}")

        if words_list:
            spell = SpellChecker()
            corrected_pairs = []
            for word in words_list:
                suggestion = spell.correction(word)
                if suggestion and suggestion != word:
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
