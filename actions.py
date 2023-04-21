import os
import random
import traceback

import RPi.GPIO as GPIO

import requests

import config
import db
import voice


def play_music():
    files = os.listdir('./music')
    music_files = [f for f in files if f.endswith('.wav')]
    random_file = random.choice(music_files)
    voice.vlc_play_music(f'./music/{random_file}')


def stop_music():
    voice.vlc_stop_music()


def turn_light_on(room):
    if not room:
        GPIO.output(config.LED_PIN_1, GPIO.HIGH)
        GPIO.output(config.LED_PIN_2, GPIO.HIGH)
        voice.speak('Vâng, em bật đèn rồi ạ')
        db.upsert_led_status(1, 1)
    elif room == 'ngủ':
        GPIO.output(config.LED_PIN_1, GPIO.HIGH)
        voice.speak('Vâng, em bật đèn phòng ngủ rồi ạ')
        db.update_single_led(1, 1)
    else:
        GPIO.output(config.LED_PIN_2, GPIO.HIGH)
        voice.speak('Vâng, em bật đèn phòng khách rồi ạ')
        db.update_single_led(2, 1)


def turn_light_off(room):
    if not room:
        GPIO.output(config.LED_PIN_1, GPIO.LOW)
        GPIO.output(config.LED_PIN_2, GPIO.LOW)
        voice.speak('Vâng, em tắt đèn rồi ạ')
        db.upsert_led_status(0, 0)
    elif room == 'ngủ':
        GPIO.output(config.LED_PIN_1, GPIO.LOW)
        voice.speak('Vâng, em tắt đèn phòng ngủ rồi ạ')
        db.update_single_led(1, 0)
    else:
        GPIO.output(config.LED_PIN_2, GPIO.LOW)
        voice.speak('Vâng, em tắt đèn phòng khách rồi ạ')
        db.update_single_led(2, 0)


def check_weather():
    try:
        api_key = '27686fa785bc572074f288438638365e'
        city = 'Hanoi'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=vi'
        response = requests.get(url)
        weather_data = response.json()

        city_name = weather_data["name"]
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

        text = f"Nhiệt độ ở {city_name} là {temp} độ C. Thời tiết {description}. Độ ẩm là {humidity} phần trăm."
        voice.speak(text)
    except:
        traceback.print_exc()
        voice.speak('Hic em không lấy được thông tin thời tiết ạ')


def stop_everything():
    voice.vlc_stop_music()
    voice.vlc_stop_sound()
