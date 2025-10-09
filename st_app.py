import streamlit as st

# --- Local utilities ---
from src.utils.call_llama import call_llama_func
from src.utils.aux_funcs import get_color, word_selection
from src.utils.constants import (
    defaults,
    game_levels,
    num_key,
    level_key,
    num_of_letter,
    level_val,
    config_locked,
    examples_html
)


# ---------------------- #
#  Streamlit Page Config #
# ---------------------- #
# Must be called before any other Streamlit commands.
st.set_page_config(
    page_title="My Wordle Game",        # Title shown in browser tab
    page_icon="🎯",                      # Emoji or path to favicon
    layout="wide",                       # "centered" (default) or "wide"
    initial_sidebar_state="expanded",    # "auto", "expanded", or "collapsed"
)

# ---------------------- #
#       Page Header      #
# ---------------------- #
st.header(":zap: Wordle")
st.subheader("Get chances to guess a word.")

# ---------------------- #
#   Sidebar Game Guide   #
# ---------------------- #
st.sidebar.header("📖 Examples")
# HTML snippet with sample gameplay demonstration
st.sidebar.markdown(examples_html, unsafe_allow_html=True) 

# ---------------------- #
#  Initialize Session    #
# ---------------------- #
# Load default values for all expected session_state keys
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def _maybe_lock() -> None:
    """
    Callback to lock the configuration panel.

    This function is triggered whenever the user changes
    either of the selectbox widgets. If both the number of
    letters and the game level are chosen (not "Select..."),
    it stores these selections into the session_state and
    locks the configuration to prevent further changes.
    """
    if st.session_state[num_key] != "Select..." and st.session_state[level_key] != "Select...":
        st.session_state[num_of_letter] = st.session_state[num_key]
        st.session_state[level_val] = st.session_state[level_key]
        st.session_state[config_locked] = True


# ---------------------- #
#   Game Configuration   #
# ---------------------- #
# Collapsible panel for selecting game settings.
with st.expander("Settings", expanded=not st.session_state.config_locked):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Number of letters:",
            ["Select...", "4-letters", "5-letters", "6-letters"],
            key=num_key,
            disabled=st.session_state[config_locked],
            on_change=_maybe_lock,
        )
    with col2:
        st.selectbox(
            "Game Level:",
            ["Select...", "Easy", "Normal", "Hard"],
            key=level_key,
            disabled=st.session_state[config_locked],
            on_change=_maybe_lock,
        )

# ---------------------- #
#    Start the Game      #
# ---------------------- #
if st.session_state[config_locked]:
    # Select the target word once at game start
    if not st.session_state.game_start:
        word_len = int(st.session_state[num_key].split('-')[0])
        word_level = game_levels[st.session_state[level_key]][1]  # difficulty index
        # Randomly pick a word that matches settings
        st.session_state.word_selected = word_selection(
            word_len=word_len,
            word_level=word_level,
            game_levels=game_levels
        )
    target_word: str = st.session_state.word_selected
    st.session_state.game_start = True

    # Game configuration derived from user selection
    number_of_letters: int = int(st.session_state[num_key].split('-')[0])
    number_of_guess: int = game_levels[st.session_state[level_key]][0]

    # Create session grids if not already initialized
    if "guesses" not in st.session_state:
        st.session_state.guesses = [
            ["" for _ in range(number_of_letters)]
            for _ in range(number_of_guess)
        ]
    if "colors" not in st.session_state:
        st.session_state.colors = [
            ["#FFFFFF" for _ in range(number_of_letters)]
            for _ in range(number_of_guess)
        ]

    # ---------------------- #
    #     Game Play Area     #
    # ---------------------- #
    with st.expander(
        "Play The Game",
        expanded=not (st.session_state.game_over or st.session_state.game_win)
    ):
        # Input form appears while the game is ongoing
        if (
            not st.session_state.game_over
            and not st.session_state.game_win
            and st.session_state.current_row < number_of_guess
        ):
            row: int = st.session_state.current_row
            with st.form(key=f"form_{row}", clear_on_submit=True):
                guess: str = st.text_input(
                    f"Guess #{row+1}",
                    max_chars=number_of_letters,
                    disabled=(st.session_state.game_win or st.session_state.game_over)
                ).upper()
                submit: bool = st.form_submit_button("Submit Guess")

                if submit:
                    guess_value: str = guess
                    # Validate guess length and characters
                    if len(guess_value) == number_of_letters and guess_value.isalpha():
                        # Fill the grid with guessed letters and color codes
                        for i, ch in enumerate(guess_value):
                            st.session_state.guesses[row][i] = ch
                            st.session_state.colors[row][i] = get_color(
                                i, ch, target_word
                            )

                        # Check win condition
                        if guess_value == target_word:
                            st.session_state.game_win = True
                            st.success("🎉 Correct!")
                            st.balloons()
                            st.rerun()
                        else:
                            # Move to next row or end game if guesses exhausted
                            st.session_state.current_row += 1
                            if st.session_state.current_row == number_of_guess:
                                st.session_state.game_over = True
                                st.error(f"Game Over! The word was **{target_word}**.")
                            st.rerun()
                    else:
                        st.error("Please enter exactly 5 letters.")

        # ---------------------- #
        #     Render Grid        #
        # ---------------------- #
        # Display the guess grid with colored tiles
        for r in range(number_of_guess):
            cols = st.columns([1] * number_of_letters, gap="small", vertical_alignment="center")
            for c in range(number_of_letters):
                ch: str = st.session_state.guesses[r][c]
                bg: str = st.session_state.colors[r][c]
                cols[c].markdown(
                    f"<div style='background:{bg};width:42px;height:42px;"
                    f"display:flex;align-items:center;justify-content:center;"
                    f"color:white;font-size:22px;font-weight:bold;border-radius:6px;'>"
                    f"{ch}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<br>", unsafe_allow_html=True)

# ---------------------- #
#   End-of-Game States   #
# ---------------------- #
if st.session_state.game_over:
    if not st.session_state.game_win:
        st.error(
            f"""
                Game over!\n
                The word was: {target_word}!\n
                Please reset the game.
            """
        )

if st.session_state.game_win and not st.session_state.balloons_shown:
    # Extra celebration message when the player wins
    st.session_state.game_over = True
    st.success(f"🎉 Congratulations! You guessed the word: {target_word}")
    st.balloons()
    st.session_state.balloons_shown = True

# ---------------------- #
#        Restart         #
# ---------------------- #
# Clears the entire session state and re-runs the script,
# returning to the configuration screen.
if st.button("🔄 Restart"):
    st.session_state.clear()
    st.rerun()