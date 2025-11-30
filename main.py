import pygame
import sys

# Drawing
import Drawing.Drawables as dr
import Drawing.Control as ctrl

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


def init():
    # Initialize Pygame
    pygame.init()

    # Get display size
    info = pygame.display.Info()
    initial_width, initial_height = info.current_w, info.current_h

    # Create a resizable window starting at full screen size
    screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
    pygame.display.set_caption("Resizable Window - Fullscreen Size")

    # Track current window size
    current_width, current_height = initial_width, initial_height
    current_width = current_width * g.DEF_WIDTH_FACTOR

    print (current_width)
    g.global_props = glprops.GlobalProps(current_height, current_width)
    g.global_props.fill_in_base_positions(g.DEF_NUM_COMPONENTS)

    control = ctrl.Control()

    return screen, control
    


def main():
    screen, control = init()
    pstate = pgs.GlobalState()
    uxctrol = uxc.UXCtrl()

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        for send, recv, msg in pctrl.parse_messages(filename):
            # print("Sender:", sender)
            # print("Receiver:", receiver)
            # print("Message:", msg)
            control.build_comm_fragment(pstate, send, recv, msg)

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
                print(event.x, uxctrol.scroll_offset_y)
            
            control.handle_events(event)

        # Fill screen white
        screen.fill(MISC_WHITE)

        # Draw center vertical line
        center_x = current_width // 2
        pygame.draw.line(screen, MISC_LINE_COLOR, (center_x, 0), (center_x, current_height), 2)

        # Draw all the drawable objects in the control
        control.draw(screen, uxctrol)

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()