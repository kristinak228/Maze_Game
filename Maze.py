#! /usr/bin/env python

import os
import random
import pygame
import time as t

# Class for sprite
class Player(object):
	
	# Initialize the Sprite
	def __init__(self):
		self.rect = pygame.Rect(32, 32, 0, 0) # 16, 16)

	# Moves the Sprite
	def move(self, dx, dy):
	# Move each axis separately. Note that this checks for collisions both times.
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)
	# checks for collision via the array
	def isSafe(self, level, dx, dy, sol):
		# Get maze size
		X = len(level[0])
		Y = len(level)
		if dx >= 0 and dx < X and dy >= 0 and dy < Y and level[dx][dy] != 0: # "W":
			self.move(dx, dy) # you have made a successful move
			return True
		return False

	# Recursively calls itself until it has ended the maze
	def solveMaze(self, level, dx, dy, sol):
		# Get maze size
		X = len(level[0])
		Y = len(level)
		# check if player has reached the end
		if (dx == X-1 and dy == Y-1):
			sol[dx][dy] = 1
			return True
		# check if we're inside the maze
		if self.isSafe(level, dx, dy, sol):
			# Mark the current cell (Backtrack)
			sol[dx][dy] = 1
			# Move right
			pygame.display.update()
			if self.solveMaze(level, dx+1, dy, sol):
				return True
			# Move down
			pygame.display.update()
			if self.solveMaze(level, dx, dy+1, sol):
				return True
			# if you can't move right or down, you've hit a wall
			sol[dx][dy] = 0
			return False

	# checks for collision via the sprite and walls
	def move_single_axis(self, dx, dy):
		# Move the player
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

# wall object
class Wall(object):
    
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Maze Runner")
screen = pygame.display.set_mode((256, 256)) # 320, 240 OR 64, 64

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
	[1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
	[1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
	[1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
	[1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
	[1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
	[0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
	[1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
	[1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

]
# Update this as you go through to show were the path(s) are
sol = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
	for col in row: # go through each row 
		if col == 0: # "W": 
			Wall((x, y))
		if col == 1: # "E":
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
	
	if player.solveMaze(level, 0, 0, sol):
		print(sol)

	else:
		print("No Solution")
	print("YOU WIN")

	t.sleep(3) # display game for 5 secs after completion
	running = False







