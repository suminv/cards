# Language Learning Helper

This is a simple command-line application built with Python to help you learn new words from a custom vocabulary list stored in an Excel file.

The application provides several modes to make learning effective and engaging.

## Features

- **Load Vocabulary from Excel**: Easily manage your word list in a `.xlsx` file.
- **Flashcards Mode**: Review words in a classic flashcard format.
- **Quiz Mode**: Test your knowledge by translating words.
- **Practice Hard Words**: The app keeps track of words you get wrong in quizzes and lets you practice them separately.
- **Dynamic Updates**: Any changes to your Excel file are reflected the next time you start the app.

## Setup

### 1. Prerequisites

- Python 3.x
- A virtual environment (recommended)

### 2. Installation

1.  **Clone the repository or download the files.**

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If a `requirements.txt` file is not available, install the dependencies manually: `pip install pandas openpyxl`)*

### 3. Prepare Your Word List

1.  Create an Excel file named `words.xlsx` in the same directory as the `main.py` script.
2.  The file **must** contain the following columns in the first sheet:
    - `section`
    - `unit`
    - `dutch`
    - `english`
    - `russian`

    You can add as many rows (words) as you like.

## How to Run

1.  Make sure your virtual environment is activated.
2.  Run the main script from your terminal:
    ```bash
    python main.py
    ```

## How to Use

Once the application starts, you will see the main menu:

```
--- Main Menu ---
1. Flashcards Mode
2. Quiz Mode
3. Practice Hard Words (Quiz)
4. Exit
```

### Flashcards Mode

- **Purpose**: To study and review words without pressure.
- **How it works**:
    1.  Choose a `unit` of words to study (or all of them).
    2.  Select the language you want to see on the "front" of the card.
    3.  The app will show you a word. Press `Enter` to reveal the translation on the "back" of the card.
    4.  Type `q` and press `Enter` at any time to return to the main menu.

### Quiz Mode

- **Purpose**: To actively test your knowledge.
- **How it works**:
    1.  Choose a `unit` of words for the quiz.
    2.  Select the language you want to translate **from** and **to**.
    3.  The app will show you a word and ask for the translation.
    4.  Type your answer and press `Enter`. The app will tell you if you were correct.
    5.  If your answer is incorrect, the word will be automatically added to your `hard_words.csv` file for later practice.
    6.  At the end of the quiz, you will see your final score.

### Practice Hard Words

- **Purpose**: To focus specifically on the words you find difficult.
- **How it works**: This mode is identical to the **Quiz Mode**, but it only uses words from the `hard_words.csv` file that is automatically generated during quizzes.
