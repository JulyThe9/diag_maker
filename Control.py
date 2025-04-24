import pygame
import Style

class Control:
    def __init__(self):
        self.drawables = []
        self.dragging_object = None
        self.mouse_offset = (0, 0)

    def add_drawable(self, drawable):
        self.drawables.append(drawable)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over any drawable object
            for drawable in self.drawables:
                if drawable.is_mouse_over(event.pos):
                    self.dragging_object = drawable
                    self.mouse_offset = (event.pos[0] - drawable.posX, event.pos[1] - drawable.posY)
                    break

        elif event.type == pygame.MOUSEMOTION:
            # If dragging an object, update its position

            for drawable in self.drawables:
                drawable.is_mouse_over(event.pos)

            if self.dragging_object:
                new_posX = event.pos[0] - self.mouse_offset[0]
                new_posY = event.pos[1] - self.mouse_offset[1]
                self.dragging_object.set_position(new_posX, new_posY)

        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging when the mouse button is released
            if self.dragging_object:
                self.dragging_object = None

    def draw(self, surface):
        # Draw all the drawable objects
        for drawable in self.drawables:
            drawable.draw(surface)

    def apply_styling(self, style: Style):
        for drawable in self.drawables:
            color = style.get_color(drawable.shape_type)
            drawable.set_color(color)