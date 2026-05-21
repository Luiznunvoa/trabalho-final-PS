import pygame
from .constantes import WHITE, DGRAY

class Button:
    def __init__(self, x, y, w, h, text, color=(70, 70, 110), text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 35, 255) for c in color)
        self.text_color = text_color
        self.enabled = True
        self.visible = True

    def draw(self, surf, font):
        if not self.visible:
            return
        mx, my = pygame.mouse.get_pos()
        hov = self.rect.collidepoint(mx, my) and self.enabled
        c = self.hover_color if hov else self.color
        if not self.enabled:
            c = (50, 50, 50)
        pygame.draw.rect(surf, (10, 10, 18), self.rect.move(3, 3), border_radius=10)
        pygame.draw.rect(surf, c, self.rect, border_radius=10)
        pygame.draw.rect(surf, WHITE if self.enabled else DGRAY, self.rect, 2, border_radius=10)
        txt = font.render(self.text, True, self.text_color)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.visible and self.enabled and self.rect.collidepoint(pos)