# import multiprocessing
import os
import traceback
import uuid
import pickle
import base64
import RPi.GPIO as GPIO

import speech_recognition as sr
import gtts
import vlc
import config

r = sr.Recognizer()
os.makedirs('./tmp', exist_ok=True)

if os.path.exists('voice_cache.pkl'):
    with open('voice_cache.pkl', 'rb') as f:
        cache: dict = pickle.load(f)
else:
    cache = dict()

voice_instance = vlc.Instance()
music_instance = vlc.Instance()

voice_media_player = voice_instance.media_player_new()
music_media_player = music_instance.media_player_new()


def listen_voice():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Listening...')
            GPIO.output(config.LISTENING_PIN, GPIO.HIGH)
            audio_data = r.listen(source, timeout=None)

            print("Recognizing...")
            result = r.recognize_google(audio_data, language='vi', show_all=True)
            print(result)
            if result:
                text = result['alternative'][0]['transcript']
                print(text)
                return text
            return ''
    except Exception:
        traceback.print_exc()
        return ''


def vlc_play_sound(audio_file):
    media = voice_instance.media_new(audio_file)
    voice_media_player.set_media(media)
    voice_media_player.play()


def vlc_play_music(audio_file):
    media = music_instance.media_new(audio_file)
    music_media_player.set_media(media)
    music_media_player.play()


def vlc_stop_sound():
    voice_media_player.stop()


def vlc_stop_music():
    music_media_player.stop()


def vlc_pause_resume_music(do_pause):
    music_media_player.set_pause(do_pause)


def speak(text):
    text = text.lower().strip()
    encoded_text = base64.b64encode(text.encode('utf-8'))

    if encoded_text in cache:
        vlc_play_sound(cache[encoded_text])

    else:
        tts = gtts.gTTS(text, lang='vi')
        sound_path = f'./tmp/{str(uuid.uuid4())}.wav'
        tts.save(sound_path)
        cache[encoded_text] = sound_path
        vlc_play_sound(sound_path)

        print('Saving to cache')
        with open('voice_cache.pkl', 'wb') as fw:
            pickle.dump(cache, fw)
        print('Saved to cache')
