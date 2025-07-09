import pandas as pd
import random
import os
from config import EXCEL_FILE, HARD_WORDS_FILE, COLUMNS
from colors import TermColors

def load_words(file_path=EXCEL_FILE):
    """Loads words from the specified Excel or CSV file."""
    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path, dtype=str)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path, dtype=str)
        else:
            print(f"{TermColors.FAIL}Error: Unsupported file format for {file_path}{TermColors.ENDC}")
            return None

        if not all(col in df.columns for col in COLUMNS):
            print(f"{TermColors.FAIL}Error: The file must contain the columns: {', '.join(COLUMNS)}{TermColors.ENDC}")
            return None
        df.fillna("", inplace=True)
        return df
    except FileNotFoundError:
        if file_path == HARD_WORDS_FILE:
            return pd.DataFrame(columns=COLUMNS)
        print(f"{TermColors.FAIL}Error: The file '{file_path}' was not found.{TermColors.ENDC}")
        return None
    except Exception as e:
        print(f"{TermColors.FAIL}An unexpected error occurred while reading '{file_path}': {e}{TermColors.ENDC}")
        return None


def save_hard_word(word):
    """Appends a word to the hard words CSV file."""
    df_to_append = pd.DataFrame([word])
    header = not os.path.exists(HARD_WORDS_FILE)
    df_to_append.to_csv(HARD_WORDS_FILE, mode="a", header=header, index=False)


def select_words_to_study(df):
    """Asks the user to select a unit and returns the corresponding dataframe."""
    all_units = sorted(df["unit"].unique())
    print(f"{TermColors.OKCYAN}Available units:{TermColors.ENDC}", ", ".join(map(str, all_units)))
    unit_choice = input(
        f"{TermColors.BOLD}Enter a unit number to study or type 'all' to study all units: {TermColors.ENDC}"
    )

    if unit_choice.lower() == "all":
        return df
    else:
        if unit_choice in all_units:
            return df[df["unit"] == unit_choice]
        else:
            print(f"{TermColors.FAIL}Invalid unit number.{TermColors.ENDC}")
            return None


def flashcards_mode(df):
    """Runs the flashcards learning mode."""
    print(f"\n{TermColors.HEADER}--- Flashcards Mode ---{TermColors.ENDC}")
    study_df = select_words_to_study(df)
    if study_df is None or study_df.empty:
        print(f"{TermColors.WARNING}No words to study. Returning to main menu.{TermColors.ENDC}")
        return

    language_map = {"1": "dutch", "2": "english", "3": "russian"}
    print(f"\n{TermColors.OKBLUE}Which language to show on the front of the card?{TermColors.ENDC}")
    print("1. Dutch\n2. English\n3. Russian")
    lang_choice = input(f"{TermColors.BOLD}Choose a language (1-3): {TermColors.ENDC}")

    if lang_choice not in language_map:
        print(f"{TermColors.FAIL}Invalid language choice. Returning to main menu.{TermColors.ENDC}")
        return

    front_lang = language_map[lang_choice]
    back_langs = [lang for lang in COLUMNS[2:] if lang != front_lang]
    word_list = study_df.to_dict("records")
    random.shuffle(word_list)

    print(
        f"\n{TermColors.OKCYAN}Starting flashcards for {len(word_list)} words. Press Enter to reveal, type 'q' to quit.{TermColors.ENDC}"
    )
    for i, word in enumerate(word_list):
        print(f"\n{TermColors.HEADER}--- Card {i + 1}/{len(word_list)} ---{TermColors.ENDC}")
        print(f"{TermColors.BOLD}{front_lang.capitalize()}:{TermColors.ENDC} {word[front_lang]}")

        action = input()
        if action.lower() == "q":
            break

        print(f"{TermColors.OKGREEN}--- Answer ---{TermColors.ENDC}")
        for lang in back_langs:
            print(f"{TermColors.BOLD}{lang.capitalize()}:{TermColors.ENDC} {word[lang]}")
        if "section" in word and word["section"]:
            print(f"{TermColors.BOLD}Section:{TermColors.ENDC} {word['section']}")
    print(f"\n{TermColors.OKGREEN}Flashcards session finished!{TermColors.ENDC}")


def quiz_mode(df, is_hard_words_mode=False):
    """Runs the quiz learning mode."""
    print(f"\n{TermColors.HEADER}--- Quiz Mode ---{TermColors.ENDC}" + (f" {TermColors.WARNING}(Hard Words){TermColors.ENDC}" if is_hard_words_mode else ""))

    study_df = df if is_hard_words_mode else select_words_to_study(df)
    if study_df is None or study_df.empty:
        print(f"{TermColors.WARNING}No words to study. Returning to main menu.{TermColors.ENDC}")
        return

    language_map = {"1": "dutch", "2": "english", "3": "russian"}
    print(f"\n{TermColors.OKBLUE}Select the language to translate FROM:{TermColors.ENDC}")
    for key, lang in language_map.items():
        print(f"{key}. {lang.capitalize()}")
    from_lang_choice = input(f"{TermColors.BOLD}Choose a language (1-3): {TermColors.ENDC}")

    print(f"\n{TermColors.OKBLUE}Select the language to translate TO:{TermColors.ENDC}")
    for key, lang in language_map.items():
        print(f"{key}. {lang.capitalize()}")
    to_lang_choice = input(f"{TermColors.BOLD}Choose a language (1-3): {TermColors.ENDC}")

    if (
        from_lang_choice not in language_map
        or to_lang_choice not in language_map
        or from_lang_choice == to_lang_choice
    ):
        print(f"{TermColors.FAIL}Invalid language selection. Returning to main menu.{TermColors.ENDC}")
        return

    from_lang, to_lang = language_map[from_lang_choice], language_map[to_lang_choice]
    word_list = study_df.to_dict("records")
    random.shuffle(word_list)

    score, total = 0, len(word_list)
    print(f"\n{TermColors.OKCYAN}Starting quiz for {total} words. Type 'q' to quit.{TermColors.ENDC}")

    for i, word in enumerate(word_list):
        question_word = word[from_lang]
        correct_answer = str(word[to_lang])
        user_answer = input(
            f"\n{TermColors.BOLD}Q{i + 1}: Translate '{question_word}' from {from_lang.capitalize()} to {to_lang.capitalize()}: {TermColors.ENDC}"
        )

        if user_answer.lower() == "q":
            break

        if user_answer.strip().lower() == correct_answer.strip().lower():
            print(f"{TermColors.OKGREEN}Correct!{TermColors.ENDC}")
            score += 1
        else:
            print(f"{TermColors.FAIL}Incorrect. The correct answer is: {correct_answer}{TermColors.ENDC}")
            if not is_hard_words_mode:
                save_hard_word(word)

    print(f"\n{TermColors.HEADER}--- Quiz Finished ---{TermColors.ENDC}\nYour final score: {score}/{total}")
    if total > 0:
        print(f"You answered {TermColors.OKGREEN}{(score / total) * 100:.2f}%{TermColors.ENDC} correctly.")


def main():
    """Main function to run the learning program."""
    words_df = load_words()
    if words_df is None:
        return

    print(f"{TermColors.HEADER}Welcome to the Language Learning Helper!{TermColors.ENDC}")
    print(f"Successfully loaded {len(words_df)} words.")

    while True:
        print(f"\n{TermColors.HEADER}--- Main Menu ---{TermColors.ENDC}")
        print(f"{TermColors.OKBLUE}1. Flashcards Mode{TermColors.ENDC}")
        print(f"{TermColors.OKBLUE}2. Quiz Mode{TermColors.ENDC}")
        print(f"{TermColors.OKBLUE}3. Practice Hard Words (Quiz){TermColors.ENDC}")
        print(f"{TermColors.OKBLUE}4. Exit{TermColors.ENDC}")
        choice = input(f"{TermColors.BOLD}Please choose a mode (1-4): {TermColors.ENDC}")

        if choice == "1":
            flashcards_mode(words_df)
        elif choice == "2":
            quiz_mode(words_df)
        elif choice == "3":
            hard_words_df = load_words(HARD_WORDS_FILE)
            if hard_words_df is not None and not hard_words_df.empty:
                quiz_mode(hard_words_df, is_hard_words_mode=True)
            else:
                print(f"\n{TermColors.WARNING}No hard words to practice yet. Keep taking quizzes!{TermColors.ENDC}")
        elif choice == "4":
            print(f"{TermColors.OKGREEN}Happy learning! Goodbye!{TermColors.ENDC}")
            break
        else:
            print(f"{TermColors.FAIL}Invalid choice. Please enter a number between 1 and 4.{TermColors.ENDC}")


if __name__ == "__main__":
    main()

