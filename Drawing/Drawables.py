from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame

from .DrawableProps import DrawableProps, Sides
from .BasicPoint import BasicPoint
import Globals as g

class ShapeType(Enum):
    BLOCK = "block"
    ARROW = "arrow"
    VERTBAR = "vertbar"

# =================================================== DRAWABLE ===================================================
class Drawable:
    def __init__(self, shape_type: ShapeType, posX: int, posY: int, sizeX: int, sizeY: int):
        if not isinstance(shape_type, ShapeType):
            raise ValueError("shape_type must be an instance of ShapeType Enum")
        self.shape_type = shape_type
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.color = (0, 0, 0)
        self.attachedDrawables = []

    def attach(self, drawable):
        self.attachedDrawables.append(drawable)

    def set_color(self, color):
        self.color = color

    def add_text(self, text_str):
        font = pygame.font.Font('./fonts/Roboto-VariableFont_wdth,wght.ttf', 18)
        self.label = font.render(text_str, True, (0, 0, 0))

        self.props.has_text = True
        self.calculate_text_label_pos()

        self.text_rect = self.label.get_rect(topleft=(self.props.get_text_label_pos().x, \
            self.props.get_text_label_pos().y))

        self.props.diff_to_text_x = self.props.get_text_label_pos().x - self.posX
        self.props.diff_to_text_y = self.props.get_text_label_pos().y - self.posY

    def draw_text(self, surface, uxctrol):
        if self.props.has_text:
            text_rect = self.label.get_rect(topleft=(uxctrol.apply_offset_x(self.text_rect.x), \
                uxctrol.apply_offset_y(self.text_rect.y)))

            surface.blit(self.label, text_rect)

    @abstractmethod
    def calc_properties(self):
        """Calculate necessary properties for drawing."""
        pass

    @abstractmethod
    def draw(self, surface, uxctrol):
        """Draw the object on the surface."""
        pass

    @abstractmethod
    def set_pos_from_ref(self, ref_point, side):
        """Calc main pos from ref pos."""
        pass

    def is_mouse_over(self, mouse_pos, uxctrol):
        # Default implementation for the base class (return False or check for a block)
        return False
    
    def set_props_text_label_pos(self):
        if self.props.has_text:
            self.props.set_text_label_pos(self.posX + self.props.diff_to_text_x, \
                self.posY + self.props.diff_to_text_y)
            self.text_rect.topleft = (self.props.get_text_label_pos().x, self.props.get_text_label_pos().y) 

    def set_position(self, x, y):
        self.posX = x
        self.posY = y
        self.set_props_text_label_pos()
        
    def get_next_ref_point(self, update=False):
        return self.props.get_next_ref_point(update)

    def get_ref_point(self, side, update=False):
        return self.props.get_ref_point(side, update)

    def mark_ref_point_used(self, ref_id):
        self.props.mark_ref_point_used(ref_id)


# =================================================== BLOCK ===================================================
class Block(Drawable):
    def __init__(self, posX, posY, sizeX, sizeY):
        # Call the parent (Drawable) class constructor
        super().__init__(ShapeType.BLOCK, posX, posY, sizeX, sizeY)
        self.props = DrawableProps()
        self.populate_ref_points()

    def populate_ref_points(self):
        self.props.add_ref_point_sides(Sides.W, BasicPoint(self.posX, self.posY + self.sizeY / 2)) # A
        self.props.add_ref_point_sides(Sides.N, BasicPoint(self.posX + self.sizeX / 2, self.posY)) # B
        self.props.add_ref_point_sides(Sides.E, BasicPoint(self.posX + self.sizeX, self.posY + self.sizeY / 2)) # C
        self.props.add_ref_point_sides(Sides.S, BasicPoint(self.posX + self.sizeX / 2, self.posY + self.sizeY)) # D

    def calculate_text_label_pos(self):
        rp_east = self.props.get_ref_point(Sides.E)
        #x = self.posX + self.sizeX * g.DEF_BLOCK_TEXT_X_MARG_FACT

        offset = 0
        if self.props.has_text:
            if self.label.get_width() <= self.sizeX:
                offset = abs(self.sizeX - self.label.get_width()) / 2

        x = self.posX + offset

        y = rp_east.y
        # legowelt
        # print("{0} : {1}".format(self.posX,self.sizeX))
        self.props.set_text_label_pos(x,y)

    def calc_properties(self):
        # Block doesn't need any special calculations, so this method is empty.
        pass

    def set_pos_from_ref(self, ref_point, side):

        if ref_point == None:
            print ("Block::set_pos_from_ref: " + "ref_point is None")
            return

        bp = None
        if side == Sides.W:
            bp = BasicPoint(ref_point.x, ref_point.y - self.sizeY / 2)
        elif side == Sides.N:
            bp = BasicPoint(ref_point.x - self.sizeX / 2, ref_point.y)
        elif side == Sides.E:
            bp = BasicPoint(ref_point.x - self.sizeX, ref_point.y - self.sizeY / 2)
        elif side == Sides.S:
            bp = BasicPoint(ref_point.x - self.sizeX / 2, ref_point.y - self.sizeY)

        if bp:
            self.set_position(bp.x, bp.y)
            

    def is_mouse_over(self, mouse_pos, uxctrol):
        res = False
        ux_pos_x = uxctrol.apply_offset_x(self.posX)
        ux_pos_y = uxctrol.apply_offset_y(self.posY)

        if ux_pos_x <= mouse_pos[0] <= ux_pos_x + self.sizeX and \
            ux_pos_y <= mouse_pos[1] <= ux_pos_y + self.sizeY:

            print("OVER BLOCK")
            res = True

        return res

    def draw(self, surface, uxctrol):
        # Draw a simple rectangle for Block

        pygame.draw.rect(surface, self.color, (uxctrol.apply_offset_x(self.posX), \
            uxctrol.apply_offset_y(self.posY), self.sizeX, self.sizeY))

        self.draw_text(surface, uxctrol)

# =================================================== ARROW ===================================================
class Arrow(Drawable):
    def __init__(self, posX, posY, endX, endY):
        # Arrow specific initialization
        super().__init__(ShapeType.ARROW, posX, posY, abs(endX-posX), 0)
        self.endX = endX
        self.endY = endY
        self.calc_properties()
        self.props = DrawableProps()
        self.populate_ref_points()
        
    def populate_ref_points(self):
        self.props.add_ref_point_sides(Sides.W, BasicPoint(self.posX, self.posY))
        self.props.add_ref_point_sides(Sides.E, BasicPoint(self.posX + self.sizeX, self.posY))

    def left_to_right(self):
        return self.posX < self.endX

    def calculate_text_label_pos(self):
        print ('arrow calculcate')
        rp_east = self.props.get_ref_point(Sides.E)

        offset = 0
        x = 0
        if self.props.has_text:
            if self.label.get_width() <= self.sizeX:
                offset = abs(self.sizeX - self.label.get_width()) / 2
                if not self.left_to_right():
                    # two thirds from right to left
                    offset = -(offset + self.label.get_width())
                x = self.posX + offset
            # too big to fit case,
            # ltr text starts at line start
            # rtl text starts at line end
            else:
                if self.left_to_right():
                    x = self.posX + offset
                else:
                    x = self.endX + offset

        _, bounding_box_y, _, height = self.bounding_box
        y = bounding_box_y - height * g.DEF_BLOCK_TEXT_Y_MARG_FACT

        self.props.set_text_label_pos(x,y)

    def calc_properties(self):
        # Calculate the properties needed for drawing the arrow
        self.start = (self.posX, self.posY)
        self.end = (self.endX, self.endY)
        self.angle = math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])
        
        head_length = 10
        head_angle = math.radians(30)

        self.left = (
            self.end[0] - head_length * math.cos(self.angle + head_angle),
            self.end[1] - head_length * math.sin(self.angle + head_angle),
        )

        self.right = (
            self.end[0] - head_length * math.cos(self.angle - head_angle),
            self.end[1] - head_length * math.sin(self.angle - head_angle),
        )

        self.bounding_box = self.calc_bounding_box()
        x, y, width, height = self.bounding_box
        print(f"Bounding Box - X: {x}, Y: {y}, Width: {width}, Height: {height}")
    
    # arrow
    def calc_bounding_box(self):
        # Calculate the width of the bounding box as the distance between start and end points
        width = math.hypot(self.end[0] - self.posX, self.end[1] - self.posY)
        
        # The height of the bounding box is the height of the arrowhead triangle
        head_length = 10 * 3  # This is twice the same head length used for the arrow
        height = head_length
        
        # Calculate the angle for the bounding box to align with the arrow direction
        angle = math.atan2(self.end[1] - self.posY, self.end[0] - self.posX)

        # Calculate the position of the bounding box
        # Center the bounding box at the start point of the arrow
        bounding_x = self.posX
        if self.posX > self.endX:
            bounding_x = self.endX
        bounding_y = self.posY - height / 2.0

        # Return the bounding box as (x, y, width, height)
        return (bounding_x, bounding_y, width, height)

    def set_position(self, posX, posY):
        """
        Override the set_position method to update both the start and end points of the arrow.
        """

        # Update the starting position of the arrow
        self.posX = posX
        self.posY = posY
        # self.start = (self.posX, self.posY)
        # self.end = (self.posX + self.sizeX, self.posY)

        if self.left_to_right():
            self.endX = self.posX + self.sizeX
        else:
            self.endX = self.posX - self.sizeX

        self.endY = self.posY
        self.calc_properties()
        
        self.set_props_text_label_pos()


    def is_mouse_over(self, mouse_pos, uxctrol):
        x, y, width, height = self.bounding_box
        x = uxctrol.apply_offset_x(x)
        y = uxctrol.apply_offset_y(y)

        res = False

        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            print("OVER ARROW")
            res = True
        return res

    def draw(self, surface, uxctrol):
        apply_scroll = lambda t: (uxctrol.apply_offset_x(t[0]), \
            uxctrol.apply_offset_y(t[1]))
    
        pygame.draw.line(surface, self.color, apply_scroll(self.start), \
            apply_scroll(self.end), 2)

        pygame.draw.polygon(surface, self.color, [apply_scroll(self.end), \
            apply_scroll(self.left), apply_scroll(self.right)])

        self.draw_text(surface, uxctrol)



# =================================================== VBAR ===================================================
class VertBar(Drawable):
    def __init__(self, posX, posY, endX, endY):
        # Arrow specific initialization
        super().__init__(ShapeType.VERTBAR, posX, posY, 0, abs(endY-posY))
        self.endX = endX
        self.endY = endY
        self.calc_properties()
        self.props = DrawableProps(ref_points_are_list=True)
        self.populate_ref_points()
        
    def populate_ref_points(self):
        step = g.DEF_BLOCK_SIZE + g.DEF_GAP
        y = self.posY
        while y <= self.endY:
            #self.props.ref_points_list.append(MarkedPoint(self.posX, y))
            self.props.add_ref_point_list(BasicPoint(self.posX, y))
            y += step

    def calc_properties(self):
        self.start = (self.posX, self.posY)
        self.end = (self.endX, self.endY)

        self.bounding_box = self.calc_bounding_box()
        x, y, width, height = self.bounding_box
        print(f"Bounding Box - X: {x}, Y: {y}, Width: {width}, Height: {height}")
    
    def calc_bounding_box(self):
        # Calculate the height of the bounding box as the distance between start and end points
        height = math.hypot(self.end[0] - self.posX, self.end[1] - self.posY)
        
        # TODO: pixels?
        width = 10
    
        bounding_x = self.posX
        bounding_y = self.posY - height / 2.0

        # Return the bounding box as (x, y, width, height)
        return (bounding_x, bounding_y, width, height)

    def set_position(self, posX, posY):
        """
        Override the set_position method to update both the start and end points of the vertical bar.
        """
        # Update the starting position of the arrow
        self.posX = posX
        self.posY = posY
        self.endX = self.posX 
        self.endY = self.posY + self.sizeY
        self.calc_properties()
        
    def is_mouse_over(self, mouse_pos, uxctrol):
        x, y, width, height = self.bounding_box
        x = uxctrol.apply_offset_x(x)
        y = uxctrol.apply_offset_y(y)
        
        res = False
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            print("OVER VERT BAR")
            res = True
        return res

    def draw(self, surface, uxctrol):
        start = (uxctrol.apply_offset_x(self.posX), uxctrol.apply_offset_y(self.posY))
        end = (uxctrol.apply_offset_x(self.endX), uxctrol.apply_offset_y(self.endY))

        pygame.draw.line(surface, self.color, start, end, 2)