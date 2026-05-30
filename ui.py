import streamlit as st

_HIDE_CHROME_CSS = """
    <style>
    .stDeployButton,
    header[data-testid="stHeader"],
    button[data-testid="manage-app-button"],
    div[data-testid="stViewerConnectionStatus"],
    iframe[title="Manage app"],
    ._terminalButton_rix23_138,
    [data-testid="collapsedControl"],
    .stActionButton {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
    }
    .main .block-container { padding-top: 2rem; }
    </style>
"""

def apply_chrome_hide() -> None:
    st.markdown(_HIDE_CHROME_CSS, unsafe_allow_html=True)
