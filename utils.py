import difflib

def check_answer(user_answer, correct_answer, threshold=0.85):
    """
    Checks if the user's answer is similar enough to the correct answer.

    Uses difflib to compare the normalized (lowercase, stripped) strings.

    Args:
        user_answer (str): The answer provided by the user.
        correct_answer (str): The correct answer.
        threshold (float, optional): The similarity ratio threshold (0.0 to 1.0). 
                                 Defaults to 0.85.

    Returns:
        bool: True if the similarity is above the threshold, False otherwise.
    """
    user_answer_normalized = user_answer.lower().strip()
    correct_answer_normalized = correct_answer.lower().strip()
    similarity_ratio = difflib.SequenceMatcher(None, user_answer_normalized, correct_answer_normalized).ratio()
    return similarity_ratio >= threshold
