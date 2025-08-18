import BasicPoint
from enum import Enum
from dataclasses import dataclass

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
    def __init__(self, ref_points: dict[Sides, MarkedPoint] | None = None):
        if ref_points is None:
            ref_points = {}  # create a fresh empty dict
        self.ref_points = ref_points

    def add_ref_point(self, side_key: Sides, point: BasicPoint):
        self.ref_points[side_key] = MarkedPoint(point, False)

    def get_next_ref_point(self, update=False) -> tuple[Sides, MarkedPoint] | None:
        """Return the first side+point where used == False, or None if all used."""
        for side, marked_point in self.ref_points.items():
            if not marked_point.used:
                print ("LEGOWELT SIDE", side)
                if update:
                    marked_point.used = True
                return marked_point.point
        return None

    def get_ref_point(self, side: Sides, update: bool = False) -> MarkedPoint | None:
        """Lookup a MarkedPoint by side. If update=True, mark it as used."""
        marked_point = self.ref_points.get(side)
        if marked_point and update:
            marked_point.used = True
        return marked_point.point
        
    def mark_ref_point_used(self, side: Sides):
        """Lookup a MarkedPoint by side. Mark it as used."""
        marked_point = self.ref_points.get(side)
        if marked_point:
            marked_point.used = True

    def __repr__(self):
        #return f"DrawableProps(next_ref_point={self.ref_points[self.next_ref_point_id]})"
        return f"DrawableProps"