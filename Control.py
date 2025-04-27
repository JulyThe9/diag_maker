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
                # self
                new_posX = event.pos[0] - self.mouse_offset[0]
                new_posY = event.pos[1] - self.mouse_offset[1]

                delta_x = new_posX - self.dragging_object.posX
                delta_y = new_posY - self.dragging_object.posY

                self.dragging_object.set_position(new_posX, new_posY)

                # children
                for child in self.dragging_object.attachedDrawables:
                    move_with_parent(child, delta_x, delta_y)


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


# free functions
def move_with_parent(drawable, delta_x, delta_y):
    drawable.set_position(drawable.posX + delta_x, drawable.posY + delta_y)
    for child in drawable.attachedDrawables:
        move_with_parent(child, delta_x, delta_y)