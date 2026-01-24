import pygame
from PIL import Image, ImageDraw, ImageFont

class CanvasControl:
    def __init__(self, use_pygame=True):
       self.use_pygame = use_pygame
       self.screen = None
       self.img_canvas = None
       self.pygame_labels = {}
       self.png_fonts = {}

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

    def png_bbox_to_width(self, font, text_str):
        bbox = font.getbbox(text_str)
        text_width  = bbox[2] - bbox[0]
        return text_width

    # holder == holder of the text 
    def add_text(self, holder_id, text_str):
        if self.use_pygame:
            if holder_id in self.pygame_labels:
                return
            label = pygame.font.Font('./fonts/Roboto-VariableFont_wdth,wght.ttf', 18).\
                render(text_str, True, (0, 0, 0))
            self.pygame_labels[holder_id] = label
            return label.get_width()
        else:
            if holder_id in self.png_fonts:
                return
            else:
                font = ImageFont.truetype('./fonts/Roboto-VariableFont_wdth,wght.ttf', 18)
                self.png_fonts[holder_id] = font
                return self.png_bbox_to_width(font, text_str)
                
        return 0

    def get_text_width(self, holder_id, text_str=""):
        if self.use_pygame:
            label = self.pygame_labels.get(holder_id)
            if label:
                return label.get_width()
        else:
            font = self.png_fonts.get(holder_id)
            if font:
                return self.png_bbox_to_width(font, text_str)
        
        return 0

    def draw_text_pygame(self, holder_id, text_struct): 
        label = self.pygame_labels.get(holder_id)
        if not label:
            return

        text_rect = label.get_rect(topleft=(text_struct.text_rect_x, \
            text_struct.text_rect_y))

        self.screen.blit(label, text_rect)

    def draw_text_png(self, holder_id, text_struct):
        x = text_struct.text_rect_x
        y = text_struct.text_rect_y

        font = self.png_fonts.get(holder_id)
        if not font:
            return

        self.img_canvas.text((x, y), text_struct.text_str, fill="black", font=font)

    def draw_text(self, holder_id, text_struct):
        if self.use_pygame:
            self.draw_text_pygame(holder_id, text_struct)
        else:
            self.draw_text_png(holder_id, text_struct)


