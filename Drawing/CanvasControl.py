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


    def draw_text_pygame(self, text_struct):
        
        # maybe TODO: originally from calculate_text_label_pos
        # offset = 0
        # if self.props.has_text:
        #     if self.label.get_width() <= self.sizeX:
        #         offset = abs(self.sizeX - self.label.get_width()) / 2

        # x = self.posX + offset

        font = pygame.font.Font('./fonts/Roboto-VariableFont_wdth,wght.ttf', 18)
        label = font.render(text_struct.text_str, True, (0, 0, 0))
        text_rect = label.get_rect(topleft=(text_struct.text_rect_x, \
            text_struct.text_rect_y))

        self.screen.blit(label, text_rect)

    def draw_text(self, text_struct):
        if self.use_pygame:
            self.draw_text_pygame(text_struct)


