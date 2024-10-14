import streamlit as st

story_page = st.Page("story_helper.py", title="Create Story", icon=":material/book:")
char_page = st.Page("char_maker.py", title="Character Maker", icon=":material/face:")

pg = st.navigation([story_page, char_page])
st.set_page_config(page_title="DNDBot", page_icon=":material/adb:")
pg.run()