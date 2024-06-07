import flet as ft
from time import sleep
from custom_package import DownloadVideo

class OneVideo(ft.Column):
    def __init__(self):
        super().__init__()
        
        # formats tersimpan
        self.result_download = []
        
        # url download
        self.url_download = ""
        
        # searching button and input
        self.input_search_url = ft.TextField(
            expand= True,
            label="input url",
            multiline= False,
        )
        self.btn_search_url = ft.ElevatedButton(
            text="Search",
            icon= ft.icons.SEARCH,
            style= ft.ButtonStyle(
                padding= 20
            ),
            on_click=self.click_btn_search
        )
        
        # label judul
        self.label_judul_video_search = ft.Text(
            value="",
            style= ft.TextStyle(
                decoration= ft.TextDecoration.UNDERLINE,
                color= ft.colors.CYAN_500,
                size= 18,
                weight= ft.FontWeight.BOLD
            )
        )
        
        # selection download video audio or storyboard
        self.select_download_format = ft.Dropdown(
            label= "--pilih format tersedia--",
            options=[
                ft.dropdown.Option(text= f"pilihan ke-{x}", key=f"{x}") for x in range(10)
            ],
            on_change=self.func_selection_download,
        )
        
        # textinput untuk mendapatkan hasil url
        self.textinput_url_hasil = ft.TextField(
            multiline=True,
            expand=True,
            hint_text= "Url downloader ...",
            min_lines= 5,
            max_lines= 5,
        )
        
        # btn download file 
        self.btn_download_file = ft.ElevatedButton(
            text="Download",
            style= ft.ButtonStyle(
                padding= 20
            ),
            on_click=self.func_start_download
        )
        
        
        # progress bar download
        self.progressbar_download = ft.Ref[ft.ProgressBar]()
        
        # referensi collumn menu and download selection
        self.ref_column_menu_selection = ft.Ref[ft.Column]()
        
        # referensi column download btn and progressbar
        self.ref_coloumn_download = ft.Ref[ft.Column]()
        
        
    def build(self):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                       self.input_search_url,
                       self.btn_search_url                        
                    ]
                ),
                ft.Container(
                    visible= False,
                    ref=self.ref_column_menu_selection,
                    padding = 20,
                    alignment= ft.alignment.center,
                    content= ft.Column(
                        controls=[
                            ft.Container(
                                alignment= ft.alignment.center,
                                padding=5,
                                content= self.label_judul_video_search
                            ),
                            self.select_download_format
                        ]
                    )
                ),
                ft.Container(
                    alignment= ft.alignment.center,
                    content=self.textinput_url_hasil
                ),
                ft.Container(
                    padding=5,
                    alignment= ft.alignment.center,
                    content= ft.Text(
                        value= "Tip: Ctrl + A lalu Ctrl + C dan pergi ke FDM ->Menu -> Paste urls from clipboard atau dengan download manager lainnya seperti IDM. Download dari aplikasi ini belum tersedia, tapi dikemudian hari mungkin akan tersedia.",
                        size= 12,
                        text_align= ft.TextAlign.CENTER
                    )
                ),
                ft.Column(
                    ref=self.ref_coloumn_download,
                    visible=False,
                    controls=[
                        ft.Container(
                            padding=5,
                            alignment= ft.alignment.center,
                            content= self.btn_download_file
                        ),
                        ft.ProgressBar(
                            ref= self.progressbar_download,
                            value = 0,
                            bar_height= 20,
                        )
                        
                    ]    
                ),
                
            ]
        )
    

    # fungsi sesudah memilih format video yang ingin di download
    def func_selection_download(self, e):
        key_option = self.select_download_format.value
        
        nanda = next(( res["url"] + "&title="  for res in self.result_download["formats"] if res["format_id"] == key_option),None)
        
        url_hasil = nanda + self.result_download["title"]
        
        self.url_download = url_hasil
        
        # memasukan url kedalam input saat file dipilih
        self.textinput_url_hasil.value = url_hasil
        # self.ref_coloumn_download.current.visible = True
        self.update()
        
    
    # tekan tombol pencarian / press button searching
    def click_btn_search(self,e):
        self.url_download = ""
        self.prosses_waiting_search(is_prosses=True)
        
        self.proses_searching_video()        
                
        if self.input_search_url != "":
            self.ref_column_menu_selection.current.visible = True
            self.label_judul_video_search.value = self.result_download["title"]
            
        self.prosses_waiting_search(is_prosses=False)     
        self.update()
    
    
    # progress dari download file/ progress file download after press button download
    def func_start_download(self, e):
        for i in range(0, 100):
            self.progressbar_download.current.value = i * 0.1
            sleep(0.1)
            self.update()
    
    
    # layout url input/output prosess 
    def prosses_waiting_search(self, is_prosses:bool):
        self.btn_search_url.disabled = is_prosses
        self.input_search_url.disabled = is_prosses
        
        if is_prosses:
            self.btn_search_url.text = "Loading ..."
        else:
            self.btn_search_url.text = "Search"
            
        self.update()
    
    
    # proses pencarian format file setelah di searching/ proccess search format file after searching
    def proses_searching_video(self):
        download_video = DownloadVideo(self.input_search_url.value)
        self.result_download = download_video.get_data
        
        self.option_download_format = []
        for vid in self.result_download["formats"]:
            format_vidio = ""
            
            is_video:bool = False
            is_audio:bool = False
            
            if vid["vcodec"] != "none":
                is_video = True
            try:
                if vid["acodec"] != "none":
                    is_audio = True
            except:
                pass
            
            if is_audio and is_video:
                format_vidio = "video"
            
            if is_audio != True and is_video:
                format_vidio = "video [no audio]"
            
            ttext = vid["format"] + " " + format_vidio
            self.option_download_format.append({"key": vid["format_id"], "text": ttext})
        
        self.select_download_format.options = [
            ft.dropdown.Option(text=vid["text"], key=vid["key"]) for vid in self.option_download_format
        ]
        self.update()