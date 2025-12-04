import pygame

import Globals as g

class UXCtrl:
    def __init__(self):
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def apply_offset_x(self, posX):
        return self.apply_drag_offset_x(self.apply_scroll_offset_x(posX))

    def apply_offset_y(self, posY):
        return self.apply_drag_offset_y(self.apply_scroll_offset_y(posY))


    def apply_scroll_offset_x(self, posX):
        return posX + self.scroll_offset_x

    def apply_scroll_offset_y(self, posY):
        return posY + self.scroll_offset_y

    def apply_drag_offset_x(self, posX):
        return posX + self.drag_offset_x

    def apply_drag_offset_y(self, posY):
        return posY + self.drag_offset_y

