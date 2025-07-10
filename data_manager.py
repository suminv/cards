import pandas as pd
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
    Saves or updates a word in the hard words CSV file when answered incorrectly.

    - If the word is new, it's added with a correct_streak of 0 and incorrect_count of 1.
    - If the word already exists, its incorrect_count is incremented, and correct_streak is reset to 0.
    """
    identifier_cols = [col for col in COLUMNS if col not in ["section", "unit"]]

    try:
        hard_words_df = pd.read_csv(HARD_WORDS_FILE, dtype=str)
        hard_words_df.fillna("", inplace=True)
        # Ensure stat columns exist and are numeric
        if "correct_streak" not in hard_words_df.columns:
            hard_words_df["correct_streak"] = 0
        if "incorrect_count" not in hard_words_df.columns:
            hard_words_df["incorrect_count"] = 0
        if "is_active" not in hard_words_df.columns:
            hard_words_df["is_active"] = (
                "True"  # Store as string to avoid mixed types with bool
            )

        hard_words_df["correct_streak"] = pd.to_numeric(hard_words_df["correct_streak"])
        hard_words_df["incorrect_count"] = pd.to_numeric(
            hard_words_df["incorrect_count"]
        )

    except FileNotFoundError:
        hard_words_df = pd.DataFrame(
            columns=COLUMNS
            + ["date_added", "correct_streak", "incorrect_count", "is_active"]
        )

    # Check if the word already exists
    mask = pd.Series([True] * len(hard_words_df))
    for col in identifier_cols:
        mask &= hard_words_df[col] == word[col]

    existing_word_idx = hard_words_df[mask].index

    if not existing_word_idx.empty:
        # Word exists: update stats
        idx = existing_word_idx[0]
        hard_words_df.loc[idx, "correct_streak"] = 0
        hard_words_df.loc[idx, "incorrect_count"] += 1
        hard_words_df.loc[idx, "is_active"] = (
            "True"  # Reactivate if it was marked as learned
        )
    else:
        # Word is new: add it
        new_word = word.copy()
        new_word["date_added"] = datetime.now().strftime("%Y-%m-%d")
        new_word["correct_streak"] = 0
        new_word["incorrect_count"] = 1
        new_word["is_active"] = "True"
        hard_words_df = pd.concat(
            [hard_words_df, pd.DataFrame([new_word])], ignore_index=True
        )

    hard_words_df.to_csv(HARD_WORDS_FILE, index=False)


def update_on_correct_answer(word):
    """
    Updates the correct_streak for a word in the hard words file.
    Returns the new streak count.
    """
    identifier_cols = [col for col in COLUMNS if col not in ["section", "unit"]]

    try:
        hard_words_df = pd.read_csv(HARD_WORDS_FILE, dtype=str)
        hard_words_df.fillna("", inplace=True)
        hard_words_df["correct_streak"] = pd.to_numeric(hard_words_df["correct_streak"])
    except (FileNotFoundError, KeyError):
        return 0  # Should not happen if called correctly

    mask = pd.Series([True] * len(hard_words_df))
    for col in identifier_cols:
        mask &= hard_words_df[col] == word[col]

    existing_word_idx = hard_words_df[mask].index

    if not existing_word_idx.empty:
        idx = existing_word_idx[0]
        hard_words_df.loc[idx, "correct_streak"] += 1
        new_streak = hard_words_df.loc[idx, "correct_streak"]
        hard_words_df.to_csv(HARD_WORDS_FILE, index=False)
        return new_streak
    return 0


def mark_word_as_learned(word, streak_threshold=3):
    """
    Marks a word as inactive (learned) in the hard words file if its streak reaches the threshold.
    """
    identifier_cols = [col for col in COLUMNS if col not in ["section", "unit"]]

    try:
        hard_words_df = pd.read_csv(HARD_WORDS_FILE, dtype=str)
        hard_words_df.fillna("", inplace=True)
        # Ensure is_active column exists and is boolean
        if "is_active" not in hard_words_df.columns:
            hard_words_df["is_active"] = "True"

    except FileNotFoundError:
        return  # File doesn't exist, nothing to mark

    mask = pd.Series([True] * len(hard_words_df))
    for col in identifier_cols:
        mask &= hard_words_df[col] == word[col]

    existing_word_idx = hard_words_df[mask].index

    if not existing_word_idx.empty:
        idx = existing_word_idx[0]
        hard_words_df.loc[idx, "is_active"] = "False"  # Mark as inactive
        hard_words_df.to_csv(HARD_WORDS_FILE, index=False)
