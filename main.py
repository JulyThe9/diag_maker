import pygame
import sys

import Drawables as dr
import Control as ctrl
import Style
import GlobalProps as glprops
import Functional as fn
import Globals as g
from DrawableProps import Sides

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

    g.global_props = glprops.GlobalProps(current_width, current_height)
    glprops.first_pos(g.global_props)

    control = ctrl.Control()

    return screen, control



def main():
    screen, control = init()

    arrow2 = fn.add_test(control)

    block = fn.add_block(control, parent=arrow2, parentSide=Sides.E, blockSide=Sides.W)
    vbar = fn.add_vbar(control, block)
    fn.add_block_to_vbar(control, vbar)
    fn.add_block_to_vbar(control, vbar)

    block3 = fn.add_block(control)
    vbar3 = fn.add_vbar(control, block3)
    fn.add_block_to_vbar(control, vbar3)
    fn.add_block_to_vbar(control, vbar3)
    fn.add_block_to_vbar(control, vbar3)

    fn.bar_to_bar(control, vbar3, vbar)

    # TODO: unit test idea
    # print("legowelt")
    # rp = block.get_ref_point(Sides.S)
    # print(rp.x, rp.y)
    # print(vbar.posX, vbar.posY)

    control.apply_styling(Style.colorful_style)

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
            
            control.handle_events(event)

        # Fill screen white
        screen.fill(MISC_WHITE)

        # Draw center vertical line
        center_x = current_width // 2
        pygame.draw.line(screen, MISC_LINE_COLOR, (center_x, 0), (center_x, current_height), 2)

        # Draw all the drawable objects in the control
        control.draw(screen)

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()