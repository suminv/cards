from data_manager import load_words
from modes import flashcards_mode, quiz_mode
from colors import TermColors
from config import HARD_WORDS_FILE

def main():
    """Runs the main application loop, allowing the user to select study modes."""
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