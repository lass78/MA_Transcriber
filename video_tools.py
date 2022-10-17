import ffmpeg
from MA_api import get_item, get_mp4_url, get_mp4_as_bytes
import sys
from moviepy.editor import VideoFileClip


class VideoConvert:
    def __init__(self, videofile):
        self.videofile = videofile
        self.input = ffmpeg.input(videofile)

    def get_audio(self, format='wav'):
        audio = self.input.audio
        # out = ffmpeg.output(audio, 'test.wav').run()
        out = ffmpeg.output(self.input, 'test.wav', format='s16le', acodec='pcm_s16le', ac=1, ar='16k').overwrite_output().run(capture_stdout=True, capture_stderr=True)

def decode_audio(in_filename, **input_kwargs):
    try:
        out, err = (ffmpeg
            .input(in_filename, **input_kwargs)
            .output('test2.wav', format='wav')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    return out



if __name__ == "__main__":
    id = "12309293" # brian vad kort
    # id = "12309875" # brian vad 1min
    # id = "12369861" # inflationsekspert 2min
    # id = "12369862" # indlationsekspert 10min
    # id = "12368871" # elise rimpler 16min
    id = "12370323" #russian voxpops
    id = "12370245" # venezuela flood
    item = get_item(id)
    print(item['itm_title'])
    video_url = get_mp4_url(item)
    print(video_url)

    print("downloadning")
    # bytes = get_mp4_as_bytes(video_url)
    mp_file = VideoFileClip(video_url)
    # mp_file.write_videofile("large/" + item['itm_title'] + ".mp4")
    print('Finished downloadning')
    

    audio = mp_file.audio
    print (audio)
    audio.write_audiofile(item['itm_title'] + '_l.mp3', ffmpeg_params=['-map_channel', '0.0.0'])
    audio.write_audiofile(item['itm_title'] +'_r.mp3', ffmpeg_params=['-map_channel', '0.0.1'])

    # print (input.audio)
     
    # v = VideoConvert(input)
    # v.get_audio()
    
    # v = decode_audio('nick_kort.mxf')
    # 'nick_lang.mxf'

    # print (type(a))
    # print(a)
    # play(a)

    # sound = AudioSegment.from_wav('myfile.wav')
    # play(sound)