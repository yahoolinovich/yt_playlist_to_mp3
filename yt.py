from pytube import YouTube, Playlist
import os


def download(vid):
    yt = YouTube(vid)

    vid = yt.streams.filter(only_audio=True).first()

    out = vid.download()

    base,ext = os.path.splitext(out)
    os.rename(out,base + '.mp3')


link = (str(input('Link of Playlist URL: \n')))
print('Starting Download...')
playlist_urls = Playlist(link)
links = [i for i in playlist_urls]
for i in range(len(links)):
    print(f'Download {i + 1} downloading...')
    download(links[i])
    print(f'Download {i+1} complete.')
