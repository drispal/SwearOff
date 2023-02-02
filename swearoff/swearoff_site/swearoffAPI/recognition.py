#SwearOff API V.2

import wave
import json
import os
import sys
import argparse

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
from profanity_check import predict
from . import Word as custom_Word
from django.core.files import File

VERBOSE = True

def AudioConverting(audio_filename):
    wf = wave.open(audio_filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        if VERBOSE : print("Converting Audio file to WAV format mono PCM...")
        sound = AudioSegment.from_wav(audio_filename)
        sound = sound.set_channels(1)
        sound.export("media/converted_temp/audio.wav", format="wav")
        wf = wave.open("media/converted_temp/audio.wav", "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            if VERBOSE : print("Audio converting failed.")
            sys.exit()
        else :
            if VERBOSE : print("Audio converting successed")
    return wf

def Censored(audio_filename, lang, audioModel):
    # Model Loading
    if lang == "en" :
        model_path = "AIModels/vosk-model-en-us-0.42-gigaspeech"
    else :
        model_path = "AIModels/vosk-model-fr-0.22"
    if not os.path.exists(model_path):
        if VERBOSE : print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
        sys.exit()
    if VERBOSE : print(f"Reading your vosk model '{model_path}'...")
    model = Model(model_path)
    if VERBOSE : print(f"'{model_path}' model was successfully read")

    wf = AudioConverting(audio_filename)

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

    #Find swears 
    for word in list_of_Words :
        if predict([word.word]) == 1:
            word.isswear = True
            #print(word.word + " is a swear")

    #Replace bad words
    principal_sound = AudioSegment.from_wav(audio_filename)
    original_replace_sound = AudioSegment.from_wav("media/audio/bip.wav")
    original_replace_sound = original_replace_sound.apply_gain(-7)

    result_sound = principal_sound
    for word in list_of_Words:
        if word.isswear :
            duration = (word.end - word.start) * 1000
            replace_sound = original_replace_sound[0:duration]
            result_sound = result_sound.overlay(replace_sound, position=word.start*1000, gain_during_overlay=-30)
    result_sound.export("media/converted/result.wav", format="wav")

    #Adding to model (to fix) 
    local_file = open('media/converted/result.wav', "rb")
    audioModel.censored_audio.save('result.wav',File(local_file))
    local_file.close()






