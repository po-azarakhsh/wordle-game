import random


def get_color(idx, letter, target_word):
    if letter in target_word and letter != target_word[idx]:
        return "#F9DC3C"
    elif letter == target_word[idx]:
        return "#6AAA64"
    else:
        return "#A9A9A9"
    
def word_selection(word_len, word_level, game_levels):
    file_path = 'src/data/words_freq.txt'

    with open(file_path, 'r') as f:
        words_freq = {}
        for line in f:
            word, freq = line.strip().split(',')
            if len(word) == word_len and int(freq) > 5_200_000:
                words_freq[word] = int(freq)
        words = list(words_freq.keys())
        break_point = len(words) // len(game_levels)
        words_list = words[(word_level - 1) * break_point:word_level * break_point]

        return random.choice(words_list).upper()
