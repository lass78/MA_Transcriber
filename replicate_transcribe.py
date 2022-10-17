import replicate
model = replicate.models.get("openai/whisper")
output = model.predict(audio=open('inflation2min_l.wav', 'rb'), model='medium')

print(output)

