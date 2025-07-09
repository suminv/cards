# Language Learning Helper

This is a simple command-line application built with Python to help you learn new words from a custom vocabulary list.

The application is now more modular and configurable, with a colorful and engaging user interface.

## Features

- **Load Vocabulary from Excel/CSV**: Easily manage your word list in a `.xlsx` or `.csv` file.
- **Configurable File Paths**: Set the path to your word list in a separate configuration file, allowing you to store it anywhere, including cloud services like iCloud Drive.
- **Flashcards Mode**: Review words in a classic flashcard format.
- **Quiz Mode**: Test your knowledge by translating words.
- **Intelligent Answer Checking**: In quiz mode, the app tolerates small typos and spelling mistakes, giving you credit for answers that are "close enough".
- **Practice Hard Words**: The app keeps track of words you get wrong and lets you practice them separately.
- **Color-Coded Interface**: Enjoy a more readable and visually appealing experience in your terminal.
- **Modular Code**: The code is split into logical files (`main.py`, `config.py`, `colors.py`, `utils.py`) for better organization and maintainability.

## Setup

### 1. Prerequisites

- Python 3.x
- A virtual environment (recommended)

### 2. Installation

1.  **Clone the repository or download the files.**
    ```bash
    git clone https://github.com/suminv/cards.git
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the configuration file:**
    Create a file named `config.py` in the same directory as `main.py`. See the **Configuration** section below for details.

## Configuration

Before running the application, you need to create a `config.py` file to tell the script where to find your words and what columns to expect.

1.  Create a file named `config.py`.
2.  Copy and paste the following code into it, adjusting the `EXCEL_FILE` path to point to your vocabulary file.

### Example `config.py`

```python
# Path to your vocabulary file. Can be an Excel (.xlsx) or CSV (.csv) file.
# This example shows a path to a file in iCloud Drive.
EXCEL_FILE = "path to your vocabulary file"

# Name of the file where words you get wrong will be saved.
HARD_WORDS_FILE = "hard_words.csv"

# The columns your vocabulary file must contain.
COLUMNS = ["section", "unit", "dutch", "english", "russian"]
```

Your vocabulary file (e.g., `filename.xlsx`) **must** contain the columns specified in the `COLUMNS` list.

## How to Run

1.  Make sure your `config.py` file is set up correctly.
2.  Make sure your virtual environment is activated.
3.  Run the main script from your terminal:
    ```bash
    python main.py
    ```

## How to Use

Once the application starts, you will see the color-coded main menu:

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
    4.  Type your answer and press `Enter`.
    5.  The app will check your answer intelligently:
        - **Perfect Match**: `Correct!` is shown in green.
        - **Close Match (with typo)**: `Correct!` is shown in yellow, and the proper spelling is displayed for you to review.
        - **Incorrect Match**: The correct answer is shown in red.
    6.  If your answer is incorrect, the word will be automatically added to your `hard_words.csv` file for later practice.
    7.  At the end of the quiz, you will see your final score.

### Practice Hard Words

- **Purpose**: To focus specifically on the words you find difficult.
- **How it works**: This mode is identical to the **Quiz Mode**, but it only uses words from the `hard_words.csv` file that is automatically generated during quizzes. The same intelligent answer checking applies here.