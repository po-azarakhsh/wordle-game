import streamlit as st

st.header(":zap: Wordle")
st.subheader("Get chances to guess a word.")

# keys / names
num_key = "num_of_letters_widget"
level_key = "game_level_widget"
config_locked = "config_locked"
num_of_letter = "num_of_letters"
level_val = "game_level"
current_row = "current_row"
game_over = "game_over"
game_win = "game_win"

target_word = "AGAIN"

game_levels = {
    'Easy': 5,
    'Normal': 6,
    'Hard': 7
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
    game_win: False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v



def _maybe_lock():
    """Callback: if both widgets have real choices, lock config and re-run so UI updates immediately."""
    if st.session_state[num_key] != "Select..." and st.session_state[level_key] != "Select...":
        st.session_state[num_of_letter] = st.session_state[num_key]
        st.session_state[level_val] = st.session_state[level_key]
        st.session_state[config_locked] = True
        # st.rerun()  # force immediate UI refresh with disabled widgets

def get_color(idx, letter):
    if letter in target_word and letter != target_word[idx]:
        return "#F9DC3C"
    elif letter == target_word[idx]:
        return "#6AAA64"
    else:
        return "#A9A9A9"


# Expander — collapsed/expanded based on lock state
with st.expander("Configure Your Game", expanded=not st.session_state[config_locked]):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Number of letters:",
            ["Select...", "5-letters", "6-letters", "7-letters"],
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
        


# Use the config when locked
if st.session_state[config_locked]:
    # --- Game session state ---
    number_of_letters = int(st.session_state[num_key].split('-')[0])
    number_of_guess = game_levels[st.session_state[level_key]]
    if "guesses" not in st.session_state:
        st.session_state.guesses = [["" for _ in range(number_of_letters)] for _ in range(number_of_guess)]
    if "colors" not in st.session_state:
        st.session_state.colors = [["#FFFFFF" for _ in range(number_of_letters)] for _ in range(number_of_guess)]
        
    with st.expander(
        "Play The Game",
        expanded=not (st.session_state.game_over or st.session_state.game_win)
    ):
        # --- Input Form ---
        if (
            (not st.session_state.game_over and not st.session_state.game_win)
            and st.session_state.current_row < number_of_guess
        ):
            row = st.session_state.current_row
            with st.form(key=f"form_{row}", clear_on_submit=True):
                guess = st.text_input(f"Guess #{row+1}", max_chars=5).upper()
                submit = st.form_submit_button("Submit Guess")
                if submit:
                    guess_value = guess
                    if len(guess_value) == number_of_letters and guess_value.isalpha():
                        for i, ch in enumerate(guess_value):
                            st.session_state.guesses[row][i] = ch
                            st.session_state.colors[row][i] = get_color(i, ch)

                        if guess_value == target_word:
                            st.session_state.game_win = True
                            st.session_state.game_over = True
                        else:
                            st.session_state.current_row += 1
                            if st.session_state.current_row == number_of_guess:
                                st.session_state.game_over = True
                                st.error(f"Game Over! The word was **{target_word}**.")
                        # ✅ Force a rerun so the next row input appears immediately
                            st.rerun()
                    else:
                        st.error("Please enter exactly 5 letters.")


        # --- Render Grid ---
        for r in range(number_of_guess):
            cols = st.columns([1] * number_of_letters, gap="small")
            for c in range(number_of_letters):
                ch = st.session_state.guesses[r][c]
                bg = st.session_state.colors[r][c]
                cols[c].markdown(
                    f"<div style='background:{bg};width:42px;height:42px;"
                    f"display:flex;align-items:center;justify-content:center;"
                    f"color:white;font-size:22px;font-weight:bold;border-radius:6px;'>"
                    f"{ch}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<br>", unsafe_allow_html=True)


if st.session_state.game_over:
    if not st.session_state.game_win:
        st.error(
            f"""
                Game over!\n
                The word was: {target_word}!\n
                Please reset the game.
            """
            )

if st.session_state.game_win:
    st.session_state[config_locked] = False
    st.success("🎉 Correct!")
    st.balloons()

# Restart: clear widget keys and logical state, then rerun
col1, col2, col3, col4 = st.columns(4)
with col4:
    if st.button("🔄 Restart Game"):
        st.session_state.clear()
        st.rerun()


