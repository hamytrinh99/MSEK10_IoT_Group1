import time
import multiprocessing
import RPi.GPIO as GPIO
from concurrent import futures
from datetime import datetime

import serial

import actions
import config
import voice
import db
from intent_detection import detect

ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0)

busy = False
processing = multiprocessing.Value('i', 0)
listening = False

GPIO.setmode(GPIO.BCM)

GPIO.setup(config.LISTENING_PIN, GPIO.OUT)
GPIO.setup(config.LED_PIN_1, GPIO.OUT)
GPIO.setup(config.LED_PIN_2, GPIO.OUT)

GPIO.output(config.LISTENING_PIN, GPIO.LOW)
GPIO.output(config.LED_PIN_1, GPIO.LOW)
GPIO.output(config.LED_PIN_2, GPIO.LOW)


def activate_speaker():
    command = voice.listen_voice()

    GPIO.output(config.LISTENING_PIN, GPIO.LOW)

    intent_ = 'UNKNOWN'
    param_ = None
    if command:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.insert_log(date_time, command)
        intent_, param_ = detect(command)

    return intent_, param_


executor = futures.ThreadPoolExecutor(max_workers=1)

future = None
print('Smart speaker started.')

try:
    while True:
        if future is not None and future.done():
            intent, param = future.result()
            print('Intent:', intent, 'Param:', param)
            if intent == 'MUSIC_ON':
                actions.play_music()
            elif intent == 'MUSIC_OFF':
                actions.stop_music()
            elif intent == 'LIGHT_ON':
                actions.turn_light_on(param)
            elif intent == 'LIGHT_OFF':
                actions.turn_light_off(param)
            elif intent == 'WEATHER':
                actions.check_weather()
                time.sleep(5)
            elif intent == 'STOP':
                actions.stop_everything()
            else:
                voice.speak('Xin lỗi, em chưa hiểu ạ')
                time.sleep(2)

            if intent != 'STOP' and intent != 'MUSIC_OFF':
                voice.vlc_pause_resume_music(do_pause=False)

            future = None
            busy = False

        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()

            if data == 'trigger' and not busy:
                busy = True

                voice.vlc_stop_sound()
                voice.vlc_pause_resume_music(do_pause=True)

                future = executor.submit(activate_speaker)  # Multithread
finally:
    GPIO.cleanup()
