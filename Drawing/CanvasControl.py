import pygame
from PIL import Image, ImageDraw

class CanvasControl:
    def __init__(self, use_pygame=True):
       self.use_pygame = use_pygame
       self.screen = None
       self.img_canvas = None

    def draw_line(self, color, start, end):
        if self.use_pygame:
            if self.screen:
                pygame.draw.line(self.screen, color, start, end, 2)
        else:
            self.img_canvas.line([start, end], fill=color, width=2)
    
    def draw_rect(self, color, x, y, w, h):
        if self.use_pygame:
            if self.screen:
                pygame.draw.rect(self.screen, color, (x, y, w, h))
        else:
            self.img_canvas.rectangle(
                [x, y, x + w, y + h],
                fill=color
            )

    def draw_arrow(self, color, start, end, head_end, head_left, head_right):
        # shaft
        self.draw_line(color, start, end)

        # arrow head
        if self.use_pygame:
            if self.screen:
                pygame.draw.polygon(self.screen, color, [head_end, \
                    head_left, head_right])
        else:
            self.img_canvas.polygon([head_end, head_left, head_right], fill=color)


