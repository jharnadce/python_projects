# Video Downloader App

This application allows the user to provide the URL to any youtube video
and the app can download the video file for them in a few different formats

#### Packages 
 - tkinter for UI
 - pytube to extract and download the file from the youtube url
 - moviepy to convert the file to video (mp4) and audio (mp3) format
 - shutil to move the downloaded / converted files from local folder to desired folder

#### App Layout
 - App window and Canvas title
 - Window sizing and format using Canvas
 - Label and Entry widget for providing video URL
 - Label and entry widget to accept path where to save the file
 - Button to request video download
 - Optional checkbox to say whether audio file is also needed
 - Button or widget to get download link or direct download - not needed

#### Steps
 1. Create the user interface
 2. Accept path to download video
 3. Get local path functional
 4. Make download button functional
 5. Test the app
 6. Convert video to MP3

#### Classes
- App class
    - TBD
- Video class
    - Attributes: url
    - Methods: get_video()