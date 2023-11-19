import pygame
import pygame_menu
from pygame_menu import themes
import time
pygame.init()
surface = pygame.display.set_mode((600, 600))
theme = themes.Theme(
            title_font_size=30,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
            background_color=(116, 161, 122),
            title_background_color=(4, 47, 58),
            title_font_color=(38, 158, 151),
            widget_selection_effect=pygame_menu.widgets.NoneSelection()
        )
menu = pygame_menu.Menu("CPU SCHEDULING",500,500, theme=theme)
table = menu.add.table("111")

row0 = table.add_row(["","CPU",""], row_background_color = 'red',cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_width=0)
row1 = table.add_row([1, 2, 3], row_background_color='blue', cell_align=pygame_menu.locals.ALIGN_CENTER)
row2 = table.add_row([10, 20, 30], row_background_color='green', cell_padding=10)
table.draw(surface)
# time.sleep(10)
menu.mainloop(surface)