import sqlite3

with sqlite3.connect('voicelog.db') as conn:
    cursor = conn.cursor()
    # Create the voice_log table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS voice_log (id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, text TEXT)")


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
    for log in logs:
        print(f'ID: {log[0]}, Date and Time: {log[1]}, Text: {log[2]}')
    return logs


if __name__ == '__main__':
    read_logs()
