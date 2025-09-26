from src.utils.wordle import Wordle


file_path = 'src/data/words_freq.txt'
word_len = 5
limit = 10000

wordle = Wordle(file_path=file_path, limit = 1000)

wordle.run()