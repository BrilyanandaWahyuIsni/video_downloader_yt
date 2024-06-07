import flet as ft
from pytube import Playlist
from custom_package import DownloadManyVideo

class PlaylistVideo(ft.Column):
    def __init__(self):
        super().__init__()
        self.input_url = ft.Ref[ft.TextField]()
        self.format_video = ft.Ref[ft.Dropdown]()
        self.btn_search = ft.Ref[ft.ElevatedButton]()
        self.input_url_hasil = ft.Ref[ft.TextField]()
        self.label_is_success = ft.Ref[ft.Text]()
        
        # value format download
        self.value_format_download = ["720p", "360p", "audio_best"]
        
        # hasil dari pencarian
        self.video_details_info = []
        
        # url hasil
        self.text_url_hasil:str = ""
        
        
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
                                    value="Playlist Download Youtube Video", 
                                    text_align= ft.TextAlign.CENTER
                                ),
                                alignment= ft.alignment.center,
                                padding= 20
                            ),
                            # tempat input dan btn pencarian
                            ft.Row(
                                controls=[
                                    ft.TextField(
                                        ref= self.input_url,
                                        label= "url playlist",
                                        expand= True,
                                    ),
                                    ft.Dropdown(
                                        options=[
                                            ft.dropdown.Option(key= value, text=value) for value in self.value_format_download
                                        ],
                                        label="format",
                                        width=130,
                                        ref=self.format_video,
                                        value= self.value_format_download[0],
                                        on_change= self.on_change_format
                                    ),
                                    ft.ElevatedButton(
                                        on_click=self.search_proccess,
                                        text="Search",
                                        style= ft.ButtonStyle(
                                            padding= 20
                                        ),
                                        ref = self.btn_search
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
                                alignment= ft.alignment.center
                            ),
                            
                            # tempat menempelkan url hasil
                            ft.Container(
                                content=ft.TextField(
                                    hint_text="url download",
                                    min_lines= 10,
                                    max_lines= 10,
                                    multiline= True,
                                    expand= True,
                                    ref=self.input_url_hasil
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
                                    '''Catatan: fitur __download__ masih belum tersedia. Untuk sementara gunakan download manager external.''',
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
            get_url_yt = Playlist(self.input_url.current.value)
            
            list_url = [vid.watch_url for vid in get_url_yt.videos]
            
            video_detail = DownloadManyVideo(list_url)
            get_video_info = video_detail.get_many_info
            
            data = [self.search_video_url(index=index,data_video_detail=data) for index, data in enumerate(get_video_info)]
            self.video_details_info = data
               
                
            for hasil in self.video_details_info:
                if hasil[self.format_video.current.value] != "none":
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

    
    def search_video_url(self, index, data_video_detail):
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
                      hasil["360p"] = f'{format["url"]}&title={index+1}. {data_video_detail["title"]}'
                   if format["format_note"] == "720p":
                      hasil["720p"] = f'{format["url"]}&title={index+1}. {data_video_detail["title"]}'
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
        pass