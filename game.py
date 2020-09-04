# Created by Mr Malaitai
# Date: 31/08/2020
import pygame, sys
from pygame.locals import *

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
    
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

clock = pygame.time.Clock()
pygame.init() # initiates pygame
pygame.display.set_caption('Pygame Platformer')
WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
true_scroll = [0,0]
game_map = load_map('map')
grass_img = pygame.image.load('images/grass.png')
dirt_img = pygame.image.load('images/dirt.png')
player_img = pygame.image.load('images/player.png').convert()

jump_sound = pygame.mixer.Sound('audio/jump.wav')

pygame.mixer.music.load('audio/music.wav') # Audio for music
pygame.mixer.music.play(-1) # Play the audio for music.  -1 is so that it loops indefinitely

player_img.set_colorkey((255,255,255))
player_rect = pygame.Rect(100,100,5,13)


while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue
    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20 # a number lower than 20 speeds up the parallax
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20 # a number higher than 20 slows down the parallax
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2 # Player speed moving to the right
    if moving_left == True:
        player_movement[0] -= 2 # Player speed moving to the left
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2 # Time in the air
    if vertical_momentum > 3:
        vertical_momentum = 3
    player_rect,collisions = move(player_rect,player_movement,tile_rects)
    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1
    display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                jump_sound.play() # Plays the jump sound when pressing up
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)