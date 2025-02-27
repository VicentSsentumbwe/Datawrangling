import random
from SpellingBeeGraphics import SpellingBeeGraphics

# Constants
DICTIONARY_FILE = "EnglishWords.txt"

# Create the SpellingBeeGraphics object
sbg = SpellingBeeGraphics()
total_score = 0  # Track the total game score
found_words = set()  # Keep track of words already guessed
valid_words = []  # Store valid words for hinting

def load_dictionary():
    """Loads words from EnglishWords.txt into a set."""
    try:
        with open(DICTIONARY_FILE, "r") as file:
            return {word.strip().lower() for word in file}  # Use a set for fast lookup
    except FileNotFoundError:
        sbg.show_message("Error: Dictionary file not found!", "Red")
        return set()

def is_valid_puzzle(puzzle):
    """Checks if the puzzle input is valid."""
    if len(puzzle) != 7:
        return False, "Puzzle must contain exactly seven letters."
    if not puzzle.isalpha():
        return False, "Puzzle must contain only letters (A-Z)."
    if len(set(puzzle)) != 7:
        return False, "Puzzle must not contain duplicate letters."
    return True, ""

def puzzle_action(s):
    """Handles user input for the puzzle field."""
    puzzle = sbg.get_field("Puzzle").upper()  # Convert input to uppercase
    valid, message = is_valid_puzzle(puzzle)

    if valid:
        sbg.set_beehive_letters(puzzle)  # ✅ Updates the beehive with the letters
        sbg.show_message(f"Puzzle updated: {puzzle}", "Green")
        found_words.clear()  # Reset words when puzzle changes
        global total_score, valid_words
        total_score = 0  # Reset score
        valid_words = []  # Reset hint list
    else:
        sbg.show_message(f"Invalid puzzle: {message}", "Red")

def is_valid_word(word, beehive_letters, center_letter):
    """Checks if a word is a valid solution for the puzzle."""
    return (
        len(word) >= 4 and  # At least 4 letters
        center_letter in word and  # Must contain the center letter
        set(word).issubset(set(beehive_letters))  # Only use beehive letters
    )

def calculate_score(word, beehive_letters):
    """Calculates the score for a word based on game rules."""
    base_score = 1 if len(word) == 4 else len(word)  # 4-letter words = 1, others = word length
    if set(word) == set(beehive_letters):  # Check if it's a pangram
        base_score += 7  # Bonus for pangram
    return base_score

def solve_action(s):
    """Finds and displays valid words from the dictionary and updates the score."""
    global total_score, valid_words
    sbg.clear_word_list()  # Clear previous words
    total_score = 0  # Reset score
    valid_words = []  # Reset hints list

    beehive_letters = sbg.get_beehive_letters().lower()
    if len(beehive_letters) != 7:
        sbg.show_message("Please enter a valid 7-letter puzzle first!", "Red")
        return

    center_letter = beehive_letters[0]  # The first letter is the center letter
    dictionary = load_dictionary()

    found_words.clear()  # Reset word list

    for word in dictionary:
        if is_valid_word(word, beehive_letters, center_letter):
            add_word_to_list(word, beehive_letters)
            valid_words.append(word)  # Store words for hint system

    if not found_words:
        sbg.show_message("No valid words found!", "Red")
    else:
        sbg.show_message(f"Found {len(found_words)} words! Total Score: {total_score}", "Green")

def add_word_to_list(word, beehive_letters):
    """Adds a valid word to the word list and updates the score."""
    found_words.add(word)  # Store found word
    global total_score
    score = calculate_score(word, beehive_letters)
    total_score += score

    if set(word) == set(beehive_letters):  # Check if it's a pangram
        sbg.add_word(f"{word} (+{score})", "Blue")  # Display pangram in blue
    else:
        sbg.add_word(f"{word} (+{score})", "Black")  # Regular word in black

def shuffle_action(s):
    """Shuffles the beehive letters while keeping the center letter fixed."""
    beehive_letters = sbg.get_beehive_letters().upper()
    if len(beehive_letters) != 7:
        sbg.show_message("Please enter a valid 7-letter puzzle first!", "Red")
        return

    center_letter = beehive_letters[0]  # Keep the center letter fixed
    outer_letters = list(beehive_letters[1:])  # Get outer letters
    random.shuffle(outer_letters)  # Shuffle outer letters
    shuffled_puzzle = center_letter + "".join(outer_letters)  # Reassemble

    sbg.set_beehive_letters(shuffled_puzzle)  # ✅ Update beehive with shuffled letters
    sbg.show_message("Beehive letters shuffled!", "Blue")

def hint_action(s):
    """Gives the user a hint by displaying one random valid word."""
    if not valid_words:
        sbg.show_message("Solve the puzzle first to get hints!", "Red")
        return

    hint_word = random.choice(valid_words)  # Pick a random word
    sbg.show_message(f"Hint: {hint_word}", "Purple")  # Show hint in purple

def check_word_action(s):
    """Handles user input for checking a single word."""
    word = sbg.get_field("Word").lower()
    beehive_letters = sbg.get_beehive_letters().lower()

    if len(beehive_letters) != 7:
        sbg.show_message("Please enter a valid 7-letter puzzle first!", "Red")
        return

    center_letter = beehive_letters[0]  # The first letter is the center letter
    dictionary = load_dictionary()

    if word in found_words:
        sbg.show_message("You already found this word!", "Red")
    elif word not in dictionary:
        sbg.show_message("Word not in dictionary!", "Red")
    elif not is_valid_word(word, beehive_letters, center_letter):
        sbg.show_message("Word does not follow puzzle rules!", "Red")
    else:
        add_word_to_list(word, beehive_letters)
        sbg.show_message(f"Correct! Score: {total_score}", "Green")

def spelling_bee():
    """Sets up the Spelling Bee GUI."""
    sbg.add_field("Puzzle", puzzle_action)
    sbg.add_button("Solve", solve_action)
    sbg.add_field("Word", check_word_action)
    sbg.add_button("Shuffle", shuffle_action)  # ✅ Add shuffle button
    sbg.add_button("Hint", hint_action)  # ✅ Add hint button

# Run the program
if __name__ == "__main__":
    spelling_bee()

