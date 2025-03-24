import pygame
import random
from pygame.constants import QUIT
import time

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDHT = 1200

COLLOR_WHITE = (225, 225, 225)
COLLOR_BLACK = (0, 0, 0)
COLLOR_BLUE = (0, 0, 255)
COLLOR_GREEN = (0, 255, 0)
BUTTON_COLOR = (100, 100, 255)

SIZE = (30, 30)
BUTTON_SIZE = (150, 50)

main_display = pygame.display.set_mode((WIDHT, HEIGHT))


class Item:
    def __init__(self, color):
        self.size = SIZE
        self.color = color
        self.rect = pygame.Rect(random.randint(0, WIDHT - SIZE[0]), random.randint(0, HEIGHT - SIZE[1]), *SIZE)
        self.speed = [random.choice([1, 1]), random.choice([1, -1])]

    def draw(self, main_display):
        pygame.draw.rect(main_display, self.color, self.rect)

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.bottom >= HEIGHT:
            self.speed = random.choice(([1, -1], [-1, -1]))
        if self.rect.top <= 0:
            self.speed = random.choice(([-1, 1], [1, 1]))
        if self.rect.right >= WIDHT:
            self.speed = random.choice(([-1, -1], [-1, 1]))
        if self.rect.left <= 0:
            self.speed = random.choice(([1, 1], [1, -1]))

class Stone(Item):
    def __init__(self):
        super().__init__(COLLOR_WHITE)

class Scissors(Item):
    def __init__(self):
        super().__init__(COLLOR_BLUE)

class Paper(Item):
    def __init__(self):
        super().__init__(COLLOR_GREEN)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 26)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)
        display.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def check_collision(obj1, obj2):
    if isinstance(obj1, Stone) and isinstance(obj2, Paper):
        return obj1.rect.colliderect(obj2.rect)
    if isinstance(obj1, Paper) and isinstance(obj2, Scissors):
        return obj1.rect.colliderect(obj2.rect)
    if isinstance(obj1, Stone) and isinstance(obj2, Scissors):
        return obj1.rect.colliderect(obj2.rect)
    return False


add_stone_button = Button(WIDHT - BUTTON_SIZE[0] - 10, HEIGHT - BUTTON_SIZE[1] - 10, BUTTON_SIZE[0], BUTTON_SIZE[1],
                          'ADD STONE', BUTTON_COLOR, COLLOR_BLACK)
add_paper_button = Button(WIDHT - BUTTON_SIZE[0] - 10, HEIGHT - BUTTON_SIZE[1] - 70, BUTTON_SIZE[0], BUTTON_SIZE[1],
                          'ADD PAPER', BUTTON_COLOR, COLLOR_BLACK)
add_scissors_button = Button(WIDHT - BUTTON_SIZE[0] - 10, HEIGHT - BUTTON_SIZE[1] - 140, BUTTON_SIZE[0], BUTTON_SIZE[1],
                             'ADD SCISSORS', BUTTON_COLOR, COLLOR_BLACK)
play_button = Button(WIDHT - BUTTON_SIZE[0] - 10, HEIGHT - BUTTON_SIZE[1] - 210, BUTTON_SIZE[0], BUTTON_SIZE[1], 'PLAY',
                     BUTTON_COLOR, COLLOR_BLACK)
stones = []
scissorses = []
papers = []
playing = True
game_start = False
while playing:
    FPS.tick(600)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if add_stone_button.is_clicked(mouse_pos):
                stones.append(Stone())
            if add_paper_button.is_clicked(mouse_pos):
                papers.append(Paper())
            if add_scissors_button.is_clicked(mouse_pos):
                scissorses.append(Scissors())
            if play_button.is_clicked(mouse_pos):
                game_start = True
    main_display.fill(COLLOR_BLACK)

    for stone in stones[:]:
        for paper in papers[:]:
            if check_collision(stone, paper):
                stones.remove(stone)
                print(f'STONES {len(stones)}')
    for scissrs in scissorses[:]:
        for stone in stones[:]:
            if check_collision(stone, scissrs):
                scissorses.remove(scissrs)
                print(f'SCISSORSES {len(scissorses)}')
    for paper in papers[:]:
        for scissors in scissorses[:]:
            if check_collision(paper, scissors):
                papers.remove(paper)
                print(f'PAPERS {len(papers)}')

    for stone in stones:
        if game_start:
            stone.move()
        stone.draw(main_display)
    for scisors in scissorses:
        if game_start:
            scisors.move()
        scisors.draw(main_display)
    for paper in papers:
        if game_start:
            paper.move()
        paper.draw(main_display)

    add_stone_button.draw(main_display)
    add_paper_button.draw(main_display)
    add_scissors_button.draw(main_display)
    play_button.draw(main_display)
    pygame.display.flip()