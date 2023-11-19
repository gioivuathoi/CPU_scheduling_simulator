import pygame
import sys
# Init
pygame.init() 
screen = pygame.display.set_mode((600,600)) 
white_color = (255,255,255)
screen.fill(white_color)

# Utility Functions

def to_width(string, length, align=False):
    
    # Modify a string to match the given length
    
    # :param string: The string to modify
    # :param length: The final length
    # :param align: Align string left (False) or right (True)
    string = str(string)
    if len(string) > length:
        return string[:length-2]+".."
    else:
        return string.rjust(length," ") if align else string.ljust(length, " ")

# Classes
class Table:
    def __init__(self, rows, settings, fontsize=12):
        self.rows = rows
        self.fontsize = fontsize
        self.settings = settings
        self.font = pygame.font.Font("GUI/OpenSans-Regular.ttf",fontsize)

    def draw(self, win, x=10, y=10):
        
        # Draw the table on a PyGame Surface starting at specified position
        
        win.blit(self.font.render("".join(to_width(s[0], s[1], s[2]) for s in self.settings), True, (0,0,0)), (x, y))
        y += self.fontsize+5

        for row in self.rows:
            info = ""
            for i,s in enumerate(self.settings):
                  print(s[1], s[2])
                  info += to_width(row[i],s[1], s[2])
            print(info)
            text = self.font.render(info,True, (0,0,0))
            win.blit(text,(x,y))
            # win.blit(self.font.render(" ".join(to_width(row[i], s[1], s[2]) for i, s in enumerate(self.settings)), True, (0,0,0)), (x, y))
            y += self.fontsize+5

rows = [
    ["Rafael", "16", "Switzerland"],
    ["Someone", "100", "Germany"]]

settings = [
    ["Name",20, False],
    ["Age", 15, False],
    ["Country",20, False]
    # (title, max_length, align (right: True, left: False))
]

table = Table(rows, settings)
table.draw(screen, 50,50)
pygame.display.update()
running = True
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
