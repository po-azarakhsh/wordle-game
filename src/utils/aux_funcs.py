import random
from typing import Dict, List


def get_color(idx: int, letter: str, target_word: str) -> str:
    """
    Return the color hex code for a guessed letter in a Wordle-style game.

    Parameters
    ----------
    idx : int
        The index position of the current letter in the guess.
    letter : str
        The guessed character.
    target_word : str
        The correct target word.

    Returns
    -------
    str
        Hex color representing the correctness of the guess:
        - "#6AAA64" : Correct letter in the correct position (green).
        - "#F9DC3C" : Letter exists in the word but wrong position (yellow).
        - "#A9A9A9" : Letter not in the word (gray).
    """
    if letter in target_word and letter != target_word[idx]:
        return "#F9DC3C"  # present but wrong position
    elif letter == target_word[idx]:
        return "#6AAA64"  # correct letter and position
    else:
        return "#A9A9A9"  # not present


def word_selection(
    word_len: int,
    word_level: int,
    game_levels: Dict[str, List[int]]
) -> str:
    """
    Select a random target word from a frequency-based word list.

    Parameters
    ----------
    word_len : int
        Desired length of the target word (e.g., 4, 5, 6 letters).
    word_level : int
        Difficulty level index (1-based) used to slice the frequency list.
        Typically derived from `game_levels[chosen_level][1]`.
    game_levels : dict[str, list[int]]
        Mapping of game levels to their configuration. Only the
        number of levels (len(game_levels)) is used to partition
        the candidate words into equal difficulty bands.

    Returns
    -------
    str
        A randomly chosen uppercase word that matches the requested
        length and frequency threshold.
    """
    file_path: str = "src/data/words_freq.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        words_freq: Dict[str, int] = {}

        # Read word-frequency pairs and filter by length & minimum frequency
        for line in f:
            word, freq = line.strip().split(",")
            if len(word) == word_len and int(freq) > 5_200_000:
                words_freq[word] = int(freq)

        # Partition words into difficulty bands based on game_levels
        words: List[str] = list(words_freq.keys())
        break_point: int = len(words) // len(game_levels)
        words_list: List[str] = words[
            (word_level - 1) * break_point : word_level * break_point
        ]

        return random.choice(words_list).upper()
