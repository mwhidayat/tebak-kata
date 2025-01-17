import streamlit as st
import random
import datetime

# Function to read words from a txt file
def read_word_list():
    file_path = "id-word-list.txt"
    with open(file_path, "r") as file:
        word_list = file.read().splitlines()
    return word_list

# Function to generate a random set of 9 letters
def generate_letters():
    vowels = ["a", "e", "i", "o", "u"]
    num_vowels = 3
    num_consonants = 9 - num_vowels

    today = datetime.date.today()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)

    letters = random.sample(vowels, num_vowels)
    consonants = [c for c in "bcdfghjklmnpqrstvwxyz" if c not in letters]
    letters += random.sample(consonants, num_consonants)

    random.shuffle(letters)  # Shuffle the letters for randomness
    random.seed(None)
    return letters

# Function to get valid words from the word list that can be made with the given letters
def get_valid_words(letters, word_list):
    valid_words = []
    for word in word_list:
        word_letters = list(word)
        if all(word_letters.count(letter) <= letters.count(letter) for letter in word_letters) and word_letters[0] in letters:
            valid_words.append(word)
    return valid_words

# Function to score a word based on its length
def calculate_word_score(word):
    return len(word)

# Function to calculate total score of guessed words
def calculate_total_score(words):
    return sum(calculate_word_score(word) for word in words)

# Function to display the letters in a 3x3 grid
def display_letters(letters):
    st.markdown("### Susunan Huruf")
    rows = [letters[i:i+3] for i in range(0, len(letters), 3)]

    for row in rows:
        cols = st.columns(3)
        for idx, letter in enumerate(row):
            with cols[idx]:
                if st.button(letter.upper(), key=letter):
                    st.session_state["user_input"] += letter

    st.markdown("---")

# Main function to run the application
def main():
    st.title("Tebak Kata")

    word_list = read_word_list()

    if "letters" not in st.session_state:
        st.session_state["letters"] = generate_letters()

    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""

    if "guessed_words" not in st.session_state:
        st.session_state["guessed_words"] = []

    if "score" not in st.session_state:
        st.session_state["score"] = 0

    letters = st.session_state["letters"]

    display_letters(letters)

    user_input = st.text_input("Kata tebakanmu:", st.session_state["user_input"]).lower()

    if st.button("Kirim"):
        if user_input:
            guessed_words = st.session_state["guessed_words"]
            score = st.session_state["score"]

            if user_input in guessed_words:
                st.warning("Kata telah ditebak. Coba kata lain.")
            else:
                valid_words = get_valid_words(letters, word_list)

                if user_input in valid_words:
                    st.success("Betul!")
                    guessed_words.append(user_input)

                    word_score = calculate_word_score(user_input)
                    score += word_score
                    st.session_state["score"] = score
                    st.info(f"Skor kata: {word_score}")
                else:
                    st.error("Ups, salah!")

                st.session_state["guessed_words"] = guessed_words

        st.session_state["user_input"] = ""  # Clear input field

    st.markdown("---")

    guessed_words = st.session_state["guessed_words"]
    score = st.session_state["score"]

    # Create two columns for displaying information
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Skor total: {score}")
        st.info(f"Jumlah tebakan benar: {len(guessed_words)}")

    with col2:
        st.info(f"Daftar kata telah ditebak: {', '.join(guessed_words)}")
        valid_words = get_valid_words(letters, word_list)
        num_valid_words = len(valid_words)
        st.info(f"Jumlah kata untuk ditebak: {num_valid_words} kata")

    if st.button("Menyerah"):
        st.info(f"Kunci jawaban: {', '.join(valid_words)}")

    with st.container():
        st.markdown("---")
        st.markdown("Initially developed by [MW Hidayat](https://github.com/mwhidayat/) to help a first grader acquire new words.")
        st.markdown("Inspired by The NYT's Spelling Bee.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Tebak Kata",
        page_icon="💡",
        layout="centered",
    )
    main()
