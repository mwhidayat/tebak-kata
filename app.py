import streamlit as st
import random
import datetime


st.set_page_config(
    page_title="Tebak Kata",
    page_icon="💡",
    layout="centered",
)

# CSS to force responsive grid on mobile
st.markdown("""<style>
                [data-testid="column"] {
                    width: calc(50% - 1rem) !important;
                    flex: 1 1 calc(50% - 1rem) !important;
                    min-width: calc(50% - 1rem) !important;
                }
                </style>""", unsafe_allow_html=True)


def read_word_list():
    """Function to read words from a txt file."""
    file_path = "id-word-list.txt"
    with open(file_path, "r") as file:
        return file.read().splitlines()


def generate_letters():
    """Function to generate a random set of 6 letters."""
    vowels = ["a", "e", "i", "o", "u"]
    num_vowels = 2
    num_consonants = 6 - num_vowels
    
    today = datetime.date.today()
    random.seed(int(today.strftime("%Y%m%d")))

    letters = random.sample(vowels, num_vowels)
    consonants = [c for c in "bcdfghjklmnpqrstvwxyz" if c not in letters]
    letters += random.sample(consonants, num_consonants)
    
    random.shuffle(letters)
    random.seed(None)
    return letters


def get_valid_words(letters, word_list):
    """Function to get valid words from the word list that can be made with the given letters."""
    return [
        word for word in word_list 
        if all(word.count(letter) <= letters.count(letter) for letter in word) and word[0] in letters
    ]


def calculate_word_score(word):
    """Function to score a word based on its length."""
    return len(word)


def calculate_total_score(words):
    """Function to calculate total score of guessed words."""
    return sum(calculate_word_score(word) for word in words)


def display_letters(letters):
    """Function to display the letters in a 2x3 grid."""
    with st.expander("Daftar huruf hari ini", expanded=True):
        rows = [letters[i:i + 2] for i in range(0, len(letters), 2)][:3]
        
        for row in rows:
            cols = st.columns([5, 1])
            for idx, letter in enumerate(row):
                with cols[idx]:
                    if st.button(letter.upper(), key=letter):
                        # Append the letter to the user input
                        st.session_state["user_input"] += letter


def main():
    """Main function to run the application."""
    st.title("Tebak Kata")
    
    word_list = read_word_list()

    st.session_state.setdefault("letters", generate_letters())
    st.session_state.setdefault("user_input", "")
    st.session_state.setdefault("guessed_words", [])
    st.session_state.setdefault("score", 0)

    letters = st.session_state["letters"]
    display_letters(letters)

    with st.expander("Kata tebakanmu:", expanded=True):
        user_input = st.text_input("", st.session_state["user_input"], key="user_input_field")

        if st.button("Kirim"):
            process_user_input(user_input, letters, word_list)

        # Clear input field if desired, otherwise leave it as is
        # st.session_state["user_input"] = ""  

    display_statistics()

    with st.container():
        st.markdown("Initially developed by [MW Hidayat](https://github.com/mwhidayat/) to help a first grader acquire new words.")
        st.markdown("Inspired by The NYT's Spelling Bee.")


def process_user_input(user_input, letters, word_list):
    """Process the user input and update the game state."""
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
                st.session_state["score"] += word_score
                st.info(f"Skor kata: {word_score}")
            else:
                st.error("Ups, salah!")

            st.session_state["guessed_words"] = guessed_words


def display_statistics():
    """Display the game statistics."""
    letters = st.session_state["letters"]
    word_list = read_word_list()
    guessed_words = st.session_state["guessed_words"]
    score = st.session_state["score"]

    with st.expander("Statistik", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.info(f"Skor total: {score}")
            valid_words = get_valid_words(letters, word_list)
            st.info(f"Jumlah kata untuk ditebak: {len(valid_words)} kata")
        
        with col2:
            st.info(f"Daftar kata telah ditebak: {', '.join(guessed_words)}")
            st.info(f"Jumlah tebakan benar: {len(guessed_words)}")

        if st.button("Menyerah"):
            st.info(f"Kunci jawaban: {', '.join(valid_words)}")


if __name__ == "__main__":
    main()
