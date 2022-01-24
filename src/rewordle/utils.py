def generate_response(guess_word: str, secret_word: str) -> list[str]:
    """Generate a response list.

    Check guess word against the secret word. Return a list of string markers:
    - green if chars match exactly
    - yellow if guess word char exists in a secret word
    - gray if guess word char does not exist in a secret word
    """
    response_list = []
    for guess_char, secret_char in zip(guess_word, secret_word):
        if guess_char == secret_char:
            response_list.append("green")
        elif guess_char in secret_word:
            response_list.append("yellow")
        else:
            response_list.append("gray")
    return response_list
