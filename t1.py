import streamlit as st
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from spellchecker import SpellChecker

# 🔄 Load model and processor only once
@st.cache_resource
def load_model():
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-stage1")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-stage1")
    return processor, model

processor, model = load_model()

# 🧠 TrOCR-based OCR function
def extract_text_from_image(image):
    image = image.convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text.strip(), []  # Empty list for compatibility with previous code

# 🧹 Local spelling correction
def correct_spelling_with_spellchecker(text):
    spell = SpellChecker()
    words = text.split()
    corrected_words = []
    for word in words:
        suggestion = spell.correction(word)
        corrected_words.append(suggestion if suggestion else word)
    return ' '.join(corrected_words)

# 🚀 Streamlit App
def main():
    st.title('Image Text Error Detection (TrOCR-powered)')

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        extracted_text, _ = extract_text_from_image(image)

        words_list = [w for w in extracted_text.split() if w.strip()]
        st.subheader("Extracted Words:")
        for idx, word in enumerate(words_list, 1):
            st.write(f"{idx}. {word}")

        if words_list:
            # Spell check each word and show only changed ones
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
