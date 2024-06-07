from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import functools
from yt_dlp import YoutubeDL
import asyncio

# ProcessPoolExecutor,

class DownloadVideo:
  def __init__(self, url_video:str):
    self.url_video = url_video
    pass
  
  @property
  def get_data(self):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'all',
        'noplaylist': True,
        'ignoreerrors': True
    }
    
    hasil = None
    with YoutubeDL(ydl_opts) as ydl:
        info_source = ydl.extract_info(url=self.url_video, download=False)
        hasil = info_source
    return hasil



class DownloadManyVideo:
    def __init__(self, url) -> None:
       self.url = url
   
    def get_video_detail(self,url_video):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'all',
            'noplaylist': True,
            'ignoreerrors': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_video, download=False)
            return ydl.sanitize_info(info)
        
    async def fetch_all_info(self,urls_video):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor(max_workers=20) as executor:
            tasks = [
                loop.run_in_executor(executor, functools.partial(self.get_video_detail, url))
                for url in urls_video
            ]
            results = await asyncio.gather(*tasks)
            
        return results
    
    @property
    def get_many_info(self):
        return asyncio.run(self.fetch_all_info(self.url))
        
    @property
    def get_info(self):
        uri = [self.url]
        return asyncio.run(self.fetch_all_info(uri))


if __name__ == "__main__":
    nanda = DownloadVideo(url_video="https://youtube.com/watch?v=38fJIy2FoDg")
    if nanda.get_data == None:
        print("error")
    else:
        vid = (nanda.get_data["formats"])
        print(vid)
    
    
    # Contoh URL
    # ch = Channel("https://www.youtube.com/@alyacitra7137")
    # urls = [vid.watch_url for vid in ch.videos]
    
    # # urls = [
    # #     "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    # #     "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
    # #     "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
    # #     "https://www.youtube.com/watch?v=VbfpW0pbvaU",
    # #     "https://www.youtube.com/watch?v=OPf0YbXqDm0",
    # #     "https://www.youtube.com/watch?v=9bZkp7q19f0",
    # #     "https://www.youtube.com/watch?v=ktvTqknDobU",
    # #     "https://www.youtube.com/watch?v=60ItHLz5WEA",
    # #     "https://www.youtube.com/watch?v=8UVNT4wvIGY",
    # #     "https://www.youtube.com/watch?v=6Ejga4kJUts"
    # # ]
    
    # url = "https://youtube.com/watch?v=38fJIy2FoDg"

    # # Menjalankan fungsi asinkron untuk mendapatkan informasi dari semua URL
    # nanda = DownloadManyVideo(url=urls)
    # results = nanda.get_many_info

    # # Menampilkan hasil
    # for i, result in enumerate(results):
    #     print(f"Info for URL {urls[i]}: {result}")