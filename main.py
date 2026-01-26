import pygame
from PIL import Image, ImageDraw
import sys
import argparse


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

def count_unique_entities(messages):
    unique_entities = set()
    
    for send, recv, _ in messages:
        unique_entities.add(send)
        unique_entities.add(recv)
    
    return len(unique_entities)

def init(mode=g.Mode.INTERACTIVE, num_components=g.DEF_NUM_COMPONENTS):    
    canvas = None
    image_obj = None
    initial_width = None
    initial_height = None
    
    if mode == g.Mode.INTERACTIVE:
        canvas, initial_width, initial_height = pygame_init()
    elif mode == g.Mode.PNG:
        initial_width = 3000
        initial_height = 6000
        image_obj, canvas = image_init(initial_width, initial_height)
    elif mode == g.Mode.SVG:
        initial_width = 3000
        initial_height = 6000
        # For SVG we don't need a canvas/image object for drawing context
        canvas = None
        image_obj = None

    # Track current window size
    current_width, current_height = initial_width, initial_height
    #current_width = current_width * g.DEF_WIDTH_FACTOR

    print (current_width)
    g.global_props = glprops.GlobalProps(current_height, current_width)

    if mode == g.Mode.INTERACTIVE:
        g.global_props.fill_in_base_positions(num_components, g.DEF_IMAGE_WIDTH_MARGIN_FACT)
    else:
        g.global_props.fill_in_base_positions(num_components, \
            g.DEF_IMAGE_WIDTH_MARGIN_FACT, g.DEF_IMAGE_HEIGHT_MARGIN_FACT)

    control = ctrl.Control()

    return canvas, image_obj, control
    
def interactive_main(filename):
    print("WE ARE IN INTERACTIVE MAIN")

    messages = list(pctrl.parse_messages(filename))
    num_components = count_unique_entities(messages)

    screen, _, control = init(g.Mode.INTERACTIVE, num_components)

    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.INTERACTIVE)
    canvas_ctrl.screen = screen

    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    for send, recv, msg in messages:
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

def png_main(filename):
    print("WE ARE IN IMAGE MAIN")

    messages = list(pctrl.parse_messages(filename))
    num_components = count_unique_entities(messages)

    img_canvas, image_obj, control = init(g.Mode.PNG, num_components)

    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.PNG)
    canvas_ctrl.img_canvas = img_canvas

    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    for send, recv, msg in messages:
        control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg)

    control.apply_styling(colorful_style)
    control.draw(canvas_ctrl, uxctrol)
    image_obj.save("output.png")

    sys.exit()

def svg_main(filename):
    print("WE ARE IN SVG MAIN")
    
    messages = list(pctrl.parse_messages(filename))
    num_components = count_unique_entities(messages)

    # We use mode=g.Mode.SVG to set up global props but avoid creating PIL images
    img_canvas, image_obj, control = init(g.Mode.SVG, num_components)
    
    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.SVG)
    
    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    for send, recv, msg in messages:
        control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg)

    control.apply_styling(colorful_style)
    control.draw(canvas_ctrl, uxctrol)
    
    # Use the dimensions from GlobalProps or the initial huge dimensions
    width = g.global_props.win_width if hasattr(g, 'global_props') else 3000
    height = g.global_props.win_height if hasattr(g, 'global_props') else 6000
    
    canvas_ctrl.save_svg("output.svg", int(width), int(height))
    print("Saved output.svg")

    sys.exit()

def main():
    parser = argparse.ArgumentParser(
        description="Process a message file and render output in different modes."
    )

    # positional argument: message file
    parser.add_argument(
        "message_file",
        help="Input file with messages (msg format: {sender, receiver, \"message\"})"
    )

    # optional argument: mode
    parser.add_argument(
        "--mode",
        choices=["inter", "png", "svg"],
        default="inter",
        help="Output mode: inter (interactive), png (image), svg"
    )

    args = parser.parse_args()

    # dispatch
    if args.mode == "png":
        png_main(args.message_file)
    elif args.mode == "svg":
        svg_main(args.message_file)
    else:
        interactive_main(args.message_file)

main()