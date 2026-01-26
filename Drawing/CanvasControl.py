import pygame
import html
from PIL import Image, ImageDraw, ImageFont

class CanvasControl:
    def __init__(self, use_pygame=True, use_svg=False):
       self.use_pygame = use_pygame
       self.use_svg = use_svg
       self.screen = None
       self.img_canvas = None
       self.pygame_labels = {}
       self.png_fonts = {}
       self.svg_elements = []

    def _to_svg_color(self, color):
        return f"rgb({color[0]},{color[1]},{color[2]})"

    def draw_line(self, color, start, end):
        if self.use_pygame:
            if self.screen:
                pygame.draw.line(self.screen, color, start, end, 2)
        elif self.use_svg:
            stroke = self._to_svg_color(color)
            self.svg_elements.append(
                f'<line x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" '
                f'stroke="{stroke}" stroke-width="2" />'
            )
        else:
            self.img_canvas.line([start, end], fill=color, width=2)
    
    def draw_rect(self, color, x, y, w, h):
        if self.use_pygame:
            if self.screen:
                pygame.draw.rect(self.screen, color, (x, y, w, h))
        elif self.use_svg:
            fill = self._to_svg_color(color)
            self.svg_elements.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" />'
            )
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
        elif self.use_svg:
            fill = self._to_svg_color(color)
            points = f"{head_end[0]},{head_end[1]} {head_left[0]},{head_left[1]} {head_right[0]},{head_right[1]}"
            self.svg_elements.append(
                f'<polygon points="{points}" fill="{fill}" />'
            )
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
            # For both PNG and SVG, we use PIL logic for text measurement
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
            # Shared logic for PIL and SVG text measurement
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

    def draw_text_svg(self, holder_id, text_struct):
        x = text_struct.text_rect_x
        # Approximation for baseline correction (PIL vs SVG text anchor)
        # PIL draws top-left by default, SVG text 'y' is baseline by default.
        # But we can use dominant-baseline="hanging" to act like top-left.
        y = text_struct.text_rect_y
        
        text_content = html.escape(text_struct.text_str)
        self.svg_elements.append(
            f'<text x="{x}" y="{y}" fill="black" '
            f'font-family="Roboto" font-size="18" dominant-baseline="hanging">'
            f'{text_content}</text>'
        )

    def draw_text(self, holder_id, text_struct):
        if self.use_pygame:
            self.draw_text_pygame(holder_id, text_struct)
        elif self.use_svg:
            self.draw_text_svg(holder_id, text_struct)
        else:
            self.draw_text_png(holder_id, text_struct)

    def save_svg(self, filename, width, height):
        if not self.use_svg:
            print("Warning: CanvasControl not initialized for SVG. Calling save_svg does nothing.")
            return

        with open(filename, 'w') as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
            # Add a white background rect
            f.write(f'<rect width="100%" height="100%" fill="white"/>\n')
            for el in self.svg_elements:
                f.write(f'  {el}\n')
            f.write('</svg>')


