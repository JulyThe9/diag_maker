import pygame
import html
from PIL import Image, ImageDraw, ImageFont

import Globals as g

class CanvasControl:
    def __init__(self, mode=g.Mode.INTERACTIVE):
       self.mode = mode
       self.screen = None
       self.img_canvas = None
       self.pygame_labels = {}
       self.png_fonts = {}
       self.svg_elements = []

    def _to_svg_color(self, color):
        return f"rgb({color[0]},{color[1]},{color[2]})"

    def draw_rect(self, color, x, y, w, h):
        if self.mode == g.Mode.INTERACTIVE:
            if self.screen:
                pygame.draw.rect(self.screen, color, (x, y, w, h))
        elif self.mode == g.Mode.SVG or self.mode == g.Mode.HTML:
            fill = self._to_svg_color(color)
            self.svg_elements.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" />'
            )
        else:
            self.img_canvas.rectangle(
                [x, y, x + w, y + h],
                fill=color
            )

    def draw_line(self, color, start, end, label=None):
        if self.mode == g.Mode.INTERACTIVE:
            if self.screen:
                pygame.draw.line(self.screen, color, start, end, 2)
        elif self.mode == g.Mode.SVG or self.mode == g.Mode.HTML:
            stroke = self._to_svg_color(color)
            line_element = (
                f'<line x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" '
                f'stroke="{stroke}" stroke-width="2" />'
            )
            
            # If label is provided (e.g., from VBar compLabel), wrap with tooltip functionality
            if label and self.mode == g.Mode.HTML:
                escaped_label = html.escape(label)
                # Add invisible rect for hover area (20 pixels on each side)
                # basically, 30 % of block width, both sides together
                rect_width = g.DEF_BLOCK_WIDTH * g.DEF_RECT_WIDTH_MARGIN_FACT
                rect_x = start[0] - rect_width / 2
                rect_y = min(start[1], end[1])
                rect_height = abs(end[1] - start[1])
                invisible_rect = (
                    f'<rect x="{rect_x}" y="{rect_y}" width="{rect_width}" height="{rect_height}" '
                    f'fill="transparent" pointer-events="all" />'
                )
                tooltip_element = (
                    f'<g class="vbar-group" data-label="{escaped_label}">\n'
                    f'      {invisible_rect}\n'
                    f'      {line_element}\n'
                    f'      <title>{escaped_label}</title>\n'
                    f'    </g>'
                )
                self.svg_elements.append(tooltip_element)
            else:
                self.svg_elements.append(line_element)
        else:
            self.img_canvas.line([start, end], fill=color, width=2)

    def draw_arrow_head(self, color, head_end, head_left, head_right):
        if self.mode == g.Mode.INTERACTIVE:
            if self.screen:
                pygame.draw.polygon(self.screen, color, [head_end, \
                    head_left, head_right])
        elif self.mode == g.Mode.SVG or self.mode == g.Mode.HTML:
            fill = self._to_svg_color(color)
            points = f"{head_end[0]},{head_end[1]} {head_left[0]},{head_left[1]} {head_right[0]},{head_right[1]}"
            self.svg_elements.append(
                f'<polygon points="{points}" fill="{fill}" />'
            )
        else:
            self.img_canvas.polygon([head_end, head_left, head_right], fill=color)


    def draw_arrow(self, color, start, end, head_end, head_left, head_right):
        # shaft
        self.draw_line(color, start, end)

        # arrow head
        self.draw_arrow_head(color, head_end, head_left, head_right)

    def draw_looped_arrow(self, color, dist, start, end, head_end, head_left, head_right):
        # to the right
        help_point_1 = (start[0] + dist, start[1])
        self.draw_line(color, start, help_point_1)

        # to bottom
        help_point_2 = (help_point_1[0], end[1])
        self.draw_line(color, help_point_1, help_point_2)

        # to the left
        self.draw_line(color, help_point_2, end)

        # arrow head
        self.draw_arrow_head(color, head_end, head_left, head_right)


    def png_bbox_to_width(self, font, text_str):
        bbox = font.getbbox(text_str)
        text_width  = bbox[2] - bbox[0]
        return text_width

    # holder == holder of the text 
    def add_text(self, holder_id, text_str):
        if self.mode == g.Mode.INTERACTIVE:
            if holder_id in self.pygame_labels:
                #TODO: why 0 if it's in the list?
                return 0
            label = pygame.font.Font('./fonts/Roboto-VariableFont_wdth,wght.ttf', 18).\
                render(text_str, True, (0, 0, 0))
            self.pygame_labels[holder_id] = label
            return label.get_width()
        else:
            # For both PNG and SVG, we use PIL logic for text measurement
            if holder_id in self.png_fonts:
                #TODO: same: why 0 if it's in the list?
                return 0
            else:
                font = ImageFont.truetype('./fonts/Roboto-VariableFont_wdth,wght.ttf', 18)
                self.png_fonts[holder_id] = font
                return self.png_bbox_to_width(font, text_str)
                
        return 0

    def get_text_width(self, holder_id, text_str=""):
        if self.mode == g.Mode.INTERACTIVE:
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
        if self.mode == g.Mode.INTERACTIVE:
            self.draw_text_pygame(holder_id, text_struct)
        elif self.mode == g.Mode.SVG or self.mode == g.Mode.HTML:
            self.draw_text_svg(holder_id, text_struct)
        else:
            self.draw_text_png(holder_id, text_struct)

    def save_svg(self, filename, width, height):
        if self.mode != g.Mode.SVG:
            print("Warning: CanvasControl not initialized for SVG. Calling save_svg does nothing.")
            return

        with open(filename, 'w') as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
            # Add a white background rect
            f.write(f'<rect width="100%" height="100%" fill="white"/>\n')
            for el in self.svg_elements:
                f.write(f'  {el}\n')
            f.write('</svg>')

    def save_html(self, filename, width, height):
        if self.mode != g.Mode.HTML:
            print("Warning: CanvasControl not initialized for HTML. Calling save_html does nothing.")
            return

        with open(filename, 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html lang="en">\n')
            f.write('<head>\n')
            f.write('  <meta charset="UTF-8">\n')
            f.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write('  <title>Diagram</title>\n')
            f.write('  <style>\n')
            f.write('    body {\n')
            f.write('      margin: 0;\n')
            f.write('      padding: 20px;\n')
            f.write('      display: flex;\n')
            f.write('      justify-content: center;\n')
            f.write('      background-color: #f5f5f5;\n')
            f.write('      font-family: Arial, sans-serif;\n')
            f.write('    }\n')
            f.write('    svg {\n')
            f.write('      background-color: white;\n')
            f.write('      border: 1px solid #ddd;\n')
            f.write('      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);\n')
            f.write('    }\n')
            f.write('    .vbar-tooltip {\n')
            f.write('      position: absolute;\n')
            f.write('      background-color: #333;\n')
            f.write('      color: white;\n')
            f.write('      padding: 5px 10px;\n')
            f.write('      border-radius: 4px;\n')
            f.write('      font-size: 12px;\n')
            f.write('      white-space: nowrap;\n')
            f.write('      pointer-events: none;\n')
            f.write('      opacity: 0;\n')
            f.write('      transition: opacity 0.2s ease-in;\n')
            f.write('      z-index: 1000;\n')
            f.write('    }\n')
            f.write('    .vbar-tooltip.show {\n')
            f.write('      opacity: 1;\n')
            f.write('    }\n')
            f.write('    .vbar-group {\n')
            f.write('      cursor: pointer;\n')
            f.write('    }\n')
            f.write('    .vbar-group:hover line {\n')
            f.write('      stroke-width: 3;\n')
            f.write('    }\n')
            f.write('  </style>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write(f'  <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" id="diagram-svg">\n')
            f.write(f'    <rect width="100%" height="100%" fill="white"/>\n')
            for el in self.svg_elements:
                f.write(f'    {el}\n')
            f.write('  </svg>\n')
            f.write('  <div id="vbar-tooltip" class="vbar-tooltip"></div>\n')
            f.write('  <script>\n')
            f.write('    const tooltip = document.getElementById("vbar-tooltip");\n')
            f.write('    const svg = document.getElementById("diagram-svg");\n')
            f.write('    \n')
            f.write('    // Get all vbar groups\n')
            f.write('    const vbarGroups = document.querySelectorAll(".vbar-group[data-label]");\n')
            f.write('    \n')
            f.write('    vbarGroups.forEach(group => {\n')
            f.write('      group.addEventListener("mouseenter", (e) => {\n')
            f.write('        const label = group.getAttribute("data-label");\n')
            f.write('        const groupRect = group.getBoundingClientRect();\n')
            f.write('        const midX = groupRect.left + groupRect.width / 2;\n')
            f.write('        const midY = groupRect.top + groupRect.height / 2;\n')
            f.write('        \n')
            f.write('        tooltip.textContent = label;\n')
            f.write('        tooltip.classList.add("show");\n')
            f.write('        tooltip.style.left = (midX - tooltip.offsetWidth / 2) + "px";\n')
            f.write('        tooltip.style.top = (midY - tooltip.offsetHeight - 10) + "px";\n')
            f.write('      });\n')
            f.write('      \n')
            f.write('      group.addEventListener("mouseleave", () => {\n')
            f.write('        tooltip.classList.remove("show");\n')
            f.write('      });\n')
            f.write('    });\n')
            f.write('  </script>\n')
            f.write('</body>\n')
            f.write('</html>')


