import streamlit as st
from MA_api import get_item, get_mp4

st.title("MA Transcriber (BETA)")
id = st.text_input("indtast eller kopier id-nummer fra MA")

# id = "12307995"



item = get_item(id)
mp4 = get_mp4(item)

st.video(mp4)

