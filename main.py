# import pygame package 
import pygame 
import sys
import pygame_menu
from pygame_menu import themes
import time
import copy
from CpuSchedulingAlgorithmsModule.Process import *
from CpuSchedulingAlgorithmsModule.Run_Scheduling import *
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
# Here are the param that will be used for CPU table
total_process = 0
pygame.init() 
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 

# Here to initialize pygame
# Here to setup some font will be used 
mediumFont = pygame.font.Font("GUI/OpenSans-Regular.ttf",28)
largeFont = pygame.font.Font("GUI/OpenSans-Regular.ttf",40)

# Here to set the caption for the main window
pygame.display.set_caption('CPU Scheduling')
#Here to setup the mode and size of the main window
white_color = (255,255,255)
#Here to fill the window or background with white color
screen.fill(white_color)
# Create the process class
# Create menu which contain cpu utilization table
theme = themes.Theme(
            title_font_size=25,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
            background_color=(116, 161, 122),
            title_background_color=(4, 47, 58),
            title_font_color=(38, 158, 151),
            widget_selection_effect=pygame_menu.widgets.NoneSelection()
        )
menu_cpu = pygame_menu.Menu("CPU UTILIZATION",650,175, theme=theme, position=(800, 50, False))
table_cpu = menu_cpu.add.table("1")

row1 = table_cpu.add_row(["Job", "Time", "Utilization", "Avg. Waiting", "Avg. Turnaround"], row_background_color=(96,96,96),
					 cell_align=pygame_menu.locals.ALIGN_CENTER, cell_padding=10,
					   cell_font_color = (255,255,255), cell_font_size = 23)
row2 = table_cpu.add_row(["Idle", 0,"0%",0,0], row_background_color='green', cell_padding=15, cell_font_size = 23)

# Create menu which contain job table
menu_job = pygame_menu.Menu("TABLE OF JOB", 1440, 350, theme=theme, center_content=False,position=(50,450, False))
table_job = menu_job.add.table("2")
job1 = table_job.add_row(["PID","Arrive Time", "Burst Time", "Priority","Response Time","Return Time", "Waiting Time", "Turnaround Time"],
						 row_background_color=(96,96,96),cell_padding=(4,25),cell_font_color = (255,255,255), cell_font_size = 23 )

class GUI_Process(pygame.sprite.Sprite):
	def __init__(self, id, color, x,y, height, width, border = 0):
		super().__init__()
		self.process_box = pygame.Rect(x,y,width, height)
		self.id = mediumFont.render(id, True, (0,0,0))
		# self.image.fill(SURFACE_COLOR)
		self.color = color
		# self.id.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.id.get_rect(size = (width/2, height/2))
		self.rect.center = self.process_box.center
		self.rect.x += 10
		pygame.draw.rect(screen,color, self.process_box,border)
		screen.blit(self.id, self.rect)

	# def moveRight(self, pixels):
	# 	self.rect.x += pixels
	# 	self.process_box.x += pixels
	# def moveLeft(self, pixels):
	# 	self.rect.x -= pixels
	# 	self.process_box.x -= pixels
	# def draw_process_box(self):
	# 	pygame.draw.rect(screen,self.color, self.process_box)
		
# This code to draw the processes ready queue
def draw_readyqueue(gui_processes):
	# p1 = process("P1", (0,255,255), 50, 100, 100, 100)
	color = (0,255,255)
	initial_x = 50
	initial_y = 100
	height = 100
	width = 100
	for i, process in enumerate(gui_processes):
		x = initial_x + i*100
		process = GUI_Process(process.id, color,x, initial_y, height, width)

# This code to draw the processes in CPU
def draw_cpu(on_cpu_process, percent):
	color = (255,255,0)
	x = 670
	y = 100
	height = 100
	width = 100
	process = GUI_Process(on_cpu_process.id, color, x,y,height, width)
	process_percent = mediumFont.render(percent + "%", True, (102,0,0))
	rect_process_percent = process_percent.get_rect()
	rect_process_percent.center = (process.rect.centerx-10, process.rect.centery+30)
	screen.blit(process_percent,rect_process_percent)

#This code to update the cpu_GUI base on the scheduling algorithm
def draw_gantt_chart(finished_processes):
	color = (77,77,255)
	initial_x = 50
	x = 0
	y = 330
	height = 100
	initial_width = 100
	pre_width = 0
	time0 = mediumFont.render("0", True, (102,0,0))
	rect_time0 = time0.get_rect()
	rect_time0.center = (50,y-20)
	screen.blit(time0,rect_time0)
	for i,process in enumerate(finished_processes):
		# print(process.execution_time)
		width = initial_width + 5*int(process.execution_time)
		if i == 0:
			x = initial_x
		else:
			x += pre_width
		pre_width = width

		percent = str(int(100*process.execution_time/process.burst))
		# print(percent)
		timer = mediumFont.render(str(int(process.return_time)), True, (0,0,20))
		process = GUI_Process(process.id, color,x, y, height, width, 3)
		process_percent = mediumFont.render(percent + "%", True, (0,0,0))
		rect_process_percent = process_percent.get_rect()
		rect_timer = timer.get_rect()
		rect_process_percent.center = (process.rect.centerx-10, process.rect.centery+30)
		rect_timer.center = (x + width,y-20)
		screen.blit(process_percent,rect_process_percent)
		screen.blit(timer,rect_timer)

def update_cpu_GUI(current_time, readyqueue, algorithm):
	if algorithm == "FCFS":
		if len(readyqueue.get_ready_queue()) > 0 and readyqueue.get_ready_queue()[-1].arrive_time < current_time:
		#NOTE:using process.on_cpu to check what process to draw
			# then update the execution_time, if execution_time still less than burst time, we 
			# draw that process and the percent, if not, we pop the process and turn it into granchart
			if readyqueue.get_ready_queue()[-1].on_cpu == False:
				readyqueue.P[-1].update_on_cpu()
				readyqueue.P[-1].update_response_time(current_time)
				readyqueue.P[-1].update_accept_time(current_time)
				readyqueue.P[-1].update_waiting_time(current_time)
			else:
				percent = 100*readyqueue.P[-1].execution_time/readyqueue.P[-1].burst
				if percent > 100:
					finish_process = readyqueue.pop_process()
					finish_process.update_completed_state()
					finish_process.update_return_time(current_time)
					finish_process.update_turnaround_time()
					finish_processes.append(finish_process)
				else:
					draw_cpu(readyqueue.P[-1], str(int(percent)))
					exe_time = current_time - readyqueue.P[-1].accept_time
					readyqueue.P[-1].update_execution_time(exe_time)
		else:
			return 0
	elif algorithm == "SJF":
		readyqueue.update_queue("SJF", current_time)
		if len(readyqueue.get_ready_queue()) > 0 and readyqueue.get_ready_queue()[-1].arrive_time < current_time:
		#NOTE:using process.on_cpu to check what process to draw
			# then update the execution_time, if execution_time still less than burst time, we 
			# draw that process and the percent, if not, we pop the process and turn it into gantt chart
			if readyqueue.get_ready_queue()[-1].on_cpu == False:
				readyqueue.P[-1].update_on_cpu()
				readyqueue.P[-1].update_response_time(current_time)
				readyqueue.P[-1].update_accept_time(current_time)
				readyqueue.P[-1].update_waiting_time(current_time)
			else:
				percent = 100*readyqueue.P[-1].execution_time/readyqueue.P[-1].burst
				if percent > 100:
					finish_process = readyqueue.pop_process()
					finish_process.update_completed_state()
					finish_process.update_return_time(current_time)
					finish_process.update_turnaround_time()
					finish_processes.append(finish_process)
				else:
					# print(readyqueue.P[-1].id)
					draw_cpu(readyqueue.P[-1], str(int(percent)))
					exe_time = current_time - readyqueue.P[-1].accept_time
					readyqueue.P[-1].update_execution_time(exe_time)
	elif algorithm == "RR":
		if len(readyqueue.get_ready_queue()) > 0 and readyqueue.get_ready_queue()[-1].arrive_time < current_time:
		#NOTE:using process.on_cpu to check what process to draw
			# then update the execution_time, if execution_time still less than burst time, we 
			# draw that process and the percent, if not, we pop the process and turn it into gantt chart
			if readyqueue.get_ready_queue()[-1].on_cpu == False:
				readyqueue.P[-1].update_on_cpu()
				readyqueue.P[-1].update_response_time(current_time)
				readyqueue.P[-1].update_accept_time(current_time)
				readyqueue.P[-1].update_waiting_time(current_time, for_RR = True)
				readyqueue.P[-1].update_remain_quantum()
			else:
				percent = 100*(1-(readyqueue.P[-1].remain_quantum/readyqueue.P[-1].quantum))
				if percent >= 100:
					readyqueue.P[-1].update_remain_burst(readyqueue.P[-1].quantum)
					if readyqueue.P[-1].remain_burst <= 0:
						finish_process = readyqueue.pop_process()
						finish_process.update_completed_state()
						finish_process.update_return_time(current_time)
						finish_process.update_turnaround_time()
						finish_process.update_execution_time(finish_process.quantum, add = True)
						finish_processes.append(finish_process)
					else:
						readyqueue.P[-1].update_return_time(current_time)
						readyqueue.P[-1].update_turnaround_time()
						readyqueue.P[-1].update_arrive_time(current_time)
						readyqueue.P[-1].update_on_cpu(value = False)
						readyqueue.P[-1].update_execution_time(readyqueue.P[-1].quantum, add = True)
						# readyqueue.P[-1].update_wait_condition(wait_for = readyqueue.P[i].waiting_time, current_time = current_time)
						finish_processes.append(copy.deepcopy(readyqueue.P[-1]))
				else:
					exe_time = current_time - readyqueue.P[-1].accept_time
					total_percent = 100*(readyqueue.P[-1].execution_time/readyqueue.P[-1].burst + exe_time/readyqueue.P[-1].burst)
					draw_cpu(readyqueue.P[-1], str(int(total_percent)))
					readyqueue.P[-1].update_remain_quantum(reset = False, decrease = exe_time)

	elif algorithm == "PPS":
		if len(readyqueue.get_ready_queue()) > 0 and readyqueue.get_ready_queue()[-1].arrive_time < current_time:
			if readyqueue.get_ready_queue()[-1].on_cpu == False:
				if len(readyqueue.get_ready_queue()) > 1:
					for i,process in enumerate(readyqueue.get_ready_queue()[:-1]):
						if process.on_cpu == True:
							print(process.id)
							process.update_return_time(current_time)
							readyqueue.P[i].update_on_cpu(value = False)
							readyqueue.P[i].update_run_condition(run_for = readyqueue.P[i].execution_time)
							readyqueue.P[i].update_wait_condition(wait_for = readyqueue.P[i].waiting_time, current_time = current_time)
							finish_processes.append(copy.deepcopy(process))
						if process.arrive_time < current_time:
							if readyqueue.P[i].continue_waiting == 0:
								print("First ", process.id)
								print(process.waiting_time)
								readyqueue.P[i].update_waiting_time(current_time)
							else:
								print("Second ", process.id)
								readyqueue.P[i].update_waiting_time(current_time, continue_wait = True)
							add_priority = readyqueue.P[i].waiting_time/30
							readyqueue.P[i].update_priority(add_priority)
				readyqueue.P[-1].update_on_cpu()
				readyqueue.P[-1].update_response_time(current_time)
				readyqueue.P[-1].update_accept_time(current_time)
				if readyqueue.P[-1].continue_waiting == 0:
					print("First ", readyqueue.P[-1].id)
					print(readyqueue.P[-1].waiting_time)
					readyqueue.P[-1].update_waiting_time(current_time)
				else:
					print("Second ", readyqueue.P[-1].id)
					readyqueue.P[-1].update_waiting_time(current_time, continue_wait = True)
				# readyqueue.P[-1].update_waiting_time(current_time)
			else:
				percent = 100*(readyqueue.P[-1].execution_time/readyqueue.P[-1].burst)
				if percent >= 100:
						finish_process = readyqueue.pop_process()
						finish_process.update_completed_state()
						finish_process.update_return_time(current_time)
						finish_process.update_turnaround_time()
						finish_process.update_execution_time(finish_process.quantum, add = True)
						# finish_process.update_waiting_time(current_time)
						finish_processes.append(finish_process)
				else:
					exe_time = current_time - readyqueue.P[-1].accept_time
					if readyqueue.P[-1].continue_run != 0:
						readyqueue.P[-1].update_execution_time(readyqueue.P[-1].continue_run)
						readyqueue.P[-1].update_execution_time(exe_time, add = True)
					else:
						readyqueue.P[-1].update_execution_time(exe_time)
					total_percent = 100*(readyqueue.P[-1].execution_time/readyqueue.P[-1].burst)
					draw_cpu(readyqueue.P[-1], str(int(total_percent)))

def update_ready_queue_GUI(current_time, readyqueue, algorithm):
	if len(readyqueue.get_ready_queue()) == 0:
		return 0
	if algorithm == "FCFS":
		readyqueue.update_queue("FCFS")
	elif algorithm == "SJF":
		readyqueue.update_queue("SJF", current_time)
	elif algorithm == "RR":
		readyqueue.update_queue("RR", quantum = quantum)
	elif algorithm == "PPS":
		readyqueue.update_queue("PPS", quantum = 5, current_time = current_time)
	gui_processes = []
	for process in readyqueue.get_ready_queue():
		if process.arrive_time < current_time and process.on_cpu == False:
			gui_processes.append(process)
	draw_readyqueue(gui_processes)
	
def update_gantt_chart_GUI():
	length = len(finish_processes)
	if length == 0:
		return 0
	elif length <=10:
		draw_gantt_chart(finish_processes)
	elif length > 10:
		num = length - 10
		draw_gantt_chart(finish_processes[num:])

def update_cpu_table(readyqueue, current_time):
	if len(readyqueue.get_ready_queue()) == 0:
		state = "Idle"
	else:
		process = readyqueue.get_ready_queue()[-1]
		if process.on_cpu == True:
			state = process.id
		else:
			state = "Idle"
	total_waiting = 0
	total_turnaround = 0
	for process in finish_processes:
		if 100*process.execution_time/process.burst >= 100:
			total_waiting += process.waiting_time
			total_turnaround += process.turnaround_time
	row2 = table_cpu.add_row([state,int(current_time),"0%",int(total_waiting/total_process),int(total_turnaround/total_process)], row_background_color='green', cell_padding=15, cell_font_size = 23)
	return row2

def update_job_table(job_list):
	if len(finish_processes) != 0:
		for job in job_list:
			table_job.remove_row(job)
		job_list = []
		show_process = []
		for process in finish_processes:
			if 100*process.execution_time/process.burst >= 100:
				show_process.append(process)
		if len(show_process) > 6:
			num = len(show_process) - 6
			show_process = show_process[num:]
		# else:
		# 	show_process = finish_processes
		for process in show_process:
			if 100*process.execution_time/process.burst >= 100:
				job = table_job.add_row([process.id, int(process.arrive_time), int(process.burst),process.priority,int(process.response_time),int(process.return_time),int(process.waiting_time),int(process.turnaround_time)],
						 row_background_color=(96,96,96),cell_padding=(4,25),cell_font_color = (255,255,255), cell_font_size = 23 )
				job_list.append(job)
	return job_list

def add_real_time_process_GUI(pid, burst, priority, pid_inserting, burst_inserting, priority_inserting,active, color):
	enter_press = False
	for event in pygame.event.get():
      # if user types QUIT then the screen will close 
		if event.type == pygame.MOUSEBUTTONDOWN: 
			if pid_rect.collidepoint(event.pos):
				pid_inserting = True
				burst_inserting = False
				priority_inserting = False
				active = True
			elif burst_rect.collidepoint(event.pos):
				pid_inserting = False
				burst_inserting = True
				priority_inserting = False
				active = True
			elif priority_rect.collidepoint(event.pos):
				pid_inserting = False
				burst_inserting = False
				priority_inserting = True
				active = True
			elif enter_rect.collidepoint(event.pos):
				enter_press = True
				active = True
			else:
				active = False

		if event.type == pygame.KEYDOWN:
			# Check for backspace 
			if event.key == pygame.K_BACKSPACE: 
				# get text input from 0 to -1 i.e. end.
				if pid_inserting:
					pid = pid[:-1]
				elif burst_inserting:
					burst = burst[:-1]
				elif priority_inserting:
					priority = priority[:-1]
			# Unicode standard is used for string formation 
			else:
				if pid_inserting:
					pid += event.unicode
				elif burst_inserting:
					burst += event.unicode
				elif priority_inserting:
					priority += event.unicode
					
		# it will set background color of screen 
	if active:
		color = color_active 
	else: 
		color = color_passive 
	# draw rectangle and argument passed which should 
	# be on screen 
	pygame.draw.rect(screen, color, pid_rect) 
	pygame.draw.rect(screen,color, burst_rect)
	pygame.draw.rect(screen,color,priority_rect)
	pygame.draw.rect(screen,color,enter_rect)
	pid_surface = mediumFont.render(pid, True, (60,19,84)) 
	burst_surface = mediumFont.render(burst, True,(60,19,84))
	priority_surface = mediumFont.render(priority, True,(60,19,84))
	enter_surface = mediumFont.render("Enter", True, (60,19,84))
	screen.blit(pid_surface, (pid_rect.x+5, pid_rect.y+5))
	screen.blit(burst_surface, (burst_rect.x+5, burst_rect.y+5))
	screen.blit(priority_surface, (priority_rect.x+5, priority_rect.y+5))
	screen.blit(enter_surface, (enter_rect.x+15, enter_rect.y+15))
	return pid, burst, priority, pid_inserting, burst_inserting, priority_inserting, active, enter_press

def add_real_process(pid, burst, priority, current_time, GUI_readyqueue, total_process):
	#NOTE: check pid, burst, priority to make sure we have a valid input
	if len(pid) == 0 or not burst.isdigit() or not priority.isdigit():
		return 0,total_process
	new_process = Process(pid, current_time, int(burst), int(priority))
	new_process.update_arrive_time(current_time)
	GUI_readyqueue.insert_process(new_process)
	total_process += 1
	return GUI_readyqueue, total_process

class CPU(pygame.sprite.Sprite):
	def __init__(self) -> None:
		super().__init__()

# Create the group of process
all_sprites_list = pygame.sprite.Group()
# p1 = process("P1", (0,255,255), 50, 100, 100, 100)
# all_sprites_list.add(p1)

# Create QUEUE and CPU regtangle
pygame.draw.rect(screen, (0, 0, 255), [50, 100, 600, 100], 2)
pygame.draw.rect(screen, (255,0,0), [670, 100, 100, 100], 2)
pygame.draw.rect(screen, (255,128,0), [50, 330, 1440, 100], 2)
queue_text = mediumFont.render("QUEUE", True, (32,32,32))
cpu_text = mediumFont.render("CPU", True, (102,0,0))
gantt_text = mediumFont.render("GANTT CHART", True, (204,102,0))
rect_queue_text = queue_text.get_rect()
rect_cpu_text = cpu_text.get_rect()
rect_gantt_text = gantt_text.get_rect()
rect_queue_text.center = (300,70)
rect_cpu_text.center = (700, 70)
rect_gantt_text.center = (750, 280)
screen.blit(queue_text, rect_queue_text)
screen.blit(cpu_text,rect_cpu_text)
screen.blit(gantt_text,rect_gantt_text)
# Update the display for the first time
pygame.display.update()
# Now let's start our main loop
running = True
clock = pygame.time.Clock()

with open("F:\Subjects\os\cpu-scheduling-simulator\process.txt","r") as f:
	lines = f.readlines()
	process_num = int(lines[0][:-1])
	total_process += process_num
	# print("Quantum: ", lines[-1])
	quantum = int(lines[-1])
	lines = lines[1:-1]
	processes = []
	for line in lines:
		info = line[:-1].split(" ")
		process_id = info[0]
		request_time = int(info[1])
		burst_time = int(info[2])
		priority = int(info[3])
		# print(info)
		new_process = Process(process_id,request_time,burst_time,priority)
		new_process.update_arrive_time(request_time)
		processes.append(new_process)

# print(len(processes))
GUI_readyqueue = ReadyQueue(processes)

algo = "FCFS"
start = time.time()
finish_processes = []
job_list = []

# Here we initailize the param and region for adding process at real-time
input_pid = ""
pid_inserting = False
input_burst = ""
burst_inserting = False
input_priority = ""
priority_inserting = False
color_active = pygame.Color('lightskyblue3') 
color_passive = pygame.Color('chartreuse4') 
color = color_passive
pid_rect = pygame.Rect(200, 800, 100, 200)
burst_rect = pygame.Rect(500, 800, 100, 200)
priority_rect = pygame.Rect(800, 800, 100, 200)
enter_rect = pygame.Rect(1000, 800, 100, 200)
active = False
PID_pointer = mediumFont.render("PID:", True, (84,19,19))
PID_pointer_rect = PID_pointer.get_rect()
PID_pointer_rect.center = (175, 830)
burst_pointer = mediumFont.render("Burst time:", True, (84,19,19))
burst_pointer_rect = burst_pointer.get_rect()
burst_pointer_rect.center = (425, 830)
priority_pointer = mediumFont.render("Priority:",True, (84,19,19))
priority_pointer_rect = priority_pointer.get_rect()
priority_pointer_rect.center = (750,830)
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

	# keys = pygame.key.get_pressed()
	# if keys[pygame.K_LEFT]:
	# 	p1.moveLeft(10)
	# if keys[pygame.K_RIGHT]:
	# 	p1.moveRight(10)
 
	# all_sprites_list.update()
	screen.fill(SURFACE_COLOR)
	for entity in all_sprites_list:
		entity.draw_process_box()
		screen.blit(entity.id,entity.rect)
	now = time.time()
	update_ready_queue_GUI(now-start, GUI_readyqueue,algo)
	update_cpu_GUI(now-start, GUI_readyqueue,algo)
	update_gantt_chart_GUI()
	table_cpu.remove_row(row2)
	row2 = update_cpu_table(GUI_readyqueue, now-start)
	job_list = update_job_table(job_list)
	input_pid, input_burst, input_priority, pid_inserting, burst_inserting, priority_inserting,active, enter = \
		  add_real_time_process_GUI(input_pid, input_burst, input_priority, pid_inserting, burst_inserting, priority_inserting,active, color)
	now2 = time.time()
	if enter:
		valid_queue, total_process = add_real_process(input_pid,input_burst,input_priority, now2-start, GUI_readyqueue, total_process)
		if valid_queue != 0:
			GUI_readyqueue = valid_queue
			input_pid = ""
			pid_inserting = False
			input_burst = ""
			burst_inserting = False
			input_priority = ""
			priority_inserting = False
	# We draw some static rectangle and text here
	pygame.draw.rect(screen, (0, 0, 255), [50, 100, 600, 100], 2)
	pygame.draw.rect(screen, (255,0,0), [670, 100, 100, 100], 2)
	pygame.draw.rect(screen, (255,128,0), [50, 330, 1440, 100], 2)
	screen.blit(queue_text, rect_queue_text)
	screen.blit(cpu_text,rect_cpu_text)
	screen.blit(gantt_text,rect_gantt_text)
	screen.blit(PID_pointer,PID_pointer_rect)
	screen.blit(burst_pointer, burst_pointer_rect)
	screen.blit(priority_pointer, priority_pointer_rect)
	menu_cpu.draw(screen)
	menu_job.draw(screen)
	pygame.display.flip()
	clock.tick(29)
 
pygame.quit()
