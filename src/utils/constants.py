num_key = "num_of_letters_widget"
level_key = "game_level_widget"
config_locked = "config_locked"
num_of_letter = "num_of_letters"
level_val = "game_level"
current_row = "current_row"
game_over = "game_over"
game_win = "game_win"
game_start = "game_start"
word_selected = ""
balloons_shown = "balloons_shown"


game_levels = {
    'Easy': [5, 1],
    'Normal': [6, 2],
    'Hard': [7, 3]
}

# initialize config session state
defaults = {
    config_locked: False,
    num_key: "Select...",
    level_key: "Select...",
    num_of_letter: None,
    level_val: None,
    current_row: 0,
    game_over: False,
    game_win: False,
    game_start: False,
    word_selected: '',
    balloons_shown: False
}

