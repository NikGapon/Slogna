import pygame
from map import RequestResult


class GuiGroup:

    def __init__(self, *views):
        self.views = list(views)

    def add(self, view):
        self.views.append(view)

    def render(self, screen):
        for view in self.views:
            view.render(screen)

    def check_click(self, pos_x, pos_y, mp):
        for view in self.views:
            view.check_click(pos_x, pos_y, mp)

    def key_pressed(self, event, mp):
        for view in self.views:
            view.key_pressed(event, mp)

    def key_released(self, event, mp):
        for view in self.views:
            view.key_released(event, mp)


class View:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = 5

    def get_rect(self):
        return (
            self.x,
            self.y,
            self.width,
            self.height
        )

    def on_click(self, mp):
        pass

    def out_click(self, mp):
        pass

    def key_pressed(self, event, mp):
        pass

    def key_released(self, event, mp):
        pass

    def get_relative_position(self, w, h, valign='center', halign='center'):
        x, y = self.x, self.y
        if halign == 'center':
            x = self.x + (self.width - w) // 2
        elif halign == 'right':
            x = self.x + self.width - w - self.margin
        elif halign == 'left':
            x = self.x + self.margin
        if valign == 'center':
            y = self.y + (self.height - h) // 2
        elif valign == 'bottom':
            y = self.y + self.height - h - self.margin
        elif valign == 'top':
            y = self.y + self.margin
        return x, y

    def check_click(self, pos_x, pos_y, mp):
        if self.x <= pos_x <= self.x + self.width \
                and self.y < pos_y <= self.y + self.height:
            self.on_click(mp)
        else:
            self.out_click(mp)

    def render(self, screen):
        pass


class Input(View):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.text = ''
        self.font = pygame.font.Font(None, 25)
        self.is_focused = False

    def on_click(self, mp):
        self.is_focused = True

    def out_click(self, mp):
        self.is_focused = False

    def key_pressed(self, event, mp):
        if self.is_focused:
            if event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
            elif event.key == 13:  # Enter key code
                request = RequestResult(self.text)
                mp.set(search_result=request)
                if mp.show_index:
                    self.text = request.address + ', ' + str(request.postal_code)
                else:
                    self.text = request.address
            else:
                self.text += event.unicode

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.get_rect(), 0)
        if not self.text and not self.is_focused:
            rendered_text = self.font.render('Поиск...', 1, pygame.Color('grey'))
        elif not self.text and self.is_focused:
            rendered_text = self.font.render('', 1, pygame.Color('white'))
        else:
            rendered_text = self.font.render(self.text, 1, pygame.Color('black'))
        screen.blit(rendered_text,
                    self.get_relative_position(rendered_text.get_width(), rendered_text.get_height(), halign='left'))


class Button(View):

    def __init__(self, title, x, y, width=0, height=0, color=pygame.Color('green'), click=None):
        self.margin = 5
        self.title = title
        self.color = color
        self.font = pygame.font.Font(None, 25)
        self.click = click
        self.rendered_title = self.get_rendered_title()
        if width == 0 and height == 0:
            width = self.rendered_title.get_width() + 2 * self.margin
            height = self.rendered_title.get_height() + 2 * self.margin
        elif width == 0:
            width = self.rendered_title.get_width() + 2 * self.margin
        elif height == 0:
            height = self.rendered_title.get_height() + 2 * self.margin
        super().__init__(x, y, width, height)

    def set_title(self, title):
        self.title = title
        self.rendered_title = self.get_rendered_title()

    def get_rendered_title(self):
        return self.font.render(self.title, 1, pygame.Color('white'))

    def on_click(self, mp):
        self.click(mp, self)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())
        screen.blit(self.rendered_title, (
            self.x + (self.width - self.rendered_title.get_width()) // 2,
            self.y + (self.height - self.rendered_title.get_height()) // 2
        ))
