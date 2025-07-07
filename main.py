import pandas as pd
import random
import os

# --- Configuration ---
EXCEL_FILE = "duolingo.xlsx"
HARD_WORDS_FILE = "hard_words.csv"
COLUMNS = ["section", "unit", "dutch", "english", "russian"]


# --- Data Loading ---
def load_words(file_path=EXCEL_FILE):
    """Loads words from the specified Excel or CSV file."""
    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            print(f"Error: Unsupported file format for {file_path}")
            return None

        if not all(col in df.columns for col in COLUMNS):
            print(f"Error: The file must contain the columns: {', '.join(COLUMNS)}")
            return None
        df.fillna("", inplace=True)
        return df
    except FileNotFoundError:
        # This is okay if the hard_words file doesn't exist yet
        if file_path == HARD_WORDS_FILE:
            return pd.DataFrame(columns=COLUMNS)  # Return empty dataframe
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
        return None


def save_hard_word(word):
    """Appends a word to the hard words CSV file."""
    df_to_append = pd.DataFrame([word])
    # Write header only if file doesn't exist, otherwise append without header
    header = not os.path.exists(HARD_WORDS_FILE)
    df_to_append.to_csv(HARD_WORDS_FILE, mode="a", header=header, index=False)


# --- Core Components ---
def select_words_to_study(df):
    """Asks the user to select a unit and returns the corresponding dataframe."""
    all_units = sorted(df["unit"].unique())
    print("Available units:", ", ".join(map(str, all_units)))
    unit_choice = input(
        "Enter a unit number to study or type 'all' to study all units: "
    )

    if unit_choice.lower() == "all":
        return df
    else:
        try:
            chosen_unit = int(unit_choice)
            if chosen_unit not in all_units:
                print("Invalid unit number.")
                return None
            return df[df["unit"] == chosen_unit]
        except ValueError:
            print("Invalid input. Please enter a number or 'all'.")
            return None


# --- Learning Modes ---
def flashcards_mode(df):
    """Runs the flashcards learning mode."""
    print("\n--- Flashcards Mode ---")
    study_df = select_words_to_study(df)
    if study_df is None or study_df.empty:
        print("No words to study. Returning to main menu.")
        return

    language_map = {"1": "dutch", "2": "english", "3": "russian"}
    print("\nWhich language to show on the front of the card?")
    print("1. Dutch\n2. English\n3. Russian")
    lang_choice = input("Choose a language (1-3): ")

    if lang_choice not in language_map:
        print("Invalid language choice. Returning to main menu.")
        return

    front_lang = language_map[lang_choice]
    back_langs = [lang for lang in COLUMNS[2:] if lang != front_lang]
    word_list = study_df.to_dict("records")
    random.shuffle(word_list)

    print(
        f"\nStarting flashcards for {len(word_list)} words. Press Enter to reveal, type 'q' to quit."
    )
    for i, word in enumerate(word_list):
        print(f"\n--- Card {i + 1}/{len(word_list)} ---")
        print(f"{front_lang.capitalize()}: {word[front_lang]}")

        action = input()
        if action.lower() == "q":
            break

        print("--- Answer ---")
        for lang in back_langs:
            print(f"{lang.capitalize()}: {word[lang]}")
        if "section" in word and word["section"]:
            print(f"Section: {word['section']}")
    print("\nFlashcards session finished!")


def quiz_mode(df, is_hard_words_mode=False):
    """Runs the quiz learning mode."""
    print("\n--- Quiz Mode ---" + (" (Hard Words)" if is_hard_words_mode else ""))

    study_df = df if is_hard_words_mode else select_words_to_study(df)
    if study_df is None or study_df.empty:
        print("No words to study. Returning to main menu.")
        return

    language_map = {"1": "dutch", "2": "english", "3": "russian"}
    print("\nSelect the language to translate FROM:")
    for key, lang in language_map.items():
        print(f"{key}. {lang.capitalize()}")
    from_lang_choice = input("Choose a language (1-3): ")

    print("\nSelect the language to translate TO:")
    for key, lang in language_map.items():
        print(f"{key}. {lang.capitalize()}")
    to_lang_choice = input("Choose a language (1-3): ")

    if (
        from_lang_choice not in language_map
        or to_lang_choice not in language_map
        or from_lang_choice == to_lang_choice
    ):
        print("Invalid language selection. Returning to main menu.")
        return

    from_lang, to_lang = language_map[from_lang_choice], language_map[to_lang_choice]
    word_list = study_df.to_dict("records")
    random.shuffle(word_list)

    score, total = 0, len(word_list)
    print(f"\nStarting quiz for {total} words. Type 'q' to quit.")

    for i, word in enumerate(word_list):
        question_word = word[from_lang]
        correct_answer = str(word[to_lang])
        user_answer = input(
            f"\nQ{i + 1}: Translate '{question_word}' from {from_lang.capitalize()} to {to_lang.capitalize()}: "
        )

        if user_answer.lower() == "q":
            break

        if user_answer.strip().lower() == correct_answer.strip().lower():
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is: {correct_answer}")
            if not is_hard_words_mode:
                save_hard_word(word)

    print(f"\n--- Quiz Finished ---\nYour final score: {score}/{total}")
    if total > 0:
        print(f"You answered {(score / total) * 100:.2f}% correctly.")


# --- Main Application Logic ---
def main():
    """Main function to run the learning program."""
    words_df = load_words()
    if words_df is None:
        return

    print("Welcome to the Language Learning Helper!")
    print(f"Successfully loaded {len(words_df)} words.")

    while True:
        print("\n--- Main Menu ---")
        print("1. Flashcards Mode")
        print("2. Quiz Mode")
        print("3. Practice Hard Words (Quiz)")
        print("4. Exit")
        choice = input("Please choose a mode (1-4): ")

        if choice == "1":
            flashcards_mode(words_df)
        elif choice == "2":
            quiz_mode(words_df)
        elif choice == "3":
            hard_words_df = load_words(HARD_WORDS_FILE)
            if hard_words_df is not None and not hard_words_df.empty:
                quiz_mode(hard_words_df, is_hard_words_mode=True)
            else:
                print("\nNo hard words to practice yet. Keep taking quizzes!")
        elif choice == "4":
            print("Happy learning! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
