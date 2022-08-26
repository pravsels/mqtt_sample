#!/usr/bin/env python3
import pyttsx3

tts_volume = 75

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    engine.setProperty('voice', voice.id)
    engine.say("Congratulations! You have successfully helped your friend escape the virtual world.", volume=tts_volume)
    engine.say("Remember to never tresspass in Anthony's room again!", volume=tts_volume)

engine.runAndWait()
