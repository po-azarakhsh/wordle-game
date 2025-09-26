import streamlit as st

st.header(":zap: Wordle")
st.subheader("Get chances to guess a word.")

# keys / names
NUM_KEY = "num_of_letters_widget"
LEVEL_KEY = "game_level_widget"
CONFIG_LOCKED = "config_locked"
NUM_VAL = "num_of_letters"
LEVEL_VAL = "game_level"

# initialize session state
defaults = {
    CONFIG_LOCKED: False,
    NUM_KEY: "Select...",
    LEVEL_KEY: "Select...",
    NUM_VAL: None,
    LEVEL_VAL: None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def _maybe_lock():
    """Callback: if both widgets have real choices, lock config and re-run so UI updates immediately."""
    if st.session_state[NUM_KEY] != "Select..." and st.session_state[LEVEL_KEY] != "Select...":
        st.session_state[NUM_VAL] = st.session_state[NUM_KEY]
        st.session_state[LEVEL_VAL] = st.session_state[LEVEL_KEY]
        st.session_state[CONFIG_LOCKED] = True
        # st.rerun()  # force immediate UI refresh with disabled widgets

# Restart: clear widget keys and logical state, then rerun
col1, col2, col3, col4 = st.columns(4)
with col4:
    if st.button("🔄 Restart Game"):
        st.session_state[CONFIG_LOCKED] = False
        st.session_state[NUM_VAL] = None
        st.session_state[LEVEL_VAL] = None
        st.session_state[NUM_KEY] = "Select..."
        st.session_state[LEVEL_KEY] = "Select..."
        st.rerun()

# Expander — collapsed/expanded based on lock state
with st.expander("Game Configuration", expanded=not st.session_state[CONFIG_LOCKED]):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Number of letters:",
            ["Select...", "5-letters", "6-letters", "7-letters"],
            key=NUM_KEY,
            disabled=st.session_state[CONFIG_LOCKED],
            on_change=_maybe_lock,
        )
    with col2:
        st.selectbox(
            "Game Level:",
            ["Select...", "Easy", "Normal", "Hard"],
            key=LEVEL_KEY,
            disabled=st.session_state[CONFIG_LOCKED],
            on_change=_maybe_lock,
        )

# Use the config when locked
if st.session_state[CONFIG_LOCKED]:
    st.badge("New")
    st.badge("Success", icon=":material/check:", color="green")

    st.markdown(
        ":violet-badge[:material/star: Favorite] :orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
    )


