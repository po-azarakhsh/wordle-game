import random

from src.utils.print_func import print_success, print_error, print_warning, print_wrong


random.seed(47)


class Wordle:
    def __init__(self, file_path: str, word_len: int = 5, limit: int = 10_000):
        self.word_len = word_len
        self.words = self.generate_word_frequency(file_path, word_len, limit)


    def generate_word_frequency(self, file_path: str, word_len: int, limit: int):
        with open(file_path, 'r') as f:
            words_freq = {}
            cnt = 0
            for line in f:
                word, freq = line.strip().split(',')
                if len(word) == word_len and cnt < limit:
                    words_freq[word] = int(freq)
                    cnt += 1
            
            words_list = list(words_freq.keys())
        
        return words_list
    

    def run(self):
        guess_times = 6
        success = False

        word_selected = random.choice(self.words)
        word_selected = word_selected.upper()
        
        while guess_times:
            word_guessed = input(f"Enter your guess (a {self.word_len} letters word): ")
            word_guessed = word_guessed.upper()

            if word_guessed.lower() == 'quit':
                print_error('See you later!')

            if len(word_guessed) != 5:
                raise Exception(f'Your guess must be a {self.word_len} letter word.')
            
            elif word_guessed == word_selected:
                print_success(f'Congratulation! The word was "{word_selected}.')
                success = True
                break

            if word_guessed.lower() not in self.words:
                print_warning('Word is not valid!')
                continue           


            else:
                for g_letter, w_letter in zip(word_guessed, word_selected):
                    if w_letter == g_letter:
                        print_success(g_letter)
                    elif g_letter in word_selected:
                        print_warning(g_letter)
                    else:
                        print_wrong(g_letter)

            print()
            guess_times -= 1

        if not success:
            print()
            print_warning(f'GAME OVER! The word was "{word_selected}"')


if __name__ == '__main__':
    wordle = Wordle()
    wordle.run()



