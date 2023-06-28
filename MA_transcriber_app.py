import streamlit as st
from MA_api import get_item, get_mp4_url, get_mp3_url
from moviepy.editor import VideoFileClip, AudioFileClip
from whisper_transcribe import get_transcription
from whisper.tokenizer import LANGUAGES
from utils import sec_to_hhmmss, hhmmss_to_sec
import codecs


# get the supported languages from whisper. Reverse keys and items to make the "human friendly" versions keys and codes the values of the dict. Dict is
# sorted in the proces to make the list more user friendly

languages = dict(sorted({v: k for k, v in LANGUAGES.items()}.items()))
languages['Automatisk'] = None # add the option of language=None for automatic detection of language

# initializations
if 'mp3' not in st.session_state:
    st.session_state.mp3 = None

if 'mp4' not in st.session_state:
    st.session_state.mp4 = None

if 'transcription_selected' not in st.session_state:
    st.session_state.transcription_selected = False
    st.session_state.transcript = None

if 'MA_id_OK' not in st.session_state:
    st.session_state.MA_id_OK = False

if 'transcript' not in st.session_state:
    st.session_state.transcript = None
st.title("MA Transcriber (BETA)")

# if 'in_time' not in st.session_state: st.session_state.in_time = 0
# if 'out_time' not in st.session_state: st.session_state.out_time = -1 

id = st.text_input("indtast eller kopier id-nummer fra MA")


def trans():
    st.session_state.transcription_selected = True
    with st.spinner('extracting audio'):
        st.write()
        if st.session_state.mp3 != None:
            audio = AudioFileClip(st.session_state.mp3).subclip((st.session_state.in_hour, st.session_state.in_minute, st.session_state.in_second), (st.session_state.out_hour, st.session_state.out_minute, st.session_state.out_second))
        else:
            audio = VideoFileClip(st.session_state.mp4).audio.subclip((st.session_state.in_hour, st.session_state.in_minute, st.session_state.in_second), (st.session_state.out_hour, st.session_state.out_minute, st.session_state.out_second))
        audio.write_audiofile('tmp.mp3')
    with st.spinner('getting transcription'):
        result = get_transcription('tmp.mp3', st.session_state.language, st.session_state.task)
    st.session_state.transcript = result

def print_transcript(result):
    
    if result != None:
        lines = []
        offset = hhmmss_to_sec(st.session_state.in_hour, st.session_state.in_minute, st.session_state.in_second)
        for segment in result['segments']:
            start_hour, start_min, start_sec = sec_to_hhmmss(segment['start']+offset)
            end_hour, end_min, end_sec = sec_to_hhmmss(segment['end']+offset)

            string = str(start_hour).zfill(2) + ':' + str(start_min).zfill(2) + ':' + str(start_sec).zfill(2) + " - "+ str(end_hour).zfill(2) + ":" + str(end_min).zfill(2) + ":" + str(end_sec).zfill(2) + "  |   " + segment['text'] + "\n"
            lines.append(string)
            st.write (str(start_hour).zfill(2), ':', str(start_min).zfill(2), ':', str(start_sec).zfill(2), " - ",str(end_hour).zfill(2), ":", str(end_min).zfill(2), ":",str(end_sec).zfill(2), "  |   ", segment['text'])

        filename = "transcripts/"+id+ ".txt"
        with codecs.open(filename, "w", "utf-8") as f:
            for line in lines:
                f.write(line)

    else:
        st.write('No Transcript')


try:
    item = get_item(id)
    st.session_state.mp3 = get_mp3_url(item)
    st.session_state.mp4 = get_mp4_url(item)
    st.session_state.MA_id_OK = True
    st.session_state.old_id = id

except KeyError as e:
    st.warning('Mangler et gyldigt MA-id')
    st.session_state.MA_id_OK = False

except ConnectionError as e:
    st.warning("FEJL: Kan ikke ikke komme i kontakt med MedieArkivet")
    st.session_state.MA_id_OK = False

print (item)

duration_hours = 0
duration_minutes = 0
duration_seconds = 0
if st.session_state.MA_id_OK:
    
    if st.session_state.mp4 != None:
        clip = VideoFileClip(st.session_state.mp4)
        st.video(st.session_state.mp4)
    elif st.session_state.mp3 != None:
        clip = AudioFileClip(st.session_state.mp3)
        st.audio(st.session_state.mp3)
    duration_hours = int(clip.duration / (60*60))
    duration_minutes = int((clip.duration - duration_hours*3600)/60)
    duration_seconds = int((clip.duration - (duration_hours * 3600 + duration_minutes * 60)))

col1, col2 = st.columns(2)


st.write('Indtid')
col11, col12, col13 = st.columns(3)
with col11:
    st.session_state.in_hour = st.number_input('Timer', min_value=0, max_value=59, step=1, value=0, key="ih")
with col12:
    st.session_state.in_minute = st.number_input('Minutter', min_value=0, max_value=59, step=1, value=0, key="im")
with col13:
    st.session_state.in_second = st.number_input('Sekunder', min_value=0, max_value=59, step=1, value=0, key="is")

    # st.session_state.in_time = st.text_input("Starttid", help="Indtast tidskode som mm:ss", on_change=check_value)


st.write('Udtid')
col21, col22, col23 = st.columns(3)

with col21:
    st.session_state.out_hour = st.number_input('Timer', min_value=0, max_value=59, step=1, value=duration_hours, key="oh")
with col22:
    st.session_state.out_minute = st.number_input('Minutter', min_value=0, max_value=59, step=1, key="om", value=duration_minutes)
with col23:
    st.session_state.out_second = st.number_input('Sekunder', min_value=0, step=1, key="os", value = duration_seconds)


    #st.session_state.out_time = st.text_input("Sluttid", help="Indtast tidskode som mm:ss")

with col1:
    st.session_state.task = st.radio("Skal det transcriberes eller oversættes?", options = ['transcribe', 'translate'])

with col2:
    st.session_state.language = languages[st.selectbox("Vælg sprog", options = languages.keys(), index=(len(languages)-1))]

st.button(label='Sæt igang!', on_click=trans)

print_transcript(st.session_state.transcript)

