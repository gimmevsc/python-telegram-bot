from flask import Flask, send_file
from threading import Thread
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"

# Function to download list.db file from the server database folder to the desktop
def download_list_db():
    db_path = os.path.join(os.getcwd(), 'database', 'list.db')
    if os.path.exists(db_path):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        destination_path = os.path.join(desktop_path, 'list.db')
        os.replace(db_path, destination_path)
        print("list.db downloaded successfully to Desktop")
    else:
        print("Database file not found")

# Main function to download list.db every 1 minute
def main():
    while True:
        download_list_db()
        time.sleep(60)  # Wait for 1 minute before downloading again

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    main()
