import streamlit as st


from src.utils.aux_funcs import get_color, word_selection
from src.utils.constants import (
    defaults,
    game_levels,
    num_key,
    level_key,
    num_of_letter,
    level_val,
    config_locked
)

st.header(":zap: Wordle")
st.subheader("Get chances to guess a word.")

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def _maybe_lock():
    """Callback: if both widgets have real choices, lock config and re-run so UI updates immediately."""
    if st.session_state[num_key] != "Select..." and st.session_state[level_key] != "Select...":
        st.session_state[num_of_letter] = st.session_state[num_key]
        st.session_state[level_val] = st.session_state[level_key]
        st.session_state[config_locked] = True

        

# Expander — collapsed/expanded based on lock state
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

# Use the config when locked
if st.session_state[config_locked]:
    # --- Select the target word randomly ---
    if not st.session_state.game_start:
        word_len = int(st.session_state[num_key].split('-')[0])
        word_level = game_levels[st.session_state[level_key]][1]
        st.session_state.word_selected = word_selection(word_len=word_len, word_level=word_level, game_levels=game_levels)
    target_word = st.session_state.word_selected
    st.session_state.game_start = True
    st.write(target_word)


    # --- Game session state ---
    number_of_letters = int(st.session_state[num_key].split('-')[0])
    number_of_guess = game_levels[st.session_state[level_key]][0]
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
            with st.form(
                key=f"form_{row}",
                clear_on_submit=True,
            ):
                guess = st.text_input(
                    f"Guess #{row+1}",
                    max_chars=number_of_letters,
                    disabled=(st.session_state.game_win or st.session_state.game_over)
                ).upper()
                submit = st.form_submit_button("Submit Guess")
                if submit:
                    guess_value = guess
                    if len(guess_value) == number_of_letters and guess_value.isalpha():
                        for i, ch in enumerate(guess_value):
                            st.session_state.guesses[row][i] = ch
                            st.session_state.colors[row][i] = get_color(i, ch, target_word)

                        if guess_value == target_word:
                            st.session_state.game_win = True
                            st.success("🎉 Correct!")
                            st.balloons()
                            st.rerun()
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
            cols = st.columns([1] * number_of_letters, gap="small", vertical_alignment="center")
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

if st.session_state.game_win and not st.session_state.balloons_shown:
    st.session_state.game_over = True
    st.success(f"🎉 Congratulations! You guessed the word: {target_word}")
    st.balloons()
    st.session_state.balloons_shown = True

# Restart: clear widget keys and logical state, then rerun
col1, col2, col3, col4 = st.columns(4)
with col4:
    if st.button("🔄 Restart Game"):
        st.session_state.clear()
        st.rerun()


