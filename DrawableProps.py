class BasicPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class DrawableProps:
    def __init__(self, next_ref_point=None):
        self.next_ref_point = next_ref_point

    def set_next_ref_point(self, point):
        self.next_ref_point = point

    def get_next_ref_point(self):
        return self.next_ref_point

    def __repr__(self):
        return f"DrawableProps(next_ref_point={self.next_ref_point})"