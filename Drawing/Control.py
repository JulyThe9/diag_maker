import pygame

from . import Style
from . import Functional as fn
import Globals as g

class Control:
    def __init__(self):
        self.drawables = []
        self.dragging_object = None
        self.dragging_view = False
        self.last_free_mouse_pos = (0, 0)
        # only used for object dragging
        self.mouse_offset = (0, 0)

    def add_drawable(self, drawable):
        self.drawables.append(drawable)

    def handle_events(self, event, uxctrol):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over any drawable object
            for drawable in self.drawables:
                if drawable.is_mouse_over(event.pos, uxctrol):
                    self.dragging_object = drawable
                    self.mouse_offset = (event.pos[0] - drawable.posX, event.pos[1] - drawable.posY)
                    break
            

            if not self.dragging_object and event.button == 1:
                self.dragging_view = True

        elif event.type == pygame.MOUSEMOTION:
            # If dragging an object, update its position

            if self.dragging_view:
                mx, my = event.pos
                last_x, last_y = self.last_free_mouse_pos

                # delta movement
                dx = mx - last_x
                dy = my - last_y

                # apply movement to your view offset
                uxctrol.drag_offset_x += dx
                uxctrol.drag_offset_y += dy

                print("drag_offset_x = {0}".format(uxctrol.drag_offset_x))
                print("drag_offset_y = {0}".format(uxctrol.drag_offset_y))

                # update reference position
                self.last_free_mouse_pos = (event.pos[0], event.pos[1])
                return

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

                self.last_free_mouse_pos = (event.pos[0], event.pos[1])
                return

            for drawable in self.drawables:
                drawable.is_mouse_over(event.pos, uxctrol)

            self.last_free_mouse_pos = (event.pos[0], event.pos[1])


        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging when the mouse button is released
            if self.dragging_object:
                self.dragging_object = None

            if event.button == 1:
                self.dragging_view = False

    def draw(self, canvas_ctrl, uxctrol):
        # Draw all the drawable objects
        for drawable in self.drawables:
            drawable.draw(canvas_ctrl, uxctrol)

    def apply_styling(self, style: Style):
        for drawable in self.drawables:
            color = style.get_color(drawable.shape_type)
            drawable.set_color(color)

    # def get_drawable(self, idx):
    #     if idx >= len(self.drawables):
    #         return None

    #     return self.drawables[idx]

    
    def build_comm_fragment(self, pstate, canvas_ctrl, send, recv, msg):
        send_bar = recv_bar = None

        # print ("processing {0}".format(send))
        # print (pstate.comm_entities)
        
        if send in pstate.comm_entities:
            send_bar = pstate.comm_entities[send]
        else:
            block = fn.add_rect(self, g.DEF_BLOCK_SIZE * g.DEF_RECT_WIDTH_FACT)
            
            if block:
                block.add_text(send, canvas_ctrl)

            send_bar = fn.add_vbar(self, block)
            pstate.comm_entities[send] = send_bar
        
        if recv in pstate.comm_entities:
            recv_bar = pstate.comm_entities[recv]
        else:
            block = fn.add_rect(self, g.DEF_BLOCK_SIZE * g.DEF_RECT_WIDTH_FACT)
            
            if block:
                block.add_text(recv, canvas_ctrl)

            recv_bar = fn.add_vbar(self, block)
            pstate.comm_entities[recv] = recv_bar
        
        fn.bar_to_bar(self, canvas_ctrl, send_bar, recv_bar, msg)
        

# free functions
def move_with_parent(drawable, delta_x, delta_y):
    drawable.set_position(drawable.posX + delta_x, drawable.posY + delta_y)
    for child in drawable.attachedDrawables:
        move_with_parent(child, delta_x, delta_y)