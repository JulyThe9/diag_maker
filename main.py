import pygame
import sys

import Drawables as dr
import Control as ctrl
import Style

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

    control = ctrl.Control()

    block1 = dr.Block(posX=100, posY=150, sizeX=50, sizeY=50)
    control.add_drawable(block1)  

    posX = block1.get_next_ref_point().x
    posY = block1.get_next_ref_point().y
    control.add_drawable(dr.Arrow(posX=posX, posY=posY,
        endX=posX+100, endY=posY))  

    control.apply_styling(Style.colorful_style)

    return screen, control



def main():

    screen, control = init()

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