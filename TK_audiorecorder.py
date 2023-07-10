# MP3 Streams for testing : https://wiki.ubuntuusers.de/Internetradio/Stationen/

import tkinter as tk
from tkinter import ttk
import requests
import subprocess
import threading
import time


def download_and_convert(url, filename):
    response = requests.get(url, stream=True)

    # Create a unique identifier for the temporary file
    unique_id = int(time.time())

    # Save the downloaded audio as a temporary file with a unique id-number
    temp_audio_file_name = f'temp_audio_{unique_id}'
    with open(temp_audio_file_name, 'wb') as temp_audio_file:
        for chunk in response.iter_content(chunk_size=8192):
            temp_audio_file.write(chunk)

    # Use FFmpeg to convert the audio to mp3
    subprocess.run(['ffmpeg', '-y', '-i', temp_audio_file_name, f'{filename}_{unique_id}.mp3'])


# Function to start the recording process in a separate thread
def record():
    url = url_entry.get()
    filename = filename_entry.get()
    duration = duration_entry.get()

    # Start the recording process in a separate thread
    threading.Thread(target=download_and_convert, args=(url, filename)).start()

    # Add the recording to the table
    table.insert('', 'end', values=(filename, url, duration))


# Create the main Tkinter window
root = tk.Tk()
root.title("Audio Recorder")

# Create input fields for URL, filename, and duration
url_label = tk.Label(root, text="Stream URL:")
url_label.grid(column=0, row=0)
url_entry = tk.Entry(root, width=50)
url_entry.grid(column=1, row=0)

filename_label = tk.Label(root, text="Filename:")
filename_label.grid(column=0, row=1)
filename_entry = tk.Entry(root, width=50)
filename_entry.grid(column=1, row=1)

duration_label = tk.Label(root, text="Duration (s):")
duration_label.grid(column=0, row=2)
duration_entry = tk.Entry(root, width=50)
duration_entry.grid(column=1, row=2)

# Create the Record button
record_button = tk.Button(root, text="Record", command=record)
record_button.grid(column=1, row=3)

# Create a table to display previous recordings
table = ttk.Treeview(root, columns=("Filename", "URL", "Duration"), show="headings")
table.heading("Filename", text="Filename")
table.heading("URL", text="URL")
table.heading("Duration", text="Duration")
table.grid(column=0, row=4, columnspan=2)

# Run the Tkinter main loop
root.mainloop()
