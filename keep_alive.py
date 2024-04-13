from flask import Flask, send_file
from threading import Thread
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import schedule
import time

app = Flask(__name__)

# Function to authenticate with Google Drive
def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")  # Load credentials from JSON file
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved credentials
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")  # Save credentials back to file
    return GoogleDrive(gauth)

# Function to upload file to Google Drive
def upload_to_google_drive(drive, file_path):
    file_name = os.path.basename(file_path)
    file_list = drive.ListFile({'q': f"title='{file_name}' and trashed=false"}).GetList()
    if file_list:
        for file in file_list:
            file.Delete()
    file = drive.CreateFile({'title': file_name})
    file.SetContentFile(file_path)
    file.Upload()
    print(f"Uploaded {file_name} to Google Drive successfully!")

@app.route('/get_db_file')
def get_db_file():
    db_path = os.path.join(os.getcwd(), 'database', 'list.db')
    if os.path.exists(db_path):
        return send_file(db_path, as_attachment=True)
    else:
        return {"error": "Database file not found"}, 404

def upload_db_to_drive():
    db_path = os.path.join(os.getcwd(), 'database', 'list.db')
    if os.path.exists(db_path):
        drive = authenticate_google_drive()
        upload_to_google_drive(drive, db_path)
    else:
        print("Database file not found. Skipping upload to Google Drive.")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()

    # Schedule upload to Google Drive every 5 minutes
    schedule.every(5).minutes.do(upload_db_to_drive)

    while True:
        schedule.run_pending()
        time.sleep(1)
