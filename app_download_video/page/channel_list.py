import flet as ft
from custom_package import DownloadVideo, DownloadManyVideo
import threading
from pytube import Channel

class ChannelListVideo(ft.Column):
    def __init__(self):
        super().__init__()
        self.input_url = ft.Ref[ft.TextField]()
        self.format_video = ft.Ref[ft.Dropdown]()
        self.format_type_video_ch = ft.Ref[ft.Dropdown]()
        self.btn_search = ft.Ref[ft.ElevatedButton]()
        self.input_url_hasil = ft.Ref[ft.TextField]()
        self.label_is_success = ft.Ref[ft.Text]()
        
        # value format download
        self.value_format_download = ["720p", "360p", "audio_best"]
        
        # value video download
        self.type_video_channel = ["video","short", "live"]
        
        # hasil dari pencarian
        self.video_details_info = []
        
        # url hasil
        self.text_url_hasil:str = ""
        
        
        self.value_start_end_list = {"start": 0, "end": None}
        pass
    
    def build(self):
        return ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # judul dari playlist
                            ft.Container(
                                content=ft.Text(
                                    value="Channel List Youtube Video", 
                                    text_align= ft.TextAlign.CENTER
                                ),
                                alignment= ft.alignment.center,
                                padding= 20
                            ),
                            # tempat input pencarian
                            ft.Container(
                                padding = 10,
                                content=ft.TextField(
                                    label="url playlist",
                                    expand=True,
                                    ref=self.input_url
                                ),
                            ),
                            # btn untuk pencarian
                            ft.Row(
                                alignment= ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Dropdown(
                                        options=[
                                            ft.dropdown.Option(key=val, text=val) for val in self.type_video_channel
                                        ],
                                        label="type",
                                        width=130,
                                        value=self.type_video_channel[0],
                                        ref= self.format_type_video_ch
                                    ),
                                    ft.Dropdown(
                                        options=[
                                            ft.dropdown.Option(key=val, text=val) for val in self.value_format_download
                                        ],
                                        label="format",
                                        width=130,
                                        value=self.value_format_download[0],
                                        ref=self.format_video,
                                        on_change=self.on_change_format
                                    ),
                                    ft.TextField(
                                        value=1,
                                        label="start",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        key="start",
                                        width=60,
                                        on_change= self.change_start_video,
                                    ),
                                    ft.TextField(
                                        label="end",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        key="end",
                                        width=60,
                                        on_change= self.change_start_video
                                    ),
                                    ft.ElevatedButton(
                                        text="Search",
                                        style= ft.ButtonStyle(
                                            padding= 20
                                        ),
                                        on_click= self.search_proccess,
                                        ref=self.btn_search
                                    )
                                ]
                            ),

                            # label menempelkan url
                            ft.Container(
                                content=ft.Text(
                                    ref= self.label_is_success,
                                    value= "Masukan link diatas dulu",
                                    text_align= ft.TextAlign.CENTER,
                                    size= 20,
                                    weight= ft.FontWeight.BOLD
                                ),
                                padding= 20,
                                alignment= ft.alignment.center,
                            ),
                            
                            # tempat menempelkan url hasil
                            ft.Container(
                                content=ft.TextField(
                                    hint_text="url download",
                                    min_lines= 10,
                                    max_lines= 10,
                                    multiline= True,
                                    expand= True,
                                    ref= self.input_url_hasil
                                )
                            ),
                            # label tips
                            ft.Container(
                                padding=ft.padding.only(0,10,0,0),
                                alignment= ft.alignment.center,
                                content= ft.Markdown(
                                    '''Tip: __Ctrl + A__ lalu __Ctrl + C__ dan pergi ke *FDM* -> *Menu* -> *Paste urls from clipboard*.''',
                                    selectable=False,
                                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                )
                            ),
                            # label tips
                            ft.Container(
                                alignment= ft.alignment.center,
                                content= ft.Markdown(
                                    '''Catatan: fitur __download__ masih belum tersedia. Untuk sementara gunakan download manager external. Karena jumlah video dalam channel lumayan banyak dan akan memakan waktu lama, saya merekomendasikan agar membatasi dengan menggunaka _start_ untuk dimulai dari list mana dan _end_ di akhiri mana''',
                                    selectable=False,
                                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                )
                            ),
                            ft.Container(
                                alignment= ft.alignment.center,
                                content= ft.Markdown(
                                    '''Karena jumlah video dalam channel lumayan banyak dan akan memakan waktu lama, saya merekomendasikan agar membatasi dengan menggunaka _start_ untuk dimulai dari list ke-n dan _end_ diakhiri list ke-n. Untuk mengambil video dari-n sampai habis cukup kosongkan saja input _end_. Jika _start_ dan _end_ tidak diisi kami menganggap mulai dari awal sampai habis''',
                                    selectable=False,
                                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                )
                            ),
                            
                            
                        ]
                    )
                )
            ]
        )
    
    
           
    def search_proccess(self, e):
        self.label_is_success.current.value = "Sabar ya, lagi proses pencarian nih!"
        self.label_is_success.current.color = ft.colors.BLUE_600
        self.btn_search.current.disabled = True
        self.update()
        
        self.search_link_yt_video()
        pass
    
    def search_link_yt_video(self):
        try:
            ch = Channel(self.input_url.current.value)
            
            list_url = [vid.watch_url for vid in ch.videos]
            
            if self.format_type_video_ch.current.value == "short":
                list_url = [vid.watch_url for vid in ch.shorts]
            if self.format_type_video_ch.current.value == "live":
                list_url = [vid.watch_url for vid in ch.live]
            
            
            a = self.value_start_end_list["start"] - 1
            b = self.value_start_end_list["end"]
            print(a,b)
            
            list_filter = list_url
            
            if b != None and b > len(list_url):
                b = None
                
            if a == None or a <= 0:
                a = 0
            
            print(a,b)
            
            if b != None:
                list_filter = list_url[a:b]
            else:
                list_filter = list_url[a:]
            
            print(list_filter)
            
            video_detail = DownloadManyVideo(list_filter)
            get_video_info = video_detail.get_many_info
            
            
            data = [self.search_video_url(data) for data in get_video_info]
            self.video_details_info = data
                
            for hasil in self.video_details_info:
                
                if hasil != None and  hasil[self.format_video.current.value] != "none":
                    self.text_url_hasil += f"{hasil[self.format_video.current.value]}\n"
            
            self.label_is_success.current.value = "Udah selesai bos! dibawah hasil urlnya."
            self.label_is_success.current.color = ft.colors.GREEN_600
            self.btn_search.current.disabled = False
            self.input_url_hasil.current.value = self.text_url_hasil
            self.update()
                
            
                
        except:
            self.label_is_success.current.value = "Internet atau url yang anda masukan bermasalah!"
            self.label_is_success.current.color = ft.colors.RED_600
            self.btn_search.current.disabled = False
            self.update()

    
    
    
    def search_video_url(self, data_video_detail):
        if data_video_detail == None:
            return None
        hasil = {
            "id": data_video_detail["id"],
            "title": data_video_detail["title"],
            "360p" : "none",
            "720p" : "none",
            "audio_best": "none",
            "selected": "none"
        }
        
        for format in data_video_detail["formats"]:
            try:
                if format["vcodec"] != "none" and format["acodec"] != "none":
                   if format["format_note"] == "360p":
                      hasil["360p"] = format["url"] 
                   if format["format_note"] == "720p":
                      hasil["720p"] = format["url"] 
            except:
                pass
        
        try:
            nanda = [audio for audio in data_video_detail["formats"] if audio["resolution"] == "audio only"]
            hasil["audio_best"] = max(nanda, key=lambda x: x["filesize_approx"])["url"]
        except:
            pass

        if hasil["720p"] != "none":
            hasil["selected"] = "720p"
        elif hasil["360p"] != "none":
            hasil["selected"] = "360p"
        
        return hasil
        
     
    def change_start_video(self, e):
        try:
            if e.control.key == "start":
                self.value_start_end_list["start"] = int(e.control.value)
            
            if e.control.key == "end":
                self.value_start_end_list["end"] = int(e.control.value)
        except:
            if e.control.key == "start":
                self.value_start_end_list["start"] = None
            
            if e.control.key == "end":
                self.value_start_end_list["end"] = None
            
        
        
    def on_change_format(self, e):
        self.text_url_hasil = ""
        for hasil in self.video_details_info:
            if hasil[self.format_video.current.value] != "none":
                self.text_url_hasil += f"{hasil[self.format_video.current.value]}\n"
        
        self.label_is_success.current.value = "Udah selesai bos! dibawah hasil urlnya."
        self.label_is_success.current.color = ft.colors.GREEN_600
        self.btn_search.current.disabled = False
        self.input_url_hasil.current.value = self.text_url_hasil
        self.update()