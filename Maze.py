#! /usr/bin/env python

import os
import random
import pygame

# Class for the orange dude --> learner sprite
class Player(object):
    
	# keep track of pathway for each sprite

	def __init__(self):
		self.rect = pygame.Rect(32, 32, 16, 16)
	'''
	def move(self, dx, dy):
    	# Move each axis separately. Note that this checks for collisions both times.
		print("dx, dy: ", dx, dy)
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)
	'''
	def move_single_axis(self, dx, dy):
		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom
	
	# check to see all possible pathways for Sprite at current position
	def checkPos(self, dx, dy):

		player_temp = self
	
		# Move the Sprite
		player_temp.rect.x += 16 # FIGURE OUT: how to deal with taking away dx, dy
		player_temp.rect.y += 0

		player_temp.RIGHT = True
		player_temp.LEFT = True
		player_temp.DOWN = True
		player_temp.UP = True

		# you have to account for where it's coming from,
		# but that can be implemented with a path follower

		# Checks if you collide with a wall
		for wall in walls:
			done = False
			while done != True:
				if self.rect.colliderect(wall.rect):
								
					if dx > 0: # Moving right; Hit the left side of the wall
						self.rect.right = wall.rect.left
						player_temp.RIGHT = False
						player_temp.rect.x -= 32 # x = -16, y = 0  
					if dx < 0: # Moving left; Hit the right side of the wall
						self.rect.left = wall.rect.right
						player_temp.LEFT = False
						player_temp.rect.x += 16
						player_temp.rect.y -= 16 # x = 0, y = -16	
					if dy > 0: # Moving down; Hit the top side of the wall
						self.rect.bottom = wall.rect.top
						player_temp.DOWN = False
						player_temp.rect.y += 32 # x = 0, y = 16
					if dy < 0: # Moving up; Hit the bottom side of the wall
						self.rect.top = wall.rect.bottom
						player_temp.UP = False
				done = True			
		# Return possible moves
		return player_temp.RIGHT, player_temp.LEFT, player_temp.DOWN, player_temp.UP		

# Nice class to hold a wall rect
class Wall(object):
    
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Maze Runner")
screen = pygame.display.set_mode((320, 240))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
"WWWWWWWWWWWWWWWWWWWW",
"W                  W",
"W         WWWWWW   W",
"W   WWWW       W   W",
"W   W        WWWW  W",
"W WWW  WWWW        W",
"W   W     W W      W",
"W   W     W   WWW WW",
"W   WWW WWW   W W  W",
"W     W   W   W W  W",
"WWW   W   WWWWW W  W",
"W W      WW        W",
"W W   WWWW   WWW   W",
"W     W    E   W   W",
"WWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
	for col in row: # go through each row 
		if col == "W": 
			Wall((x, y))
		if col == "E":
			end_rect = pygame.Rect(x, y, 16, 16)
		x += 16 # go to next "block" in row
	y += 16 # go to next row
	x = 0 # start at beginning of row

running = True
while running: # while not at the end of the maze
    
	clock.tick(60)
    
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			running = False
	'''
	Sprite checks to see how many options it has to move (up, down, right, left)
		the direction behind the Sprite does not count as an option
	'''
	player.checkPos() # checks ever possible future position
	'''
	If options n is > 1, create n - 1 Sprites to follow those other directions,
		direct the original Sprites direction up until then to the new Sprite(s)
	If options n is = 0, kill that Sprite and save that direction as invalid
	'''    
	
	
	# Move the playeri if an arrow key is pressed
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		player.move_single_axis(-16, 0) 	
	if key[pygame.K_RIGHT]:
		player.move_single_axis(16, 0)
	if key[pygame.K_UP]:
		player.move_single_axis(0, -16)
	if key[pygame.K_DOWN]:
		player.move_single_axis(0, 16)
    
	# Just added this to make it slightly fun ;)
	if player.rect.colliderect(end_rect):
		raise SystemExit, "You win!"
    
	# Draw the scene
	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (104, 196, 210), wall.rect)
	pygame.draw.rect(screen, (122, 68, 230), end_rect)
	pygame.draw.rect(screen, (239, 163, 97), player.rect)
	pygame.display.flip()
