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
    item = get_item(id)
    print(item)
    video_url = get_mp4_url(item)
    print(video_url)

    bytes = get_mp4_as_bytes(video_url)

    print("downloadning")
    # input = ffmpeg.input(bytes)
    
    
    mp_file = VideoFileClip(video_url)
    print('Finished downloadning')
    audio = mp_file.audio
    print (type(audio))
    audio.write_audiofile('test.wav')
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