import sqlite3


def init():
    with sqlite3.connect('smartspeaker.db') as conn:
        cursor = conn.cursor()
        # Create the voice_log table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS voice_log "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, text TEXT)")

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS led_status '
            '(id INTEGER PRIMARY KEY, led1_status INTEGER NOT NULL, led2_status INTEGER NOT NULL)')

        conn.commit()


# Function to insert a voice log into the database
def insert_log(date_time, text):
    with sqlite3.connect('voicelog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO voice_log (date_time, text) VALUES (?, ?)", (date_time, text))
        conn.commit()


# Function to read voice logs from the database
def read_logs():
    with sqlite3.connect('voicelog.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM voice_log")
        logs = cursor.fetchall()
    res = []
    for log in logs:
        if log[2].strip():
            res.append([log[1].strip(), log[2].strip()])
    res = res[::-1]
    return res[:min(10, len(res))]


def upsert_led_status(led1_status, led2_status):
    with sqlite3.connect('smartspeaker.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO led_status (id, led1_status, led2_status)
                          VALUES (1, ?, ?)''', (led1_status, led2_status))
        conn.commit()


def update_single_led(led_number, led_status):
    with sqlite3.connect('smartspeaker.db') as conn:
        cursor = conn.cursor()
        if led_number == 1:
            cursor.execute('''UPDATE led_status SET led1_status = ? WHERE id = 1''', (led_status,))
        elif led_number == 2:
            cursor.execute('''UPDATE led_status SET led2_status = ? WHERE id = 1''', (led_status,))
        else:
            print("Invalid LED number. Use 1 or 2.")
            return
        conn.commit()


def get_led_status():
    with sqlite3.connect('smartspeaker.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT led1_status, led2_status FROM led_status WHERE id = 1')
        led_status = cursor.fetchone()
        return led_status[0], led_status[1]


init()
upsert_led_status(0, 0)
