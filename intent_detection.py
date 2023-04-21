import re
import traceback

music_on_intent = r'(?:mở|bật|phát).*(?:nhạc|bài)'
music_off_intent = r'(?:tắt|dừng|rừng).*(?:nhạc|bài)'
light_on_intent = r'(?:mở|bật).*(?:đèn|bóng|điện)'
light_off_intent = r'tắt.*(?:đèn|bóng|điện)'
light_on_room_intent = r'(?:mở|bật).*(?:đèn|bóng|điện).*?(ngủ|khách)'
light_off_room_intent = r'tắt.*(?:đèn|bóng|điện).*?(ngủ|khách)'
weather_intent = r'thời tiết'
stop_intent = r'(?:[dr]ừng|im|câm|trật tự|tắt)'

intent_list = [music_on_intent, music_off_intent, light_on_room_intent, light_off_room_intent,
               light_on_intent, light_off_intent, weather_intent, stop_intent]
intent_key = ['MUSIC_ON', 'MUSIC_OFF', 'LIGHT_ON',
              'LIGHT_OFF', 'LIGHT_ON', 'LIGHT_OFF', 'WEATHER', 'STOP']


def detect(command: str):
    command = command.lower()
    print(f'Detecting intention... (text = {command})')
    matches = []
    for intent in intent_list:
        m = re.search(intent, command)
        matches.append(m)

    start = 1e9
    intent = 'UNKNOWN'  # Default intent
    param = None

    for i in range(len(matches)):
        if matches[i]:
            if matches[i].start() < start:
                start = matches[i].start()
                intent = intent_key[i]
                try:
                    param = matches[i].group(1)
                except IndexError:
                    pass
                except Exception:
                    traceback.print_exc()
    return intent, param


if __name__ == '__main__':
    command_list = [
        'em ơi Bật đèn lên đi',
        'bật cho anh bóng điện ở phòng ngủ của anh',
        'tắt đèn đi',
        'tắt đèn phòng khách',
        'mở nhạc nghe cho vui',
        'tắt bài hát này đi',
        'thời tiết hôm nay như nào nhỉ',
        'trật tự'
    ]

    for c in command_list:
        print(detect(c))
