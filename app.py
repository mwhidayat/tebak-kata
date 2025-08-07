import streamlit as st
import random
import datetime

# ==========================
# Utility Functions
# ==========================

def read_word_list(file_path="id-word-list.txt"):
    with open(file_path, "r") as file:
        return file.read().splitlines()


def generate_letters():
    """Generate 9 unique letters with 3 vowels and 6 consonants."""
    vowels = list("aeiou")
    consonants = [c for c in "bcdfghjklmnpqrstvwxyz"]
    
    today = datetime.date.today()
    random.seed(int(today.strftime("%Y%m%d")))

    selected_vowels = random.sample(vowels, 3)
    selected_consonants = random.sample([c for c in consonants if c not in selected_vowels], 6)
    
    letters = selected_vowels + selected_consonants
    random.shuffle(letters)

    center_letter = random.choice(letters)
    letters.remove(center_letter)
    letters.insert(0, center_letter)  # Center letter always at index 0

    random.seed(None)
    return letters


def get_valid_words(letters, word_list):
    """Return valid words using the given letters and containing the center letter."""
    center_letter = letters[0]
    return [
        word for word in word_list
        if center_letter in word and all(char in letters for char in word)
    ]


def calculate_word_score(word):
    return len(word)


# ==========================
# UI Functions
# ==========================

def render_letter_grid(letters):
    center = letters[0]
    outer = letters[1:]

    html_grid = """
    <style>
        .bee-container {
            display: flex; justify-content: center; margin: 20px 0;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 40px);
            grid-template-rows: repeat(3, 40px);
            gap: 10px;
        }
        .grid-letter {
            width: 40px; height: 40px;
            background: #ffcc00;
            border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            font-size: 18px; font-weight: bold;
            color: black;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .center-letter {
            background: #00cc66 !important;
        }
    </style>
    <div class="bee-container">
        <div class="grid">
    """

    for i in range(9):
        if i == 4:
            html_grid += f'<div class="grid-letter center-letter">{center}</div>'
        else:
            outer_index = i if i < 4 else i - 1  # Skip index 4
            html_grid += f'<div class="grid-letter">{outer[outer_index]}</div>'

    html_grid += """
        </div>
    </div>
    """

    st.markdown(html_grid, unsafe_allow_html=True)


# ==========================
# Main App
# ==========================

def main():
    st.set_page_config(page_title="Tebak Kata", page_icon="🔡", layout="centered")
    st.title("🔡 Tebak Kata")

    word_list = read_word_list()

    # -- Session Initialization --
    if "letters" not in st.session_state:
        st.session_state.letters = generate_letters()
        st.session_state.guessed_words = []
        st.session_state.score = 0
        st.session_state.give_up = False

    letters = st.session_state.letters
    guessed_words = st.session_state.guessed_words
    score = st.session_state.score

    # -- Letter Grid --
    render_letter_grid(letters)

    # -- Shuffle Button --
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Pusing? Ubah susunan huruf"):
            center_letter = letters[0]
            outer_letters = letters[1:]
            random.shuffle(outer_letters)
            st.session_state.letters = [center_letter] + outer_letters
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Valid Words Info --
    valid_words = get_valid_words(letters, word_list)
    st.info(f"Ada {len(valid_words)} kata yang bisa kamu tebak. Huruf berwarna hijau wajib digunakan.")

    # -- User Guess Input --
    user_input = st.text_input("Kata tebakanmu:", key="guess_input").lower().strip()

    if st.button("✅ Periksa"):
        if not user_input:
            st.warning("Masukkan sebuah kata.")
        elif user_input in guessed_words:
            st.warning("Kata sudah ditebak.")
        elif user_input in valid_words:
            st.success("Benar!")
            guessed_words.append(user_input)
            st.session_state.score += calculate_word_score(user_input)
        else:
            st.error("Salah tebak.")

    # -- Score and Guesses --
    col1, col2 = st.columns(2)
    with col1:
        last_score = calculate_word_score(user_input) if user_input in valid_words else 0
        st.metric("📝 Skor Kata", last_score)
        st.metric("📈 Skor Total", st.session_state.score)

    with col2:
        st.metric("✅ Kata Benar", len(guessed_words))
        if guessed_words:
            st.write("**🧠 Tebakan:** " + ", ".join(guessed_words))

    # -- Give Up Option --
    if not st.session_state.give_up:
        if st.button("😓 Nyerah"):
            st.session_state.give_up = True
            st.rerun()
    else:
        kbbi_links = [f"[{word}](https://kbbi.web.id/{word})" for word in valid_words]
        st.info("Jawaban lengkap: " + ", ".join(kbbi_links))

    # -- Footer --
    st.markdown("---")
    st.markdown("Dikembangkan oleh MW Hidayat · Terinspirasi oleh *Spelling Bee*.")


if __name__ == "__main__":

    main()
