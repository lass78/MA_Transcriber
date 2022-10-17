from google.cloud import speech_v1 as speech
from google.cloud import storage

def speech_to_text(config, audio):
    client = speech.SpeechClient()
    response = client.long_running_recognize(config=config, audio=audio)
    print_sentences(response)



def print_sentences(operation):
    print("Waiting for operation to complete...")
    response = operation.result(timeout=7)
    for result in response.results:
        print(result)
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print(f"Transcript: {transcript}")
        print(f"Confidence: {confidence:.0%}")

        print (best_alternative.words)

        for word_info in best_alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )






if __name__ == '__main__':
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("matranscriberaudiobucket")
    blob = bucket.blob("tmp.wav")
    blob.upload_from_filename('test_l.wav')

    config = dict(language_code="da-DK", enable_word_time_offsets=True)
    audio = dict(uri="gs://matranscriberaudiobucket/tmp.wav")




    speech_to_text(config, audio)