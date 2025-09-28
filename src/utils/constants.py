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

examples_html = """
<style>
    .word-row {
        display: flex;
        gap: 4px;
        margin-bottom: 4px;
    }
    .tile {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        color: white;
        border: 2px solid #000;
    }
    .green { background-color: #6aaa64; }
    .yellow { background-color: #c9b458; }
    .grey { background-color: #787c7e; }
    .black { background-color: #121213; color: white; }
</style>

<!-- Example 1 -->
<div class="word-row">
    <div class="tile green">W</div>
    <div class="tile black">O</div>
    <div class="tile black">R</div>
    <div class="tile black">D</div>
    <div class="tile black">Y</div>
</div>
<p>W is in the word and in the correct spot.</p>

<!-- Example 2 -->
<div class="word-row">
    <div class="tile black">L</div>
    <div class="tile yellow">I</div>
    <div class="tile black">G</div>
    <div class="tile black">H</div>
    <div class="tile black">T</div>
</div>
<p>I is in the word but in the wrong spot.</p>

<!-- Example 3 -->
<div class="word-row">
    <div class="tile black">R</div>
    <div class="tile black">O</div>
    <div class="tile grey">U</div>
    <div class="tile black">G</div>
    <div class="tile black">E</div>
</div>
<p>U is not in the word in any spot.</p>
"""

