import pygame
# Fuck config file all my homies hardcode FUCK config file
screen_width = 1280
screen_height = 720
tile_size_x = 32
tile_size_y = 30
FPS = 60
gravity = 11
amount = 30
RUNNING = True
falling = True

radius = 20
acceleration = amount
delta_time = 1/1000
jump_strength = 500

start_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
color_1 = "#E8181C"

