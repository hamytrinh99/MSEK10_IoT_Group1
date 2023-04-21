import streamlit as st

import RPi.GPIO as GPIO

import config
import db

st.title('Smartspeaker dashboard')


@st.cache
def init():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(config.LED_PIN_1, GPIO.OUT)
    GPIO.setup(config.LED_PIN_2, GPIO.OUT)


init()

led_1_on, led_2_on = db.get_led_status()


def toggle_led_1():
    global led_1_on
    led_1_on = 1 - led_1_on

    if led_1_on:
        GPIO.output(config.LED_PIN_1, GPIO.HIGH)
    else:
        GPIO.output(config.LED_PIN_1, GPIO.LOW)
    db.upsert_led_status(led_1_on, led_2_on)


def toggle_led_2():
    global led_2_on
    led_2_on = 1 - led_2_on
    if led_2_on:
        GPIO.output(config.LED_PIN_2, GPIO.HIGH)
    else:
        GPIO.output(config.LED_PIN_2, GPIO.LOW)
    db.upsert_led_status(led_1_on, led_2_on)


st.subheader('Điều khiển đèn')
checkbox1 = st.checkbox('Đèn phòng ngủ', value=led_1_on, on_change=toggle_led_1)
checkbox2 = st.checkbox('Đèn phòng khách', value=led_2_on, on_change=toggle_led_2)

st.subheader('Lịch sử giọng nói')

cols = st.beta_columns((1, 3))
for dt, text in db.read_logs():
    cols[0].write(dt.strip())
    cols[1].write(text.strip())
