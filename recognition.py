
#SwearOff API V.1

import wave
import json
import os
import sys
import argparse

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
from profanity_check import predict
import Word as custom_Word

# # Reading script arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-l", "--lang", help="language to recognise (en or fr, default is Fr)")
argParser.add_argument("-f", "--file", help="audio file to process (no file means no process)")
args = argParser.parse_args()
if args.lang == "en" :
    model_path = "vosk-model-en-us-0.42-gigaspeech"
else :
    model_path = "vosk-model-fr-0.22"
if args.file == None :
    print("No audio file provided")
    sys.exit()
else :
    audio_filename = args.file

# Audio file conversion
wf = wave.open(audio_filename, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Converting Audio file to WAV format mono PCM...")
    sound = AudioSegment.from_wav(audio_filename)
    sound = sound.set_channels(1)
    sound.export("converted_temp/audio.wav", format="wav")
    wf = wave.open("converted_temp/audio.wav", "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio converting failed.")
        sys.exit()
    else :
        print("Audio converting successed")

# Model Loading
if not os.path.exists(model_path):
    print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
    sys.exit()

print(f"Reading your vosk model '{model_path}'...")
model = Model(model_path)
print(f"'{model_path}' model was successfully read")

# Recognition text
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

wf.close()  # close audiofile

# convert list of JSON dictionaries to list of 'Word' objects
list_of_Words = []
for sentence in results:
    if len(sentence) == 1:
        # sometimes there are bugs in recognition 
        # and it returns an empty dictionary
        # {'text': ''}
        continue
    for obj in sentence['result']:
        w = custom_Word.Word(obj)  # create custom Word object
        list_of_Words.append(w)  # and add it to list

# output to the screen
#for word in list_of_Words:
#    print(word.to_string())

#Find swears 
for word in list_of_Words :
    if predict([word.word]) == 1:
        word.isswear = True
        #print(word.word + " is a swear")

#Replace bad words
principal_sound = AudioSegment.from_wav(audio_filename)
original_replace_sound = AudioSegment.from_wav("bip.wav")
original_replace_sound = original_replace_sound.apply_gain(-7)

result_sound = principal_sound
for word in list_of_Words:
    if word.isswear :
        duration = (word.end - word.start) * 1000
        replace_sound = original_replace_sound[0:duration]
        result_sound = result_sound.overlay(replace_sound, position=word.start*1000, gain_during_overlay=-30)
result_sound.export("result.wav", format="wav")