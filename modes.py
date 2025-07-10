import random
from colors import TermColors
from utils import check_answer
from data_manager import save_hard_word
from config import COLUMNS

def select_words_to_study(df):
    """
    Prompts the user to select a unit of words to study and returns a filtered DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing all words.

    Returns:
        pd.DataFrame or None: A DataFrame filtered by the selected unit, or the original
                              DataFrame if 'all' is selected. Returns None for invalid input.
    """
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
    """
    Runs the flashcards study mode.

    The user selects a language to be shown on the front of the card. The other languages
    are shown on the back. The user can quit at any time by typing 'q'.

    Args:
        df (pd.DataFrame): The DataFrame of words to study.
    """
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
    """
    Runs the quiz study mode.

    The user selects the 'from' and 'to' languages for translation. It scores the user's
    answers and saves incorrectly answered words for later practice.

    Args:
        df (pd.DataFrame): The DataFrame of words to be quizzed on.
        is_hard_words_mode (bool, optional): If True, runs the quiz on words marked as 'hard'.
                                         Defaults to False.
    """
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

        is_perfect_match = user_answer.strip().lower() == correct_answer.strip().lower()

        if is_perfect_match:
            print(f"{TermColors.OKGREEN}Correct!{TermColors.ENDC}")
            score += 1
        elif check_answer(user_answer, correct_answer):
            print(f"{TermColors.WARNING}Correct!{TermColors.ENDC}")
            print(f"{TermColors.WARNING}Correct answer: {correct_answer}{TermColors.ENDC}")
            score += 1
        else:
            print(f"{TermColors.FAIL}Incorrect. The correct answer is: {correct_answer}{TermColors.ENDC}")
            if not is_hard_words_mode:
                save_hard_word(word)

    print(f"\n{TermColors.HEADER}--- Quiz Finished ---{TermColors.ENDC}\nYour final score: {score}/{total}")
    if total > 0:
        print(f"You answered {TermColors.OKGREEN}{(score / total) * 100:.2f}%{TermColors.ENDC} correctly.")
