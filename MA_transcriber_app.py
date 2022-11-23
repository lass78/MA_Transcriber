import streamlit as st
from MA_api import get_item, get_mp4_url
from moviepy.editor import VideoFileClip
from whisper_transcribe import get_transcription

if 'transcription_selected' not in st.session_state:
    st.session_state.transcription_selected = False
    st.session_state.transcription = []

if 'MA_id_OK' not in st.session_state:
    st.session_state.MA_id_OK = False

st.title("MA Transcriber (BETA)")

id = "12307995"
id = st.text_input("indtast eller kopier id-nummer fra MA")

def trans():
    st.session_state.transcription_selected = True
    with st.spinner('extracting audio'):
        st.write()
        audio = VideoFileClip(mp4).audio
        audio.write_audiofile('tmp.mp3')
    with st.spinner('getting transcription'):
        result = get_transcription('tmp.mp3', 'da')

    for segment in result['segments']:
        start_min = int(segment['start']/60)
        start_sec = int(segment['start'] % 60)
        end_min = int(segment['end']/60)
        end_sec = int(segment['end'] % 60)
       

        st.write (str(start_min).zfill(2), ':', str(start_sec).zfill(2), " - ", str(end_min).zfill(2), ":",str(end_sec).zfill(2), "  |   ", segment['text'])    


try:
    item = get_item(id)
    mp4 = get_mp4_url(item)
    st.session_state.MA_id_OK = True

except KeyError as e:
    st.warning('Mangler et gyldigt MA-id')
    st.session_state.MA_id_OK = False


print (item)


if st.session_state.MA_id_OK:
    st.video(mp4)

st.button(label='transkriber', on_click=trans)


