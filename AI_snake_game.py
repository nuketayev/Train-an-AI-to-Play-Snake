import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np


pygame.init()

font = pygame.font.SysFont('arial', 25)
font_info = pygame.font.SysFont('arial', 15)

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

BLOCK_SIZE = 20
DHEIGHT = 720
DWIDTH = 1080
INFO_ZONE_HEIGHT = 80
PLAY_ZONE_HEIGHT = DHEIGHT - INFO_ZONE_HEIGHT


class SnakeGameAI:

    def __init__(self, height = DHEIGHT, width=DWIDTH):
        self.w = width
        self.h = height
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()
        self.record = 0
        self.nb_games = -1
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.snake_head = Point(self.w / 2, INFO_ZONE_HEIGHT + (PLAY_ZONE_HEIGHT / 2))
        self.snake = [self.snake_head,
                      Point(self.snake_head.x,(self.snake_head.y - BLOCK_SIZE)),
                      Point(self.snake_head.x,(self.snake_head.y - (BLOCK_SIZE * 2)))]

        self.score = 0
        self.nb_games += 1
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, ((self.w - BLOCK_SIZE) // BLOCK_SIZE)) * BLOCK_SIZE
        y = random.randint(INFO_ZONE_HEIGHT // BLOCK_SIZE, ((self.h - BLOCK_SIZE) // BLOCK_SIZE)) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action, SPEED):
        self.frame_iteration += 1
        self.snake_speed = SPEED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._move(action)
        self.snake.insert(0, self.snake_head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.snake_head == self.food:
            self.score += 1
            if self.record < self.score:
                self.record = self.score
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(self.snake_speed)

        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake_head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < INFO_ZONE_HEIGHT:
            return True
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill("black")
        self.display.fill("#202020", (0, 0, self.w, INFO_ZONE_HEIGHT))


        for pt in self.snake:
            pygame.draw.rect(self.display, "BLUE", pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, "GREEN", pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, "RED", pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, "GREEN", pygame.Rect(self.food.x+(BLOCK_SIZE/2), self.food.y, BLOCK_SIZE/3, BLOCK_SIZE/3))
        text = font.render("Game: " + str(self.nb_games), True, "RED")
        self.display.blit(text, [BLOCK_SIZE, BLOCK_SIZE])
        text = font.render("Score: " + str(self.score), True, "WHITE")
        self.display.blit(text, [BLOCK_SIZE * 8, BLOCK_SIZE])
        text = font.render("Record: " + str(self.record), True, "WHITE")
        self.display.blit(text, [BLOCK_SIZE * 15, BLOCK_SIZE])
        text = font.render("Speed: " + str(self.snake_speed) + " units/s", True, "WHITE")
        self.display.blit(text, [BLOCK_SIZE * 22, BLOCK_SIZE])
        text = font_info.render("Press Q - quit   |   W/UP - increase speed   |   S/DOWN - reduce speed   |   SPACE - set speed 300 units/s   |   R - reset speed", True, "WHITE")
        self.display.blit(text, [BLOCK_SIZE, BLOCK_SIZE * 2.8])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.snake_head.x
        y = self.snake_head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.snake_head = Point(x, y)