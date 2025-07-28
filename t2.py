

# Local spelling correction using pyspellchecker
from spellchecker import SpellChecker

def correct_spelling_local(text):
    spell = SpellChecker()
    words = text.split()
    corrected = []
    for word in words:
        suggestion = spell.correction(word)
        if suggestion is not None and suggestion != word:
            corrected.append(suggestion)
    return corrected

if __name__ == "__main__":
    user_input = input("Enter text to check spelling: ")
    corrected_words = correct_spelling_local(user_input)
    if corrected_words:
        print(f"corrected words: {', '.join(corrected_words)}")
