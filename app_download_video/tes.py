import asyncio
from aioprocessing import AioProcess, AioQueue
from yt_dlp import YoutubeDL
from pytube import Playlist

class VideoInfoFetcher:
    def __init__(self, urls):
        self.urls = urls

    def get_info(self, url):
        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)

    async def fetch_info_async(self, queue, url):
        info = self.get_info(url)
        await queue.coro_put(info)

    async def fetch_all_info(self):
        queue = AioQueue()
        processes = [AioProcess(target=self.fetch_info_async, args=(queue, url)) for url in self.urls]
        for process in processes:
            process.start()
        results = []
        for _ in self.urls:
            result = await queue.coro_get()
            results.append(result)
        for process in processes:
            process.join()
        return results

    def run(self):
        return asyncio.run(self.fetch_all_info())

# Mengambil URL dari playlist menggunakan `pytube`
playlist_url = "https://www.youtube.com/watch?v=dMYv6InQgno&list=PLcZp9zrMgnmOOQXevC-2CfH67QP3mB4wv"
playlist = Playlist(playlist_url)
urls = [video.watch_url for video in playlist.videos]

# Membuat instance dari VideoInfoFetcher dan menjalankan fetcher
fetcher = VideoInfoFetcher(urls)

# Jika ini dijalankan dalam konteks Flet atau GUI lainnya:
if __name__ == "__main__":
    import threading

    def run_fetcher():
        results = fetcher.run()
        for i, result in enumerate(results):
            print(f"Info for URL {urls[i]}: {result}")

    fetcher_thread = threading.Thread(target=run_fetcher)
    fetcher_thread.start()
