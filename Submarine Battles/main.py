import pygame
import pygame.locals
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Submarine Battles")

WHITE = 255,255,255
BLACK = 0,0,0
gray = 255,0,0
YELLOW = 255,255,0
border = pygame.Rect(WIDTH//2 ,0, 10, HEIGHT)

health_font = pygame.font.SysFont("comicsans", 45)
winner_font = pygame.font.SysFont("futura", 75)

fps = 60
vel = 5
missile_vel = 7
max_missiles = 5
player_width = 55
player_height = 40
yellow_hit = pygame.USEREVENT+1
gray_hit = pygame.USEREVENT+2

gray_sub_img = pygame.image.load("./images/gray-sub.png")
gray_sub_scale = pygame.transform.scale(gray_sub_img, (player_width, player_height))
gray_sub = pygame.transform.rotate(gray_sub_scale, 270)

yellow_sub_img = pygame.image.load("./images/yellow-sub.png")
yellow_sub_scale = pygame.transform.scale(yellow_sub_img, (player_width, player_height))
yellow_sub = pygame.transform.rotate(yellow_sub_scale, 90)

bg = pygame.image.load("./images/pixelwater.png")
bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))

def draw_screen(gray,yellow,gray_missile,yellow_missile,gray_health,yellow_health,bg):
    screen.blit(bg_scaled, (0,0))
    pygame.draw.rect(screen, WHITE, border)
    gray_health_text = health_font.render("Health: " + str(gray_health), 1, WHITE)
    yellow_health_text = health_font.render("Health: " + str(yellow_health), 1, WHITE)
    screen.blit(gray_health_text, (WIDTH-gray_health_text.get_width()-10, 20))
    screen.blit(yellow_health_text, (10, 20))
    screen.blit(yellow_sub, (yellow.x,yellow.y))
    screen.blit(gray_sub, (gray.x, gray.y))

    for missile in gray_missile:
        pygame.draw.rect(screen, gray, missile)
    
    for missile in yellow_missile:
        pygame.draw.rect(screen, YELLOW, missile)
    
def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0:
        yellow.x -=  vel
    elif keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < border.x:
        yellow.x += vel
    elif keys_pressed[pygame.K_w] and yellow.y - vel > 0:
        yellow.y -=  vel
    elif keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < HEIGHT - 15:
        yellow.y += vel
    
def handle_gray_movement(keys_pressed, gray):
    if keys_pressed[pygame.K_LEFT] and gray.x - vel > border.x + border.width:
        gray.x -=  vel
    elif keys_pressed[pygame.K_RIGHT] and gray.x + vel + gray.width < WIDTH:
        gray.x += vel
    elif keys_pressed[pygame.K_UP] and gray.y - vel > 0:
        gray.y -=  vel
    elif keys_pressed[pygame.K_DOWN] and gray.y + vel + gray.height < HEIGHT - 15:
        gray.y += vel

def handle_missiles(yellow_missiles, yellow, gray_missiles, gray):
    for missile in yellow_missiles:
        missile.x += missile_vel
        if gray.colliderect(missile):
            yellow_missiles.remove(missile)
            pygame.event.post(pygame.event.Event(gray_hit))
        elif missile.x > WIDTH:
            yellow_missiles.remove(missile)
    
    for missile in gray_missiles:
        missile.x -= missile_vel
        if yellow.colliderect(missile):
            gray_missiles.remove(missile)
            pygame.event.post(pygame.event.Event(yellow_hit))
        elif missile.x < 0:
            gray_missiles.remove(missile)