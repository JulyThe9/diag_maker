import pygame
from PIL import Image, ImageDraw
import sys

# Drawing
import Drawing.Drawables as dr
import Drawing.Control as ctrl
import Drawing.CanvasControl as canvasctrl

from Drawing.Style import colorful_style

import Drawing.GlobalProps as glprops
import Drawing.Functional as fn
import Globals as g
from Drawing.DrawableProps import Sides

# Parser
import Parser.ParserCtrl as pctrl
import Parser.GlobalState as pgs

# UXCtrl
import UX.UXCtrl as uxc


 # Colors
MISC_WHITE = (255, 255, 255)
MISC_LINE_COLOR = (0, 0, 0)  # Black


def pygame_init():
    # Initialize Pygame
    pygame.init()

    # Get display size
    info = pygame.display.Info()
    initial_width, initial_height = info.current_w, info.current_h

    # Create a resizable window starting at full screen size
    screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
    pygame.display.set_caption("Resizable Window - Fullscreen Size")

    return screen, initial_width, initial_height

def image_init(width, height):
    image = Image.new("RGB", (width, height), MISC_WHITE)  # transparent bg
    img_canvas = ImageDraw.Draw(image)

    return image, img_canvas

def init(interactive=True):
    
    canvas = None
    image_obj = None
    initial_width = None
    initial_height = None
    if interactive:
        canvas, initial_width, initial_height = pygame_init()
    else:
        initial_width = 3000
        initial_height = 6000
        image_obj, canvas = image_init(initial_width, initial_height)

    # Track current window size
    current_width, current_height = initial_width, initial_height
    current_width = current_width * g.DEF_WIDTH_FACTOR

    print (current_width)
    g.global_props = glprops.GlobalProps(current_height, current_width)
    g.global_props.fill_in_base_positions(g.DEF_NUM_COMPONENTS)

    control = ctrl.Control()

    return canvas, image_obj, control
    
def interactive_main():
    print("WE ARE IN INTERACTIVE MAIN")

    screen, _, control = init()

    canvas_ctrl = canvasctrl.CanvasControl(True)
    canvas_ctrl.screen = screen

    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        for send, recv, msg in pctrl.parse_messages(filename):
            # print("Sender:", sender)
            # print("Receiver:", receiver)
            # print("Message:", msg)
            control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg)

    # TODO: unit test idea
    # print("legowelt")
    # rp = block.get_ref_point(Sides.S)
    # print(rp.x, rp.y)
    # print(vbar.posX, vbar.posY)

    control.apply_styling(colorful_style)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.w, event.h
                # Only update internal size variables, don't recreate the window!
            elif event.type == pygame.MOUSEWHEEL:
                uxctrol.scroll_offset_y -= event.y * g.DEF_SCROLL_SPEED_FACT
                # print(event.x, uxctrol.scroll_offset_y)
            
            control.handle_events(event, uxctrol)

        # Fill screen white
        canvas_ctrl.screen.fill(MISC_WHITE)

        # Draw center vertical line
        center_x = current_width // 2
        pygame.draw.line(canvas_ctrl.screen, MISC_LINE_COLOR, (center_x, 0), (center_x, current_height), 2)

        # Draw all the drawable objects in the control
        control.draw(canvas_ctrl, uxctrol)

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def image_main():
    print("WE ARE IN IMAGE MAIN")
    img_canvas, image_obj, control = init(False)

    canvas_ctrl = canvasctrl.CanvasControl(False)
    canvas_ctrl.img_canvas = img_canvas

    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        for send, recv, msg in pctrl.parse_messages(filename):
            control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg)

    control.apply_styling(colorful_style)
    control.draw(canvas_ctrl, uxctrol)
    image_obj.save("output.png")

    sys.exit()

def main():
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'y':
            image_main()
        else:
            interactive_main()
    else:
        interactive_main()

main()