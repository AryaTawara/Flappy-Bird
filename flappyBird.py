import pygame
import time
import random
import sys

pygame.init()
game_font = pygame.font.Font('Flappy Bird/04B_19.ttf', 30)

#window
dis_width = 288
dis_length = 512
dis = pygame.display.set_mode((dis_width, dis_length))

#bird
bird1 = pygame.image.load("Flappy Bird/bird1.png")
bird2 = pygame.image.load("Flappy Bird/bird2.png")
bird3 = pygame.image.load("Flappy Bird/bird3.png")
bird_frames = [bird1, bird2, bird3]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

#background and base
bg = pygame.image.load("Flappy Bird/bg.png")
base = pygame.image.load("Flappy Bird/base.png")

#pipes
pipe_surface = pygame.image.load("Flappy Bird/pillar.png")
pipe_list = []
pipe_pos = [200, 250, 300, 350, 400]
SPWANPIPE = pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE, 1000)

#game over screen
game_over = pygame.image.load("Flappy Bird/message.png")
game_over_rect = game_over.get_rect(center = (144, 240))

#window title and icon
pygame.display.set_icon(bird1)
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

x1_change_base = 0

gravity = 0.26
bird_movement = 0

score = 0
high_score = 0
game_active = True

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, [255, 255, 255])
        score_rect = score_surface.get_rect(center = (144, 50))
        score_surface1 = game_font.render(str(int(score)), True, [0, 0, 0])
        score_rect1 = score_surface.get_rect(center = (147, 53))
        dis.blit(score_surface1, score_rect1)
        dis.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'SCORE: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        score_surface1 = game_font.render(f'SCORE: {int(score)}', True, (0, 0, 0))
        score_rect1 = score_surface.get_rect(center = (147, 53))
        dis.blit(score_surface1, score_rect1)
        dis.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'HIGH SCORE: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (144, 425))
        high_score_surface1 = game_font.render(f'HIGH SCORE: {int(high_score)}', True, (0, 0, 0))
        high_score_rect1 = high_score_surface.get_rect(center = (147, 428))
        dis.blit(high_score_surface1, high_score_rect1)
        dis.blit(high_score_surface, high_score_rect)

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

def roate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -5, 1)
    return new_bird

def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            time.sleep(0.5)
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        time.sleep(0.5)
        return False

    return True    

def create_pipe():
    pipe_y = random.choice(pipe_pos)
    bottom_pipe = pipe_surface.get_rect(midtop = (300, pipe_y))
    top_pipe = pipe_surface.get_rect(midbottom = (300, pipe_y - 150))
    return bottom_pipe, top_pipe

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            dis.blit(pipe_surface, pipe)
        else:
            fliped_pipe = pygame.transform.flip(pipe_surface, False, True)
            dis.blit(fliped_pipe, pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_floor():
    dis.blit(base, (x1_change_base, 450))
    dis.blit(base, (x1_change_base + 288, 450))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                score = 0
                pipe_list.clear()
                bird_rect.center = (50, 256)
                
        if event.type == SPWANPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    dis.blit(bg, (0, 0))
    if game_active:
        #bird
        bird_movement += gravity
        roated_bird = roate_bird(bird_surface)
        bird_rect.centery += bird_movement
        dis.blit(roated_bird, bird_rect)
        game_active = collision(pipe_list)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.0099
        high_score = update_score(score, high_score)
        score_display('main_game')
    else:
        dis.blit(game_over, game_over_rect)
        score_display('game_over')
    #floor
    x1_change_base -= 3

    if x1_change_base < -288:
        x1_change_base = 0
    
    draw_floor()

    pygame.display.update()
    clock.tick(90)

pygame.quit()
quit()
