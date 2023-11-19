# import pygame package 
import pygame 
import sys
import pygame_menu
from pygame_menu import themes
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN 
)
from pygame.sprite import AbstractGroup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SURFACE_COLOR = (255,255,255)
RED = (255,0,0)

# Here to initialize pygamr
pygame.init() 

# Here to setup some font will be used 
mediumFont = pygame.font.Font("GUI/OpenSans-Regular.ttf",28)
largeFont = pygame.font.Font("GUI/OpenSans-Regular.ttf",40)

# Here to set the caption for the main window
pygame.display.set_caption('CPU Scheduling')

#Here to setup the mode and size of the main window
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
white_color = (255,255,255)

#Here to fill the window or background with white color
screen.fill(white_color)
# Create the process class
class process(pygame.sprite.Sprite):
	def __init__(self, id, color, x,y, height, width):
		super().__init__()

		self.process_box = pygame.Rect(x,y,width, height)
		
		self.id = mediumFont.render(id, True, (0,0,0))
		# self.image.fill(SURFACE_COLOR)
		self.color = color
		# self.id.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.id.get_rect(size = (width/2, height/2))
		self.rect.center = self.process_box.center
		self.rect.x += 10
		pygame.draw.rect(screen,color, self.process_box)

	def moveRight(self, pixels):
		self.rect.x += pixels
		self.process_box.x += pixels
	def moveLeft(self, pixels):
		self.rect.x -= pixels
		self.process_box.x -= pixels
	def draw_process_box(self):
		pygame.draw.rect(screen,self.color, self.process_box)

class CPU(pygame.sprite.Sprite):
	def __init__(self) -> None:
		super().__init__()

# Create menu which contain cpu utilization table
theme = themes.Theme(
            title_font_size=30,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
            background_color=(116, 161, 122),
            title_background_color=(4, 47, 58),
            title_font_color=(38, 158, 151),
            widget_selection_effect=pygame_menu.widgets.NoneSelection()
        )
menu_cpu = pygame_menu.Menu("CPU UTILIZATION",750,175, theme=theme, position=(750, 50, False))
table_cpu = menu_cpu.add.table("1")

row1 = table_cpu.add_row(["Job", "Time", "Idle Time", "Utilization", "Avg. Waiting", "Avg. Turnaround"], row_background_color=(96,96,96),
					 cell_align=pygame_menu.locals.ALIGN_CENTER, cell_padding=10,
					   cell_font_color = (255,255,255), cell_font_size = 23)
row2 = table_cpu.add_row(["Idle",0, 0,"0%",0,0], row_background_color='green', cell_padding=10, cell_font_size = 23)

# Create menu which contain job table
menu_job = pygame_menu.Menu("TABLE OF JOB", 1440, 390, theme=theme, center_content=False,position=(50,450, False))
table_job = menu_job.add.table("2")
job1 = table_job.add_row(["PID","Arrive Time", "Burst Time", "Priority","Response Time","Return Time", "Waiting Time", "Turnaround Time"],
						 row_background_color=(96,96,96),cell_padding=(4,25),cell_font_color = (255,255,255), cell_font_size = 23 )
# Create the group of process
all_sprites_list = pygame.sprite.Group()
p1 = process("P1", (0,255,255), 50, 100, 100, 100)
all_sprites_list.add(p1)

# Create QUEUE and CPU regtangle
pygame.draw.rect(screen, (0, 0, 255), [50, 100, 500, 100], 2)
pygame.draw.rect(screen, (255,0,0), [600, 100, 100, 100], 2)
pygame.draw.rect(screen, (255,128,0), [50, 330, 1440, 100], 2)
queue_text = mediumFont.render("QUEUE", True, (32,32,32))
cpu_text = mediumFont.render("CPU", True, (102,0,0))
gantt_text = mediumFont.render("GANTT CHART", True, (204,102,0))
rect_queue_text = queue_text.get_rect()
rect_cpu_text = cpu_text.get_rect()
rect_gantt_text = gantt_text.get_rect()
rect_queue_text.center = (300,70)
rect_cpu_text.center = (650, 70)
rect_gantt_text.center = (750, 300)
screen.blit(queue_text, rect_queue_text)
screen.blit(cpu_text,rect_cpu_text)
screen.blit(gantt_text,rect_gantt_text)
# Update the display for the first time
pygame.display.update()

# Now let's start our main loop
running = True
clock = pygame.time.Clock()
# keep game running till running is true 
while running: 
	# Check for event if user has pushed 
	# any event in queue 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				running = False
		elif event.type == pygame.K_ESCAPE:
			sys.exit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		p1.moveLeft(10)
	if keys[pygame.K_RIGHT]:
		p1.moveRight(10)
 
	all_sprites_list.update()
	screen.fill(SURFACE_COLOR)
	for entity in all_sprites_list:
		entity.draw_process_box()
		screen.blit(entity.id,entity.rect)
	pygame.draw.rect(screen, (0, 0, 255), [50, 100, 500, 100], 2)
	pygame.draw.rect(screen, (255,0,0), [600, 100, 100, 100], 2)
	pygame.draw.rect(screen, (255,128,0), [50, 330, 1440, 100], 2)
	screen.blit(queue_text, rect_queue_text)
	screen.blit(cpu_text,rect_cpu_text)
	screen.blit(gantt_text,rect_gantt_text)
	menu_cpu.draw(screen)
	menu_job.draw(screen)
	pygame.display.flip()
	clock.tick(29)
 
pygame.quit()
