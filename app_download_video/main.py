import flet as ft
from page import OneVideo,PlaylistVideo,ChannelListVideo


class MyNavbar:
    def __init__(self, page:ft.Page):
        self.page_selection = [OneVideo(), PlaylistVideo(), ChannelListVideo()]
        
        self.page = page
        self.navi_utama = ft.NavigationBar(
            on_change= self.change_page,
            selected_index=0,
            destinations=[
                ft.NavigationDestination(
                    icon= ft.icons.ONDEMAND_VIDEO,
                    label= "Video"
                ),
                ft.NavigationDestination(
                    icon = ft.icons.PLAYLIST_ADD_CHECK ,
                    label= "Playlist"
                ),
                ft.NavigationDestination(
                    icon = ft.icons.ASSIGNMENT_IND_SHARP,
                    label= "Channel"
                )
            ]
        )
        self.page.navigation_bar = self.navi_utama
        self.main_page = ft.Container(
            content= self.page_selection[0],
            padding= ft.padding.only(left=20,right=20)
        )
        
        self.page.add(self.main_page)
    
    def change_page(self, e):
        self.main_page.content = self.page_selection[e.control.selected_index]
        self.page.update()
        
        

# bagian utama
def main(page: ft.Page):
    page.title = "Cakata Download Video Youtube"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO    
    MyNavbar(page=page)
    
    
if __name__ == "__main__":
    ft.app(target=main)