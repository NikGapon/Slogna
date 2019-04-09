import pygame
from map import Map
from eventlogger import keylogger
from gui import Input, Button, GuiGroup

FPS = 60


def on_click(mp, view):
    mp.set(search_result=None)
    input_view.text = ''


def index_click(mp, view):
    mp.set(show_index=not mp.show_index)
    if mp.show_index:
        view.color = pygame.Color('green')
        if mp.search_result is not None:
            input_view.text = mp.search_result.address + ', ' + str(mp.search_result.postal_code)
    else:
        view.color = pygame.Color('red')
        if mp.search_result is not None:
            input_view.text = mp.search_result.address


pygame.init()
width, height = 600, 450
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
mp = Map()
input_view = Input(10, 400, 500, 40)
btn = Button('Сбросить', 510, 400, height=40, click=on_click)
index_btn = Button('Индекс', 10, 10, color=pygame.Color('red'), click=index_click)
group = GuiGroup(input_view, btn, index_btn)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            keylogger(event, mp, group)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            group.check_click(*event.pos, mp)
    screen.blit(mp.get_map(), (0, 0))
    group.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
