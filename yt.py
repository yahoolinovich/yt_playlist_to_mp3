from pytube import YouTube, Playlist
import os
import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO

def download(vid, index):
    yt = YouTube(vid)
    vid = yt.streams.filter(only_audio=True).first()
    out = vid.download()
    base, ext = os.path.splitext(out)
    os.rename(out, base + '.mp3')
    status_labels[index].config(text="Download complete")

def get_video_info(url):
    yt = YouTube(url)
    return {
        'title': yt.title,
        'thumbnail': yt.thumbnail_url
    }

def download_playlists():
    link = entry.get()
    playlist_urls = Playlist(link)
    links = [i for i in playlist_urls]

    for widget in video_widgets:
        widget.destroy()
    video_widgets.clear()
# Display video caption, thumbnail and Download status
    for i, link in enumerate(links):
        video_info = get_video_info(link)

        # Frame for each video
        video_frame = tk.Frame(window, bg="white", bd=2, relief=tk.SOLID)
        video_frame.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
        response = requests.get(video_info['thumbnail'])
        img = Image.open(BytesIO(response.content))
        img = img.resize((120, 90), Image.ANTIALIAS)
        thumbnail_img = ImageTk.PhotoImage(img)
        thumbnail_label = tk.Label(video_frame, image=thumbnail_img)
        thumbnail_label.image = thumbnail_img
        thumbnail_label.pack(side=tk.LEFT, padx=10, pady=10)
        video_widgets.append(thumbnail_label)

        # Caption of video
        caption_label = tk.Label(video_frame, text=video_info['title'], bg="white")
        caption_label.pack(side=tk.LEFT, padx=10, pady=10)
        video_widgets.append(caption_label)

        # Download Status
        status_label = tk.Label(video_frame, text="", bg="white")
        status_label.pack(side=tk.LEFT, padx=10, pady=10)
        status_labels.append(status_label)

    # Download each video
    for i, link in enumerate(links):
        status_labels[i].config(text="Downloading...")
        download(link, i)


window = tk.Tk()
window.title("YouTube Playlist Downloader")
window.configure(bg="white")
label = tk.Label(window, text="Enter the YouTube playlist URL:", bg="white")
label.grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(window, width=50)
entry.grid(row=0, column=1, padx=10, pady=10)
button = tk.Button(window, text="Download", command=download_playlists)
button.grid(row=0, column=2, padx=10, pady=10)


video_widgets = []
status_labels = []

# Start the GUI event loop
window.mainloop()
