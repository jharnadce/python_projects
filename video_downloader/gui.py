from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *
import shutil

# https://www.youtube.com/watch?v=3CFoZl0T3GQ
def download():
    filepath = filepath_label.cget("text")
    video_path = download_entry.get()
    print("Downloading...")
    # Download the video in highest resolution so that we get both video and audio
    mp4 = YouTube(video_path).streams.get_highest_resolution().download()
    
    # Convert the mp4 file into Video File
    video_clip = VideoFileClip(mp4)
    # Convert to mp3 (audio only)
    audio_file = video_clip.audio
    audio_file.write_audiofile('audio.mp3')
    audio_file.close()
    shutil.move('audio.mp3', filepath)
    video_clip.close()

    # Move from current location to the user given path
    shutil.move(mp4, filepath)
    pass

def filepath():
    filepath = filedialog.askdirectory()
    filepath_label.config(text=filepath)

app = Tk()
app.title("Video Downloader")
canvas = Canvas(app, width=400, height=300)
canvas.pack()

title = Label(app, text="Video Downloader app", 
              fg='blue', font=("Arial", 20))

download_label = Label(app, text="Enter the video URL")
download_entry = Entry(app)
filepath_label = Label(app, text="Path for downloaded file")
filepath_button = Button(app, text="Select", command=filepath)
download_button = Button(app, text="Download", command=download)

canvas.create_window(200, 30, window=title)
canvas.create_window(200, 90, window=download_label)
canvas.create_window(200, 110, window=download_entry)
canvas.create_window(200, 140, window=filepath_label)
canvas.create_window(200, 180, window=filepath_button)
canvas.create_window(200, 250, window=download_button)


app.mainloop()