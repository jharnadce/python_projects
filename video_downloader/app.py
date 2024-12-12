from tkinter import Tk, Canvas, Entry, Label, Button, filedialog
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip

class VideoHandler:
    @staticmethod
    def download_video(video_url, target_path):
        """
        Download the video, convert it to audio, and save to the target path.

        Args:
            video_url (str): The URL of the YouTube video.
            target_path (str): The directory where the downloaded files will be saved.

        Raises:
            RuntimeError: If an error occurs during the download or conversion process.
        """
        """Download the video, convert it to audio, and save to the target path."""
        try:
            print("Downloading video...")
            # Get the video file
            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()
            video_file_path = video_stream.download()

            # Convert to audio
            print("Converting to audio")
            video_clip = VideoFileClip(video_file_path)
            audio_file_path = "audio.mp3"
            video_clip.audio.write_audiofile(audio_file_path)
            video_clip.audio.close()
            video_clip.close()

            # Save the files at target path
            shutil.move(audio_file_path, target_path)
            shutil.move(video_file_path, target_path)

            print("Download and conversion completed!")
        except Exception as e:
            raise RuntimeError(f"An error occurred during video processing: {e}")
        
class VideoDownloaderApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("Video Downloader")

        # GUI setup
        self.setup_gui()
        # To store the user-selected file path
        self.filepath = "" 

    def setup_gui(self):
        """Set up the GUI components"""
        self.canvas = Canvas(self.app, width=400, height=300)
        self.canvas.pack()

        self.title = Label(self.app, text="Video Downloader app", 
              fg='blue', font=("Arial", 20))

        self.download_label = Label(self.app, text="Enter the video URL")
        self.download_entry = Entry(self.app)
        self.filepath_label = Label(self.app, text="Path for downloaded file")
        self.filepath_button = Button(self.app, text="Select", command=self.select_filepath)
        self.download_button = Button(self.app, text="Download", command=self.handle_download)

        self.canvas.create_window(200, 30, window=self.title)
        self.canvas.create_window(200, 90, window=self.download_label)
        self.canvas.create_window(200, 110, window=self.download_entry)
        self.canvas.create_window(200, 140, window=self.filepath_label)
        self.canvas.create_window(200, 180, window=self.filepath_button)
        self.canvas.create_window(200, 250, window=self.download_button)

    def select_filepath(self):
        """Set the user defined path"""
        self.filepath = filedialog.askdirectory()
        self.filepath_label.config(text=self.filepath)

    def handle_download(self):
        """Handle the download button click event"""
        video_url = self.download_entry.get()

        if not self.filepath:
            self.show_error("Please select a file path")
            return

        if not video_url:
            self.show_error("Please provide video url")
            return
        
        try:
            VideoHandler.download_video(video_url, self.filepath)
        except RuntimeError as e:
            self.show_error(str(e))


    def show_error(self, message):
        """Display error message to the user"""
        error_label = Label(self.app, text=message, fg='red')
        self.canvas.create_window(200, 280, window=error_label)


    def run(self):
        """Rain the main event loop"""
        self.app.mainloop()

        
if __name__ == "__main__":
    video_app = VideoDownloaderApp()
    video_app.run()
        