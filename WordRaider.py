import random
from pathlib import Path

BASE_DIR = Path(__file__).parent
ANSWERS_PATH = BASE_DIR / "ref" / "answers.txt"
VALID_GUESSES_PATH = BASE_DIR / "ref" / "valid_guesses.txt"
MAX_TURNS = 6

def get_words(filepath:Path) -> list[str]:
    words_list = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():
                words_list.append(line.strip().lower())
        return words_list

def get_todays_word(filepath:Path)->str:
    words_list = get_words(filepath)
    todays_word = random.choice(words_list)
    return todays_word

def check_if_guess_valid(guess:str, word_length:int, valid_guesses:set[str], guesses:list[str])-> tuple[bool, str]:
    # Check if length of guess is good
    if len(guess) != word_length:
        return False, f"The number of letters in the word is {word_length}, you guessed {len(guess)}" 
    if not guess.isalpha():
        return False, "The guess must only be letters"
    if guess not in valid_guesses:
        return False, "Invalid Guess - Not in Valid Guess Library"
    if guess in guesses:
        return False, f"{guess} already guessed."
    return True, "Guess Works"

def check_letter_match(guess:str, answer:str) -> tuple[list[str], list[str], list[str]]:
    '''
    Score one guess against the answer.

    Returns:
        - turn_pattern: letter at each position matches exactly, "_" elsewhere.
        - turn_present_letters: letters in the answer but in the wrong position.
        - turn_absent_letters: letters with no unclaimed copy left in the answer.

    Each letter in the answer can be claimed once: exact matches first,
    then misplaced matches left to right.  So guessing "eerie" against
    "sheep" gives two present e's and one absent e.
    '''

    answer_chars = list(answer)
    turn_pattern = ["_"]*len(answer)
    turn_present_letters = []
    turn_absent_letters = []

    for idx,letter in enumerate(guess):
        if letter == answer[idx]:
            turn_pattern[idx] = letter
            answer_chars[idx] = None

    for idx, letter in enumerate(guess):
        if turn_pattern[idx] != "_":
            continue
        elif letter in answer_chars:
            turn_present_letters.append(letter)
            answer_chars.remove(letter)
        else:
            turn_absent_letters.append(letter)
    return turn_pattern, turn_present_letters, turn_absent_letters


def save_pattern(pattern: list[str], turn_pattern:list[str]) -> list[str]:
    updated_pattern = list(pattern)
    for idx,letter in enumerate(turn_pattern):
        if letter != "_":
            updated_pattern[idx] = letter
    return updated_pattern

def save_present_letters(pattern:list[str], present_letters:set[str], turn_present_letters:list[str]) -> set[str]:
    to_remove = "_"
    cleaned_pattern = { n for n in pattern if n!=to_remove }
    updated_present_letters = cleaned_pattern | present_letters | set(turn_present_letters)
    return updated_present_letters

def save_absent_letters(absent_letters:list[str], turn_absent_letters:list[str], present_letters:set[str]) -> set[str]:
    # assign as sets
    set_absent_letters = set(absent_letters)
    set_turn_absent_letters = set(turn_absent_letters)
    set_present_letters = set(present_letters)

    # Union
    updated_absent_letters = (set_absent_letters | set_turn_absent_letters) - set_present_letters
    return updated_absent_letters

def save_turn_state(
        pattern: list[str], turn_pattern:list[str], 
        present_letters, turn_present_letters,
        absent_letters, turn_absent_letters
        ) -> tuple[list[str], set[str], set[str]]:
    updated_pattern = save_pattern(pattern, turn_pattern)
    updated_present_letters = save_present_letters(updated_pattern, present_letters, turn_present_letters)
    updated_absent_letters = save_absent_letters(absent_letters, turn_absent_letters, updated_present_letters)
    return updated_pattern, updated_present_letters, updated_absent_letters

def main():
    # Initialize
    todays_word = get_todays_word(ANSWERS_PATH)
    valid_guesses = set(get_words(VALID_GUESSES_PATH)) | set(get_words(ANSWERS_PATH))
    print("Welcome to Word Raider, my attempt at rebuild wordle!")
    print("A mystery word has been loaded!")
    print(f"There are {len(todays_word)} letters in the word")

    # Set Config
    current_turn = 0
    guesses = []
    pattern = ["_"]*len(todays_word)
    present_letters = set()
    absent_letters = set()
    
    while current_turn < MAX_TURNS:
        print(f"We are on turn {current_turn+1} of {MAX_TURNS}")
        user_guess = input(f"Guess a {len(todays_word)} letter word! ").lower()
        is_valid, message = check_if_guess_valid(user_guess, len(todays_word), valid_guesses, guesses)
        if not is_valid:
            print(message)
            continue

        current_turn += 1
        guesses.append(user_guess)
        turn_pattern, turn_present_letters, turn_absent_letters = check_letter_match(user_guess, todays_word)
        pattern, present_letters, absent_letters = save_turn_state(
                                                                            pattern, turn_pattern,
                                                                            present_letters, turn_present_letters,
                                                                            absent_letters, turn_absent_letters,
                                                                        )
        print(pattern)
        print(f'These letters are in the word: {present_letters}')
        print(f'These letters are absent from the word: {absent_letters}')
        if user_guess == todays_word:
            print(f"Congratulations! You guessed correctly in {current_turn} turns! ")
            print(f"Your guesses were {guesses}")
            break

    else:
        print(f"Game over! The word was {todays_word}")

if __name__ == "__main__":
    main()
