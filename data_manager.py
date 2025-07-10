import pandas as pd
import os
from datetime import datetime
from config import EXCEL_FILE, HARD_WORDS_FILE, COLUMNS
from colors import TermColors


def load_words(file_path=EXCEL_FILE):
    """
    Loads words from the specified Excel or CSV file.

    Handles file not found errors and ensures the file has the required columns.

    Args:
        file_path (str, optional): The path to the file to load.
                                 Defaults to EXCEL_FILE from config.

    Returns:
        pd.DataFrame or None: A DataFrame containing the words, or None if an error occurs.
    """
    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path, dtype=str)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path, dtype=str)
        else:
            print(
                f"{TermColors.FAIL}Error: Unsupported file format for {file_path}{TermColors.ENDC}"
            )
            return None

        if not all(col in df.columns for col in COLUMNS):
            print(
                f"{TermColors.FAIL}Error: The file must contain the columns: {', '.join(COLUMNS)}{TermColors.ENDC}"
            )
            return None
        df.fillna("", inplace=True)
        return df
    except FileNotFoundError:
        if file_path == HARD_WORDS_FILE:
            return pd.DataFrame(columns=COLUMNS)
        print(
            f"{TermColors.FAIL}Error: The file '{file_path}' was not found.{TermColors.ENDC}"
        )
        return None
    except Exception as e:
        print(
            f"{TermColors.FAIL}An unexpected error occurred while reading '{file_path}': {e}{TermColors.ENDC}"
        )
        return None


def save_hard_word(word):
    """
    Saves a word to the hard words CSV file if it's not already present.

    Checks for duplicates based on the word's content (excluding section and unit).
    Adds a timestamp when saving a new word.

    Args:
        word (dict): A dictionary representing the word to save.
    """
    identifier_cols = [col for col in COLUMNS if col not in ["section", "unit"]]

    try:
        hard_words_df = pd.read_csv(HARD_WORDS_FILE, dtype=str)
        hard_words_df.fillna("", inplace=True)
    except FileNotFoundError:
        hard_words_df = pd.DataFrame()

    new_word_df = pd.DataFrame([word])

    is_duplicate = False
    if not hard_words_df.empty:
        merged_df = pd.merge(hard_words_df, new_word_df, on=identifier_cols)
        if not merged_df.empty:
            is_duplicate = True

    if not is_duplicate:
        word_to_save = word.copy()
        word_to_save["date_added"] = datetime.now().strftime("%Y-%m-%d")
        df_to_append = pd.DataFrame([word_to_save])
        header = not os.path.exists(HARD_WORDS_FILE)
        df_to_append.to_csv(HARD_WORDS_FILE, mode="a", header=header, index=False)
