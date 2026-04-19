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

    # component is general for send and recv
    # in other words, communicating entity
    def get_or_create_block_and_vbar(self, pstate, canvas_ctrl, component):
        vbar = None
        if component in pstate.comm_entities:
            vbar = pstate.comm_entities[component]
        else:
            block = fn.add_rect(self, g.DEF_BLOCK_SIZE * g.DEF_RECT_WIDTH_FACT)
            
            if block:
                block.add_text(component, canvas_ctrl)

            vbar = fn.add_vbar(self, block)
            pstate.comm_entities[component] = vbar
        return vbar
    
    def build_comm_fragment(self, pstate, canvas_ctrl, send, recv, msg):
        if g.DEBUG:
            print (f"legowelt size of added entities: {len(pstate.comm_entities)}")
        send_bar = self.get_or_create_block_and_vbar(pstate, canvas_ctrl, send)
        recv_bar = self.get_or_create_block_and_vbar(pstate, canvas_ctrl, recv)
        
        if send_bar.ID < 0 or recv_bar.ID < 0:
            print("WARNING: USING OBJ ID BEFORE IT IS SET")

        if send_bar != recv_bar:
            fn.bar_to_bar(self, canvas_ctrl, send_bar, recv_bar, \
                send, recv, pstate.comm_entities, msg)
        else:
            fn.bar_to_iteslf(self, canvas_ctrl, send_bar, msg)
   
    def find_components_between(self, send, recv, comm_entities):
        keys = list(comm_entities.keys())

        # Find positions of send and recv
        try:
            i = keys.index(send)
            j = keys.index(recv)
        except ValueError:
            raise ValueError("send or recv not in comm_entities")

        # Determine range between them (exclude endpoints)
        if i < j:
            keys_inbetween = keys[i + 1:j]
        else:
            keys_inbetween = keys[j + 1:i]

        # Collect vbars in between
        vbars_inbetween = [comm_entities[k] for k in keys_inbetween]
        if g.DEBUG:
            print(f"Components between {send} and {recv} are:")
            for item in keys_inbetween:
                print(item)

        return vbars_inbetween

# free functions
def move_with_parent(drawable, delta_x, delta_y):
    drawable.set_position(drawable.posX + delta_x, drawable.posY + delta_y)
    for child in drawable.attachedDrawables:
        move_with_parent(child, delta_x, delta_y)