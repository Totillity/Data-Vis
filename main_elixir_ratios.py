from typing import List, Tuple
import math

import pygame


pygame.init()


SORT_METHOD = lambda data_tuple: data_tuple[0]
# 0 is damage dealt, 1 is card name, 2 is damage/elixir ratio, 3 is cost
REVERSED = False

CARD_BAR_HEIGHT = 25
SEP_BAR_WIDTH = 3
MAX_BAR_WIDTH = 1000
TOTAL_BAR_WIDTH = MAX_BAR_WIDTH + SEP_BAR_WIDTH
MAX_PRINCESS_WIDTH = MAX_BAR_WIDTH * 2534//(2534 + 4008)
MAX_KING_WIDTH = MAX_BAR_WIDTH * 4008//(2534 + 4008)
PIXELS_PER_HEALTH = MAX_PRINCESS_WIDTH/2534
BORDERS = 20
BK = (32, 32, 32)
BK = (255, 255, 255)

font = pygame.font.SysFont("impact", CARD_BAR_HEIGHT)

COLOR_1 = pygame.Color(20, 20, 200)
COLOR_2 = pygame.Color(200, 200, 0)
COLOR_3 = pygame.Color(220, 0, 0)
COLOR_OFFSET = pygame.Color(30, 30, 30)


data: List[Tuple[int, str, float, int]] = []

with open("data.txt", "r") as data_file:

    for card in data_file.readlines():
        # print(card)
        attrs = card.split()

        if len(attrs) > 1:
            card_name: str = attrs[0]
            king: bool = len(attrs) >= 4
            if king:
                damage: int = int(attrs[1]) + 2534
            else:
                damage: int = int(attrs[1])
            cost = int(attrs[-1])
            ratio = damage / cost

            data.append((damage, card_name, ratio, cost))

data.sort(key=SORT_METHOD, reverse=REVERSED)


names: List[pygame.Surface] = [font.render(name.replace("_", " "), True, (255, 255, 255)) for _, name, __, ___ in data]
MAX_TEXT_WIDTH = max(name.get_width() for name in names) + SEP_BAR_WIDTH*2  # sep bar width for some elbow room
MAX_RATIO = max(k[2] for k in data)
PIXELS_PER_RATIO = MAX_TEXT_WIDTH/MAX_RATIO

print("(" + ",\n ".join(str(item) for item in data) + ")")

screen: pygame.Surface = pygame.display.set_mode((TOTAL_BAR_WIDTH + MAX_TEXT_WIDTH,
                                                  len(data)*CARD_BAR_HEIGHT))
screen.fill(BK)

for n, (damage, name, ratio, cost) in enumerate(data):
    if damage < 2534:
        color = COLOR_1
    elif damage == 2534:
        color = COLOR_2
    else:
        color = COLOR_3

    if n % 2 == 1:
        color += COLOR_OFFSET

    if damage > 2534:
        extra = SEP_BAR_WIDTH
    else:
        extra = 0

    pygame.draw.rect(screen, color, pygame.Rect(MAX_TEXT_WIDTH + SEP_BAR_WIDTH, n*CARD_BAR_HEIGHT,
                                                PIXELS_PER_HEALTH*damage + extra, CARD_BAR_HEIGHT))

    pygame.draw.rect(screen, color, pygame.Rect(MAX_TEXT_WIDTH - PIXELS_PER_RATIO*ratio,
                                                n*CARD_BAR_HEIGHT,
                                                PIXELS_PER_RATIO*ratio + 1,
                                                CARD_BAR_HEIGHT))

    if n % 2 == 1:
        color += COLOR_OFFSET


    vert_offset = math.ceil((CARD_BAR_HEIGHT - names[n].get_height()) / 2)
    screen.blit(names[n], (SEP_BAR_WIDTH, n * CARD_BAR_HEIGHT + vert_offset))

    if damage <= 2534:
        num_1 = font.render(f"{damage} ({round(ratio)})", True, (255, 255, 255))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_1.get_height()) / 2)
        screen.blit(num_1, (MAX_TEXT_WIDTH + SEP_BAR_WIDTH*2, n * CARD_BAR_HEIGHT + vert_offset))

        num_2 = font.render(str(2534 - damage), True, (255, 255, 255))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_2.get_height()) / 2)
        screen.blit(num_2, (MAX_TEXT_WIDTH + MAX_PRINCESS_WIDTH - SEP_BAR_WIDTH - num_2.get_width(), n * CARD_BAR_HEIGHT + vert_offset))

        num_3 = font.render("0", True, (127, 127, 127))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_3.get_height()) / 2)
        screen.blit(num_3, (MAX_TEXT_WIDTH + MAX_PRINCESS_WIDTH + SEP_BAR_WIDTH*2, n * CARD_BAR_HEIGHT + vert_offset))

        num_4 = font.render("4008", True, (127, 127, 127))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_3.get_height()) / 2)
        screen.blit(num_4, (MAX_TEXT_WIDTH + TOTAL_BAR_WIDTH - SEP_BAR_WIDTH - num_4.get_width(), n * CARD_BAR_HEIGHT + vert_offset))
    else:
        num_1 = font.render(f"2534 ({round(ratio)})", True, (255, 255, 255))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_1.get_height()) / 2)
        screen.blit(num_1, (MAX_TEXT_WIDTH + SEP_BAR_WIDTH * 2, n * CARD_BAR_HEIGHT + vert_offset))

        num_2 = font.render("0", True, (255, 255, 255))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_2.get_height()) / 2)
        screen.blit(num_2, (MAX_TEXT_WIDTH + MAX_PRINCESS_WIDTH - SEP_BAR_WIDTH - num_2.get_width(), n * CARD_BAR_HEIGHT + vert_offset))

        num_3 = font.render(str(damage - 2534), True, (255, 255, 255))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_3.get_height()) / 2)
        screen.blit(num_3, (MAX_TEXT_WIDTH + MAX_PRINCESS_WIDTH + SEP_BAR_WIDTH*2, n * CARD_BAR_HEIGHT + vert_offset))

        num_4 = font.render(str(4008 - (damage - 2534)), True, (255, 255, 255))
        vert_offset = math.ceil((CARD_BAR_HEIGHT - num_3.get_height()) / 2)
        screen.blit(num_4, (MAX_TEXT_WIDTH + TOTAL_BAR_WIDTH - SEP_BAR_WIDTH - num_4.get_width(), n * CARD_BAR_HEIGHT + vert_offset))


pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(MAX_TEXT_WIDTH, 0,
                                                      SEP_BAR_WIDTH, len(data)*CARD_BAR_HEIGHT))
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(MAX_TEXT_WIDTH + MAX_PRINCESS_WIDTH, 0,
                                                      SEP_BAR_WIDTH, len(data)*CARD_BAR_HEIGHT))

_copy = screen.copy()

screen = pygame.display.set_mode((_copy.get_width() + BORDERS*2, _copy.get_height() + BORDERS*2))
screen.fill(BK)
screen.blit(_copy, (BORDERS, BORDERS))

pygame.image.save(screen, "vis2.png")
