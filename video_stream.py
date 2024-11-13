# video_stream.py
import yt_dlp

def get_video_url(youtube_url):
    ydl_opts = {
        'format': 'worst',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict['url']
