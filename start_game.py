import pygame 
import os
import sys

DHEIGHT = 720
DWIDTH = 1080
BW = 200
BH = 50

pygame.init()

menu_screen = pygame.display.set_mode((DWIDTH, DHEIGHT))
pygame.display.set_caption("Snake Game Play and AI train")

background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (DWIDTH, DHEIGHT))

font = pygame.font.Font(None, 96)
small_font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, True, color)
    textrect = text_object.get_rect()
    textrect.center = (x, y)
    surface.blit(text_object, textrect)

def play_game():
    pygame.quit()
    os.system('python human_snake_game.py')
    sys.exit()

def train_ai():
    pygame.quit()
    os.system('python agent.py')
    sys.exit()


def main_menu():
    while True:
        menu_screen.blit(background_image, (0, 0))
        draw_text('Snake Game', font, "black", menu_screen, DWIDTH/2, DWIDTH/6)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect((DWIDTH/2)-(BW/2), 250, 200, 50)
        button_2 = pygame.Rect((DWIDTH/2)-(BW/2), 350, 200, 50)
        button_3 = pygame.Rect((DWIDTH/2)-(BW/2), 450, 200, 50)

        if button_1.collidepoint((mx,my)):
            if click:
                play_game()
        if button_2.collidepoint((mx, my)):
            if click:
                train_ai()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(menu_screen, "#3CB371", button_1)
        pygame.draw.rect(menu_screen, "#2E8B57", button_2)
        pygame.draw.rect(menu_screen, "#800000", button_3)

        draw_text("Play Game", small_font, "BLACK", menu_screen, (DWIDTH/2), 275)
        draw_text("Train AI", small_font, "BLACK", menu_screen, (DWIDTH/2), 375)
        draw_text("Quit", small_font, "BLACK", menu_screen, (DWIDTH/2), 475)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


if __name__ == "__main__":
    main_menu()

