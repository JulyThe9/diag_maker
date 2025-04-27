import BasicPoint as bp

class GlobalProps:
    def __init__(self, win_height, win_width, next_position=None):
        if next_position is None:
            next_position = bp.BasicPoint()
        self.next_position = next_position
        self.win_height = win_height
        self.win_width = win_width

    def set_next_pos(self, x, y):
        self.next_position = bp.BasicPoint(x, y)

    def get_next_pos(self):
        return self.next_position

    def __repr__(self):
        return f"GlobalProps(next_position={self.next_position})"


def first_pos(gprops):
    x = gprops.win_width / 2 / 2
    y = gprops.win_height / 4
    gprops.set_next_pos(x, y)
