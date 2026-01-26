from . import BasicPoint
from enum import Enum
from dataclasses import dataclass
from pprint import pprint

class Sides(Enum):
    E = "E"
    N = "N"
    W = "W"
    S = "S"

@dataclass
class MarkedPoint:
    point: BasicPoint
    used: bool

class DrawableProps:
    def __init__(
        self,
        ref_points_are_list=False,
        ref_points_sides: dict[Sides, MarkedPoint] | None = None,
        ref_points_list: list[MarkedPoint] | None = None):
        
        self.ref_points_are_list = ref_points_are_list
        self.ref_points_list_id = 0

        self.ref_points_sides = ref_points_sides if ref_points_sides is not None else {}
        self.ref_points_list = ref_points_list if ref_points_list is not None else []

        self.has_text = False
        self.diff_to_text_x = 0
        self.diff_to_text_y = 0

    def add_ref_point_sides(self, side_key: Sides, point: BasicPoint):
        self.ref_points_sides[side_key] = MarkedPoint(point, False)
    
    def add_ref_point_list(self, point: BasicPoint):
        self.ref_points_list.append(MarkedPoint(point, False))

    def __get_next_ref_point_sides(self, update=False) -> tuple[Sides, MarkedPoint] | None:
        """Return the first side+point where used == False, or None if all used."""
        for side, marked_point in self.ref_points_sides.items():
            if not marked_point.used:
                if update:
                    marked_point.used = True
                return marked_point.point
        return None

    def __get_next_ref_point_list(self, update):
        for idx in range(self.ref_points_list_id, len(self.ref_points_list)):
            marked_point = self.ref_points_list[idx]
            if not marked_point.used:
                if update:
                    marked_point.used = True
                    self.ref_points_list_id = idx
                return marked_point.point
        return None  # no unused point found

    def get_next_ref_point(self, update=False):
        if self.ref_points_are_list:
            ref_point = self.__get_next_ref_point_list(update)
        else:
            ref_point = self.__get_next_ref_point_sides(update)

        if ref_point is None:
            raise ValueError("Next reference point could not be determined.")
        return ref_point

    def get_ref_point(self, side: Sides, update: bool = False) -> MarkedPoint | None:
        """Lookup a MarkedPoint by side. If update=True, mark it as used."""
        marked_point = self.ref_points_sides.get(side)
        if marked_point and self.ref_points_sides:
            marked_point.used = True
        return marked_point.point
        
    def mark_ref_point_used(self, ref_id):
        """Lookup a MarkedPoint by side/idx. Mark it as used."""
        if isinstance(ref_id, Sides):
            marked_point = self.ref_points_sides.get(ref_id)
            if marked_point:
                marked_point.used = True

        elif isinstance(ref_id, (int)):
            marked_point = self.ref_points_list[ref_id]
            if marked_point:
                marked_point.used = True

    def __repr__(self):
        #return f"DrawableProps(next_ref_point={self.ref_points_list[self.next_ref_point_id]})"
        return f"DrawableProps"