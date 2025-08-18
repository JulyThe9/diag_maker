from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame

from DrawableProps import DrawableProps, Sides
from BasicPoint import BasicPoint

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

    @abstractmethod
    def calc_properties(self):
        """Calculate necessary properties for drawing."""
        pass

    @abstractmethod
    def draw(self, surface):
        """Draw the object on the surface."""
        pass

    @abstractmethod
    def get_next_ref_point(self):
        """Draw the object on the surface."""
        pass

    @abstractmethod
    def set_pos_from_ref(self, ref_point, side):
        """Calc main pos from ref pos."""
        pass

    def is_mouse_over(self, mouse_pos):
        # Default implementation for the base class (return False or check for a block)
        return False

    def set_position(self, x, y):
        self.posX = x
        self.posY = y
        
    def get_next_ref_point(self, update=False):
        return self.props.get_next_ref_point(update)

    def get_ref_point(self, side, update=False):
        return self.props.get_ref_point(side, update)

    def mark_ref_point_used(self, side):
        self.props.mark_ref_point_used(side)


# =================================================== BLOCK ===================================================
class Block(Drawable):
    def __init__(self, posX, posY, sizeX, sizeY):
        # Call the parent (Drawable) class constructor
        super().__init__(ShapeType.BLOCK, posX, posY, sizeX, sizeY)
        self.props = DrawableProps()
        self.populate_ref_points()

    def populate_ref_points(self):
        self.props.add_ref_point(Sides.W, BasicPoint(self.posX, self.posY + self.sizeY / 2)) # A
        self.props.add_ref_point(Sides.N, BasicPoint(self.posX + self.sizeX / 2, self.posY)) # B
        self.props.add_ref_point(Sides.E, BasicPoint(self.posX + self.sizeX, self.posY + self.sizeY / 2)) # C
        self.props.add_ref_point(Sides.S, BasicPoint(self.posX + self.sizeX / 2, self.posY + self.sizeY)) # D

    def calc_properties(self):
        # Block doesn't need any special calculations, so this method is empty.
        pass

    def set_pos_from_ref(self, ref_point, side):
        bp = None
        if side == Sides.W:
            bp = BasicPoint(self.posX, self.posY - self.sizeY / 2)
        elif side == Sides.N:
            bp = BasicPoint(self.posX - self.sizeX / 2, self.posY)
        elif side == Sides.E:
            bp = BasicPoint(self.posX - self.sizeX, self.posY - self.sizeY / 2)
        elif side == Sides.S:
            bp = BasicPoint(self.posX - self.sizeX / 2, self.posY - self.sizeY)

        if bp:
            self.set_position(bp.x, bp.y)
            

    def is_mouse_over(self, mouse_pos):
        res = False
        if self.posX <= mouse_pos[0] <= self.posX + self.sizeX and self.posY <= mouse_pos[1] <= self.posY + self.sizeY:
            print("OVER BLOCK")
            res = True
        return res

    def draw(self, surface):
        # Draw a simple rectangle for Block
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, self.sizeX, self.sizeY))

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
        self.props.add_ref_point(Sides.W, BasicPoint(self.posX, self.posY))
        self.props.add_ref_point(Sides.E, BasicPoint(self.posX + self.sizeX, self.posY))

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
        bounding_y = self.posY - height / 2.0

        # Return the bounding box as (x, y, width, height)
        return (bounding_x, bounding_y, width, height)

    # def get_next_ref_point(self):
    #     return self.props.next_ref_point

    def set_position(self, posX, posY):
        """
        Override the set_position method to update both the start and end points of the arrow.
        """
        # Update the starting position of the arrow
        self.posX = posX
        self.posY = posY
        # self.start = (self.posX, self.posY)
        # self.end = (self.posX + self.sizeX, self.posY)

        self.endX = self.posX + self.sizeX
        self.endY = self.posY
        self.calc_properties()
        
        
    def is_mouse_over(self, mouse_pos):
        x, y, width, height = self.bounding_box
        res = False
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            print("OVER ARROW")
            res = True
        return res

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.end, 2)
        pygame.draw.polygon(surface, self.color, [self.end, self.left, self.right])



# =================================================== VERTBAR ===================================================
class VertBar(Drawable):
    def __init__(self, posX, posY, endX, endY):
        # Arrow specific initialization
        super().__init__(ShapeType.VERTBAR, posX, posY, 0, abs(endY-posY))
        self.endX = endX
        self.endY = endY
        self.calc_properties()
        self.props = DrawableProps()
        #self.populate_ref_points()
        
        
    # def populate_ref_points(self):
    #     self.props.add_ref_point(Sides.W, BasicPoint(self.posX, self.posY))
    #     self.props.add_ref_point(Sides.E, BasicPoint(self.posX + self.sizeX, self.posY))

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
        width = 20
    
        bounding_x = self.posX
        bounding_y = self.posY - height / 2.0

        # Return the bounding box as (x, y, width, height)
        return (bounding_x, bounding_y, width, height)

    # def get_next_ref_point(self):
    #     return self.props.next_ref_point

    def set_position(self, posX, posY):
        """
        Override the set_position method to update both the start and end points of the arrow.
        """
        # Update the starting position of the arrow
        self.posX = posX
        self.posY = posY
        self.endX = self.posX 
        self.endY = self.posY + self.sizeY
        self.calc_properties()
        
    def is_mouse_over(self, mouse_pos):
        x, y, width, height = self.bounding_box
        res = False
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            print("OVER VERT BAR")
            res = True
        return res

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.end, 2)