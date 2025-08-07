# 🔡 Tebak Kata

**Tebak Kata** is a daily Indonesian word puzzle game inspired by *The New York Times Spelling Bee*. Your goal is to find as many valid Indonesian words as possible using a set of 9 letters — with one mandatory **center letter** that must be included in every guess.

Built with [Streamlit](https://streamlit.io), this app is designed to make vocabulary building fun and interactive for Bahasa Indonesia learners and native speakers alike.

## ✨ Features

- 🔁 **Daily challenge**: Letters are randomized based on the current date.
- 🟢 **Center letter**: All valid guesses must contain this required letter.
- 🧠 **Real word list validation** using a dictionary file (`id-word-list.txt`).
- 📝 **Scoring system**: Points awarded based on word length.
- 🔀 **Shuffle letters** to see new word possibilities.
- 😓 **Give up option**: Reveals all possible answers with links to [KBBI](https://kbbi.kemdikbud.go.id).

## 📂 Project Structure

```

.
├── app.py               # Main Streamlit app
├── id-word-list.txt     # Indonesian dictionary (one word per line)
├── README.md            # Project documentation

````

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tebak-kata.git
cd tebak-kata
````

### 2. Install Dependencies

Install [Streamlit](https://streamlit.io) using pip:

```bash
pip install streamlit
```

### 3. Run the App

```bash
streamlit run app.py
```

### 4. Open in Browser

Visit the app at:

```
http://localhost:8501
```

## 📋 Word List Format

The `id-word-list.txt` file should contain:

* One word per line
* All lowercase
* No punctuation or special characters

Example:

```
kata
belajar
rumah
...
```

## 📸 Screenshot

<img width="670" height="839" alt="image" src="https://github.com/user-attachments/assets/2a523a62-4eaa-498e-9713-a989fbf4c5ce" />


![Screenshot](assets/screenshot.png)

## 🧠 Inspired By

This project is inspired by the [NYT Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee), adapted for Bahasa Indonesia to support language learning and vocabulary enrichment through play.

## 👨‍💻 Author

Developed by [MW Hidayat](https://github.com/mwhidayat)

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it.

## 🤝 Contributing

Contributions and suggestions are welcome!
Feel free to open an issue or submit a pull request.


