from io import BytesIO
import base64
import banana_dev as banana
import os

apikey = os.environ["BANANA_API_KEY"]
modelkey = os.environ["BANANA_MODEL_KEY"]

def get_transcription(filename, language=None, task=None):

#Needs test.mp3 file in directory
    with open(filename,'rb') as file:
        mp3bytes = BytesIO(file.read())
    mp3 = base64.b64encode(mp3bytes.getvalue()).decode("ISO-8859-1")
    model_payload = {"mp3BytesString":mp3, 'language':language, 'task':task}


    result = banana.run(apikey, modelkey, model_payload)['modelOutputs'][0]

    return result
    