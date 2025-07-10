# Language Learning Helper

A simple command-line application for learning new words from a custom vocabulary list.

## Features

-   **Load Vocabulary**: Supports both Excel (`.xlsx`) and CSV (`.csv`) files.
-   **Study Modes**: Includes Flashcards and Quiz modes.
-   **Intelligent Answer Checking**: Tolerates minor typos and spelling mistakes in quizzes.
-   **Practice Hard Words**: Automatically saves words you struggle with for focused practice.
-   **Modular & Organized**: Code is separated into logical modules for data management (`data_manager.py`), study modes (`modes.py`), and utilities (`utils.py`).

## Setup

1.  **Prerequisites**:
    *   Python 3.x
    *   A virtual environment (recommended)

2.  **Installation**:
    ```bash
    # Clone the repository
    git clone https://github.com/suminv/cards.git
    cd cards

    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    *   Create a `config.py` file in the project root.
    *   Add the following content, updating `EXCEL_FILE` to the absolute path of your vocabulary file:

    ```python
    # Absolute path to your vocabulary file (.xlsx or .csv)
    EXCEL_FILE = "/path/to/your/vocabulary.xlsx"

    # File to store words you get wrong
    HARD_WORDS_FILE = "hard_words.csv"

    # Required columns in your vocabulary file
    COLUMNS = ["section", "unit", "dutch", "english", "russian"]
    ```

## How to Run

Make sure your virtual environment is activated and your `config.py` is set up.

```bash
python main.py
```

## How to Use

The application will greet you with a menu:

```
--- Main Menu ---
1. Flashcards Mode
2. Quiz Mode
3. Practice Hard Words (Quiz)
4. Exit
```

-   **Flashcards Mode**: Review words without pressure. Choose a unit and a "front" language, then press Enter to reveal the translation.
-   **Quiz Mode**: Test your knowledge. Choose a unit and translation direction. Incorrect answers are saved to `hard_words.csv`.
-   **Practice Hard Words**: A quiz mode that only uses words from your `hard_words.csv` file.
