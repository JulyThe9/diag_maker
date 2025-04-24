import pygame
import sys

import Drawables as dr
import Control as ctrl
import Style

# Initialize Pygame
pygame.init()

# Get display size
info = pygame.display.Info()
initial_width, initial_height = info.current_w, info.current_h

# Create a resizable window starting at full screen size
screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window - Fullscreen Size")

# Colors
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)  # Black

# Track current window size
current_width, current_height = initial_width, initial_height

control = ctrl.Control()
control.add_drawable(dr.Block(posX=100, posY=150, sizeX=50, sizeY=50))  # Block object
control.add_drawable(dr.Arrow(posX=150, posY=175, endX=250, endY=175))  # Arrow object
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
    screen.fill(WHITE)

    # Draw center vertical line
    center_x = current_width // 2
    pygame.draw.line(screen, LINE_COLOR, (center_x, 0), (center_x, current_height), 2)

    # Draw all the drawable objects in the control
    control.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
