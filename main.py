import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from PIL import Image, ImageDraw
import sys
import json
import argparse
from pathlib import Path

# Drawing
import Drawing.Drawables as dr
import Drawing.Control as ctrl
import Drawing.CanvasControl as canvasctrl

from Drawing.Style import Style
import Drawing.Style as StyleModule

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
    
    for send, recv, *_ in messages:
        unique_entities.add(send)
        unique_entities.add(recv)
    
    return len(unique_entities)

def count_ref_points_needed(messages):
    res = 0
    for send, recv, *_ in messages:
        if send == recv:
            res += 2
        else:
            res += 1

    return res

def tune_vbar_size(num_messages):
    # +1 for margin
    return (num_messages + 1) * (g.DEF_BLOCK_SIZE + g.DEF_GAP)

def init(mode=g.Mode.INTERACTIVE, messages=None):    
    canvas = None
    image_obj = None
    initial_width = None
    initial_height = None

    vbar_tuned_size = g.DEF_VBAR_SIZE
    num_components = g.DEF_NUM_COMPONENTS
    num_messages = g.DEF_NUM_MESSAGES

    if messages:
        # + 1 for some margin
        num_components = count_unique_entities(messages) + 1
        num_messages = count_ref_points_needed(messages)

    if mode == g.Mode.INTERACTIVE:
        canvas, initial_width, initial_height = pygame_init()
    elif mode == g.Mode.PNG:
        initial_width = 3000
        initial_height = 6000
        vbar_tuned_size = tune_vbar_size(num_messages)
        image_obj, canvas = image_init(initial_width, initial_height)
    elif mode == g.Mode.SVG or mode == g.Mode.HTML:
        initial_width = 3000
        initial_height = 6000
        vbar_tuned_size = tune_vbar_size(num_messages)
        # For SVG/HTML we don't need a canvas/image object for drawing context
        canvas = None
        image_obj = None

    # Track current window size
    current_width, current_height = initial_width, initial_height
    #current_width = current_width * g.DEF_WIDTH_FACTOR

    if g.DEBUG:
        print(current_width)
    g.global_props = glprops.GlobalProps(current_height, current_width, vbar_tuned_size)

    if mode == g.Mode.INTERACTIVE:
        g.global_props.fill_in_base_positions(num_components, g.DEF_IMAGE_WIDTH_MARGIN_FACT)
    else:
        g.global_props.fill_in_base_positions(num_components, \
            g.DEF_IMAGE_WIDTH_MARGIN_FACT, g.DEF_IMAGE_HEIGHT_MARGIN_FACT)

    control = ctrl.Control()

    return canvas, image_obj, control
    
def interactive_main(filename):
    #print("WE ARE IN INTERACTIVE MAIN")

    messages = list(pctrl.parse_messages(filename))

    screen, _, control = init(g.Mode.INTERACTIVE, messages)

    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.INTERACTIVE)
    canvas_ctrl.screen = screen

    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    for send, recv, msg, details in messages:
        control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg, details)

    # TODO: unit test idea
    # rp = block.get_ref_point(Sides.S)
    # print(rp.x, rp.y)
    # print(vbar.posX, vbar.posY)
    
    control.apply_styling(Style.current())

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

def png_main(filename, output_dir, comp_order):
    #print("WE ARE IN IMAGE MAIN")

    messages = list(pctrl.parse_messages(filename))

    img_canvas, image_obj, control = init(g.Mode.PNG, messages)

    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.PNG)
    canvas_ctrl.img_canvas = img_canvas

    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    for send, recv, msg, details in messages:
        control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg, details)

    control.apply_styling(Style.current())
    control.draw(canvas_ctrl, uxctrol)
    
    base = filename.rsplit('/', 1)[-1]
    output_name = base.rsplit('.', 1)[0] + "_out.png"
    if g.DEBUG:
        output_name = "output.png"

    output_path = output_dir / output_name

    image_obj.save(output_path)
    print(f"Diagram saved {output_path}")

def svg_main(filename, output_dir, comp_order): 
    messages = list(pctrl.parse_messages(filename))

    # We use mode=g.Mode.SVG to set up global props but avoid creating PIL images
    img_canvas, image_obj, control = init(g.Mode.SVG, messages)
    
    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.SVG)
    
    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    # TODO: partial ordering instead of current (enforce ordered to go first)
    for component in comp_order:
        _ = control.get_or_create_block_and_vbar(pstate, canvas_ctrl, component)

    for send, recv, msg, details in messages:
        control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg, details)

    control.apply_styling(Style.current())
    control.draw(canvas_ctrl, uxctrol)
    
    # Use the dimensions from GlobalProps or the initial huge dimensions
    width = g.global_props.win_width if hasattr(g, 'global_props') else 3000
    height = g.global_props.win_height if hasattr(g, 'global_props') else 6000
    
    base = filename.rsplit('/', 1)[-1]
    output_name = base.rsplit('.', 1)[0] + "_out.svg"
    if g.DEBUG:
        output_name = "output.svg"

    output_path = output_dir / output_name

    canvas_ctrl.save_svg(output_path, int(width), int(height))
    print(f"Diagram saved {output_path.resolve()}")


def html_main(filename, output_dir, comp_order):
    #print("WE ARE IN HTML MAIN")
    
    messages = list(pctrl.parse_messages(filename))

    # We use mode=g.Mode.HTML to set up global props but avoid creating PIL images
    img_canvas, image_obj, control = init(g.Mode.HTML, messages)
    
    canvas_ctrl = canvasctrl.CanvasControl(mode=g.Mode.HTML)
    
    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    # TODO: partial ordering instead of current (enforce ordered to go first)
    for component in comp_order:
        _ = control.get_or_create_block_and_vbar(pstate, canvas_ctrl, component)

    for send, recv, msg, details in messages:
        control.build_comm_fragment(pstate, canvas_ctrl, send, recv, msg, details)

    control.apply_styling(Style.current())
    control.draw(canvas_ctrl, uxctrol)
    
    # Use the dimensions from GlobalProps or the initial huge dimensions
    width = g.global_props.win_width if hasattr(g, 'global_props') else 3000
    height = g.global_props.win_height if hasattr(g, 'global_props') else 6000
    
    base = filename.rsplit('/', 1)[-1]
    output_name = base.rsplit('.', 1)[0] + "_out.html"
    if g.DEBUG:
        output_name = "output.html"

    output_path = output_dir / output_name

    canvas_ctrl.save_html(output_path, int(width), int(height))
    print(f"Diagram saved {output_path.resolve()}")


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
        choices=["inter", "png", "svg", "html"],
        default="svg",
        help="Output mode: inter (interactive), png (image), svg, html"
    )

    parser.add_argument(
    "--comp-order",
        type=lambda s: s.split(","),
        default=[],
        help="Comma-separated list of components in the desired order"
    )

    # optional argument: output-dir
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Output directory (default: current directory)"
    )

    # optional argument: style settings
    parser.add_argument(
        "--style-settings",
        default="style_settings.json",
        help="Path to the style settings JSON file"
    )

    args = parser.parse_args()

    # init common stuff (styles)
    with open(args.style_settings, "r") as f:
        style_data = json.load(f)
        Style.load_from_json(style_data)

    # dispatch
    if args.mode == "png":
        png_main(args.message_file, args.output_dir, args.comp_order)
    elif args.mode == "svg":
        svg_main(args.message_file, args.output_dir, args.comp_order)
    elif args.mode == "html":
        html_main(args.message_file, args.output_dir, args.comp_order)
    else:
        interactive_main(args.message_file)

main()
sys.exit()