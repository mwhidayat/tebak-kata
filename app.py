import streamlit as st
import random
import datetime
import urllib

# Read words from a txt file
def read_word_list():
    file_path = "id-word-list.txt"
    with open(file_path, "r") as file:
        word_list = file.read().splitlines()
    return word_list

def generate_letters():
    # Generate a list of random letters with specific conditions
    vowels = ["a", "e", "i", "o", "u"]
    num_vowels = 2
    num_consonants = 7 - num_vowels

    # Get the current date (without time) to use as the seed
    today = datetime.date.today()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)

    # Add vowels
    letters = random.sample(vowels, num_vowels)

    # Add consonants
    consonants = [c for c in "bcdfghjklmnpqrstvwxyz" if c not in letters]
    letters += random.sample(consonants, num_consonants)

    # Reset the seed so that other random operations are not affected
    random.seed(None)

    return letters

def get_valid_words(letters, word_list):
    # Find all valid words that can be constructed from the given letters
    valid_words = []
    for word in word_list:
        word_letters = list(word)
        if all(letter in letters for letter in word_letters) and word_letters[0] in letters:
            valid_words.append(word)
    return valid_words

def calculate_word_score(word):
    # Calculate score for a single word
    return len(word)

def calculate_total_score(words):
    # Calculate total score for all words
    return sum(calculate_word_score(word) for word in words)

def display_letters(letters, word_list):
    center_letter = letters[0]
    other_letters = letters[1:]

    html = f"""
    <style>
    .bee-hive {{
        text-align: center;
        line-height: 1.6;
    }}

    .hexagon {{
        display: inline-block;
        margin: 10px;
        width: 30px;
        height: 30px;
        border: 1px solid #000;
        line-height: 30px;
        font-size: 20px;
        background-color: #FFAE42;
        color: #000;
    }}

    .hexagon.center {{
        background-color: #FFAE42;
    }}
    </style>

    <div class="bee-hive">
        <div></div>
        <div class="hexagon">{other_letters[0]}</div>
        <div class="hexagon">{other_letters[1]}</div>
        <div></div>
        <div class="hexagon">{other_letters[2]}</div>
        <div class="hexagon center">{center_letter}</div>
        <div class="hexagon">{other_letters[3]}</div>
        <div></div>
        <div class="hexagon">{other_letters[4]}</div>
        <div class="hexagon">{other_letters[5]}</div>
        <div></div>
    </div>
    """

    valid_words = get_valid_words(letters, word_list)
    num_valid_words = len(valid_words)

    st.markdown(html, unsafe_allow_html=True)

    st.markdown("---")

    st.info(f"Jumlah kata untuk ditebak: {num_valid_words} kata")

# Streamlit app
def main():
    st.title("Tebak kata")

    word_list = read_word_list()

    if "letters" not in st.session_state:
        st.session_state["letters"] = generate_letters()
        st.session_state["timestamp"] = datetime.datetime.now()

    letters = st.session_state["letters"]

    st.markdown("---")

    display_letters(letters, word_list)

    st.write(" ")
    st.write(" ")

    if st.button("Ubah susunan huruf"):
        random.shuffle(letters)
        st.session_state["letters"] = letters

    st.markdown("---")

    user_input = st.text_input("Kata tebakanmu:").lower()
    if user_input:
        guessed_words = st.session_state.get("guessed_words", [])
        score = st.session_state.get("score", 0)

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

            st.info(f"Skor total: {calculate_total_score(guessed_words)}")
            st.session_state["guessed_words"] = guessed_words

        num_correct_guesses = len(guessed_words)
        st.info(f"Jumlah tebakan benar: {num_correct_guesses}")

        st.info(f"Daftar kata telah ditebak: {', '.join(guessed_words)}")

        valid_words = get_valid_words(letters, word_list)
        num_valid_words = len(valid_words)

        information = f"Saya menebak {num_correct_guesses} dari {num_valid_words} kata dengan skor total {score} di aplikasi Tebak kata!"
        twitter_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(information + " di sini: https://mwhidayat-tebak-kata-app-r88f9n.streamlit.app/")
        st.write(f"[Share on Twitter]({twitter_url})")


    st.markdown("---")

    if "give_up_clicked" not in st.session_state:
        st.session_state["give_up_clicked"] = False

    give_up_clicked = st.session_state["give_up_clicked"]

    # Give up button
    if not give_up_clicked:
        if st.button("Menyerah"):
            st.session_state["give_up_clicked"] = True
            give_up_clicked = True
    else:
        valid_words = get_valid_words(letters, word_list)
        st.info(f"Kunci jawaban: {', '.join(valid_words)}")

    # Footer
    with st.container():
        st.markdown("---")
        st.markdown("Initially developed by [MW Hidayat](https://twitter.com/casecrit) to help a first grader learning new words. Inspired by The NYT's Spelling Bee.")

if __name__ == "__main__":
    st.set_page_config(
    page_title="Tebak kata",
    page_icon="💡",
    layout="centered",
    )
    main()
