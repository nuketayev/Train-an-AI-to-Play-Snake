import pygame
from collections import namedtuple
from enum import Enum
import random
import math
import time

pygame.init()

Point = namedtuple("Point","x, y")

font_score = pygame.font.SysFont('arial', 30)
font_restart = pygame.font.SysFont('arial', 80)
font_button = pygame.font.SysFont('arial', 30)
font_info = pygame.font.SysFont('arial', 15)

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

BOX_SIZE = 20
DHEIGHT = 720
DWIDTH = 1080
INFO_ZONE_HEIGHT = 80
PLAY_ZONE_HEIGHT = DHEIGHT - INFO_ZONE_HEIGHT
SPEED = 20

class MyButton:
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, "WHITE")
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Game:

    def __init__(self, height = DHEIGHT, width=DWIDTH):
        self.display_hight = height
        self.display_width = width

        self.direction = Direction.DOWN
        self.next_direction = self.direction

        self.display = pygame.display.set_mode((self.display_width, self.display_hight))
        self.surface = pygame.Surface((self.display_width, self.display_hight), pygame.SRCALPHA)
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.snake_head = Point(self.display_width/2, INFO_ZONE_HEIGHT + (PLAY_ZONE_HEIGHT / 2))
        self.snake = [self.snake_head,
                      Point(self.snake_head.x,(self.snake_head.y - BOX_SIZE)),
                      Point(self.snake_head.x,(self.snake_head.y - (BOX_SIZE * 2)))]

        self.score = 0
        self.record = 0
        
        self.food = None
        self.spawn_food()

        self.restart_button = MyButton(self.display_width - 120, 10, 100, 40, "restart", font_button, "#660000", "red")
        self.pause_button = MyButton(self.display_width - 230, 10, 100, 40, "pause", font_button, "#4fc3f7", "red")

        self.arrow_image = pygame.image.load("arrow.png")
        self.arrow_image = pygame.transform.scale(self.arrow_image, (30, 30))
        self.degree = 0
        self.paused = False
        self.nowall_mode = False
        self.nowall_mode_status = "OFF"

    def reset(self):
        self.direction = Direction.DOWN
        self.next_direction = self.direction
        self.snake_head = Point(self.display_width/2, self.display_hight/2)
        self.snake = [self.snake_head,
                      Point(self.snake_head.x,(self.snake_head.y - BOX_SIZE)),
                      Point(self.snake_head.x,(self.snake_head.y - (BOX_SIZE * 2)))]
        self.score = 0
        self.food = None
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, ((self.display_width - BOX_SIZE) // BOX_SIZE)) * BOX_SIZE
        y = random.randint(INFO_ZONE_HEIGHT // BOX_SIZE, ((self.display_hight - BOX_SIZE) // BOX_SIZE)) * BOX_SIZE
        self.food = Point(x, y)
  
        if self.food in self.snake:
            self.spawn_food()
        

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    self.reset()
                    return False, self.score
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_SPACE:
                    self.nowall_mode = not self.nowall_mode
                    if self.nowall_mode:
                        self.nowall_mode_status = "ON"
                    else:
                        self.nowall_mode_status = "OFF"
                if not self.paused:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
            if self.restart_button.is_clicked(event):
                self.reset()
                return False, self.score
            if self.pause_button.is_clicked(event):
                self.paused = not self.paused

        if self.paused:
            self.draw_pause_menu()
            return False, self.score

        if (self.next_direction == Direction.UP and self.direction != Direction.DOWN) or \
        (self.next_direction == Direction.DOWN and self.direction != Direction.UP) or \
        (self.next_direction == Direction.LEFT and self.direction != Direction.RIGHT) or \
        (self.next_direction == Direction.RIGHT and self.direction != Direction.LEFT):
            self.direction = self.next_direction
                
        self.move()
        self.snake.insert(0, self.snake_head)

        gameIsOver = False
        if self.isCollition():
            gameIsOver = True
            self.countdown()
            self.reset()
            return gameIsOver, self.score
        
        if self.snake_head == self.food:
            self.score += 1
            if self.record <= self.score:
                self.record = self.score
            self.spawn_food()
        else:
            self.snake.pop()

        if self.score < 5: 
            self.speed = SPEED
        elif self.score >= 5 and self.score < 10:
            self.speed = SPEED * 1.5
        else:
            self.speed = SPEED * 2

        self.toward_food()
        self.update_ui()
        self.clock.tick(self.speed)

        return gameIsOver, self.score

    def isCollition(self):
        if not self.nowall_mode:
            if self.snake_head.x < 0 or self.snake_head.x > (self.display_width - BOX_SIZE):
                return True
            if self.snake_head.y < INFO_ZONE_HEIGHT or self.snake_head.y > (self.display_hight - BOX_SIZE):
                return True
            
        if self.snake_head in self.snake[1:]:
            print("Snake ate itself")
            return True
        return False

    def draw_pause_menu(self):
        self.surface.fill((0,0,0,0))
        pygame.draw.rect(self.surface, (32, 32, 32, 5), [0, 0, self.display_width, self.display_hight])
        self.display.blit(self.surface, (0, 0))
        pause_text = font_restart.render("PAUSED", True, "WHITE")
        self.display.blit(pause_text, [self.display_width // 2 - pause_text.get_width() // 2, self.display_hight // 2 - pause_text.get_height() // 2 - 40])
        
        resume_text = font_score.render("Press ESC to resume", True, "WHITE")
        self.display.blit(resume_text, [self.display_width // 2 - resume_text.get_width() // 2, self.display_hight // 2 - resume_text.get_height() // 2 + 40])
    
        pygame.display.flip()

    def toward_food(self):
        x = abs(self.food.x - self.snake_head.x)
        y = abs(self.food.y - self.snake_head.y)
        right_angle = 90
        
        if self.food.x >= self.snake_head.x and self.food.y <= self.snake_head.y:
            radians = math.atan2(y, x)
            self.degree = math.degrees(radians)
        elif self.food.x <= self.snake_head.x and self.food.y <= self.snake_head.y:
            radians = math.atan2(x, y)
            self.degree = (math.degrees(radians) + right_angle)
        elif self.food.x <= self.snake_head.x and self.food.y >= self.snake_head.y:
            radians = math.atan2(y, x)
            self.degree = (math.degrees(radians) + (right_angle * 2))
        elif self.food.x >= self.snake_head.x and self.food.y >= self.snake_head.y:
            radians = math.atan2(x, y)
            self.degree = (math.degrees(radians) + (right_angle * 3))

        # if (self.food.x + BOX_SIZE * 3) < self.snake_head.x and (self.food.y - BOX_SIZE * 3) > self.snake_head.y:
        #     self.arrow_direction = "↙"
        # elif (self.food.x - BOX_SIZE * 3) > self.snake_head.x and (self.food.y - BOX_SIZE * 3) > self.snake_head.y:
        #     self.arrow_direction = "↘"
        # elif (self.food.x - BOX_SIZE * 3) > self.snake_head.x and (self.food.y + BOX_SIZE * 3) < self.snake_head.y:
        #     self.arrow_direction = "↗"
        # elif (self.food.x + BOX_SIZE * 3) < self.snake_head.x and (self.food.y + BOX_SIZE * 3) < self.snake_head.y:
        #     self.arrow_direction = "↖"
        # elif (self.food.x + BOX_SIZE * 3) < self.snake_head.x:
        #     self.arrow_direction = "←"
        # elif (self.food.x - BOX_SIZE * 3) > self.snake_head.x:
        #     self.arrow_direction = "→"
        # elif (self.food.y + BOX_SIZE * 3) < self.snake_head.y:
        #     self.arrow_direction = "↑"
        # elif (self.food.y - BOX_SIZE * 3) > self.snake_head.y:
        #     self.arrow_direction = "↓"

    def rotate_arrow(self, angle):
        rotated_image = pygame.transform.rotate(self.arrow_image, angle)
        new_rect = rotated_image.get_rect(center=self.arrow_image.get_rect(topleft=((self.display_width / 2) - (self.arrow_image.get_width() / 2), BOX_SIZE-5)).center)
        return rotated_image, new_rect
        # if direction == "↙":
        #     return pygame.transform.rotate(self.arrow_image, 225)
        # elif direction == "↘":
        #     return pygame.transform.rotate(self.arrow_image, 315)
        # elif direction == "↗":
        #     return pygame.transform.rotate(self.arrow_image, 45)
        # elif direction == "↖":
        #     return pygame.transform.rotate(self.arrow_image, 135)
        # elif direction == "←":
        #     return pygame.transform.rotate(self.arrow_image, 180)
        # elif direction == "→":
        #     return pygame.transform.rotate(self.arrow_image, 0)
        # elif direction == "↑":
        #     return pygame.transform.rotate(self.arrow_image, 90)
        # elif direction == "↓":
        #     return pygame.transform.rotate(self.arrow_image, 270)

        

    def update_ui(self):
        self.display.fill("#202020", (0, 0, self.display_width, INFO_ZONE_HEIGHT))
        text_score = font_score.render("Score: " + str(self.score), True, "GOLD")
        self.display.blit(text_score, [BOX_SIZE, BOX_SIZE])
        text_keys = font_info.render("Press Q - quit   |   R - restart   |   ESC - pause   |   WASD/Arrows - move   |   SPACE - no wall mode",
                                      True, "WHITE")
        self.display.blit(text_keys, [BOX_SIZE, BOX_SIZE*2.8])
        text_speed = font_info.render(f"Speed: {int(self.speed)} units/s", True, "white")
        self.display.blit(text_speed, [650, BOX_SIZE-5])
        text_mode = font_info.render(f"No wall mode: {self.nowall_mode_status}", True, "white")
        self.display.blit(text_mode, [650, BOX_SIZE*2])
        rotated_arrow, new_rect = self.rotate_arrow(self.degree)
        text_record = font_score.render(f"Record: {int(self.record)}", True, "#4fc3f7")
        self.display.blit(text_record, [160, BOX_SIZE])
        self.restart_button.draw(self.display)
        self.pause_button.draw(self.display)

        self.display.fill("black", (0, INFO_ZONE_HEIGHT, self.display_width, self.display_hight))
        for pt in self.snake:
            pygame.draw.rect(self.display, "BLUE", pygame.Rect(pt.x, pt.y, BOX_SIZE, BOX_SIZE))
            pygame.draw.rect(self.display, "GREEN", pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        pygame.draw.rect(self.display, "RED", pygame.Rect(self.food.x, self.food.y, BOX_SIZE, BOX_SIZE))
        pygame.draw.rect(self.display, "GREEN", pygame.Rect(self.food.x+(BOX_SIZE/2), self.food.y, BOX_SIZE/3, BOX_SIZE/3))
        pygame.draw.circle(self.display, "white", [new_rect.centerx, new_rect.centery], 20, 0)
        self.display.blit(rotated_arrow, new_rect.topleft)
        pygame.display.flip()

    def move(self):
        x = self.snake_head.x
        y = self.snake_head.y
        if self.nowall_mode:
            if self.direction == Direction.RIGHT and self.snake_head.x >= self.display_width - BOX_SIZE:
                x = 0
            elif self.direction == Direction.LEFT and self.snake_head.x < 0:
                x = self.display_width - BOX_SIZE
            elif self.direction == Direction.UP and self.snake_head.y <= INFO_ZONE_HEIGHT:
                y = self.display_hight - BOX_SIZE
            elif self.direction == Direction.DOWN and self.snake_head.y >= self.display_hight - BOX_SIZE:
                y = INFO_ZONE_HEIGHT
            else:
                if self.direction == Direction.UP:
                    y -= BOX_SIZE
                if self.direction == Direction.DOWN:
                    y += BOX_SIZE
                if self.direction == Direction.RIGHT:
                    x += BOX_SIZE
                if self.direction == Direction.LEFT:
                    x -= BOX_SIZE
        else:
            if self.direction == Direction.UP:
                y -= BOX_SIZE
            if self.direction == Direction.DOWN:
                y += BOX_SIZE
            if self.direction == Direction.RIGHT:
                x += BOX_SIZE
            if self.direction == Direction.LEFT:
                x -= BOX_SIZE

        self.snake_head = Point(x, y)

    def countdown(self):
        for i in range(3, 0, -1):
            self.display.fill("BLACK")

            game_over_text = font_restart.render("GAME OVER", True, "RED")
            self.display.blit(game_over_text, [self.display_width // 2 - game_over_text.get_width() // 2, self.display_hight // 2 - game_over_text.get_height() // 2 - 40])
            
            countdown_text = font_score.render(f"restart in {i}", True, "WHITE")
            self.display.blit(countdown_text, [self.display_width // 2 - countdown_text.get_width() // 2, self.display_hight // 2 - countdown_text.get_height() // 2 + 40])
            
            pygame.display.flip()
            time.sleep(0.5)
        self.reset()

if __name__ == "__main__":
    game = Game()

    while True:
        gameIsOver, score = game.play_step()
        if gameIsOver:
            continue

pygame.quit()