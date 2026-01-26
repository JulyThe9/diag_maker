from . import BasicPoint as bp

class GlobalProps:
    def __init__(self, win_height, win_width, num_components=2, next_position=None):
        if next_position is None:
            next_position = bp.BasicPoint()
        self.next_position = next_position
        self.win_height = win_height
        self.win_width = win_width
        self.base_positions = []
        self.base_pos_idx = 0
        
    def fill_in_base_positions(self, num_components):
        offset = self.win_width / num_components
        print (self.win_width)
        first_x = offset / 2 
        y = self.win_height / 4

        for i in range(num_components):
            x = first_x + i * offset
            print (x)
            self.base_positions.append(bp.BasicPoint(x,y))


    def get_next_pos(self, update=False):
        cur_base_pos_idx = self.base_pos_idx

        if cur_base_pos_idx >= len(self.base_positions):
            return None

        if update:
            self.base_pos_idx += 1
        return self.base_positions[cur_base_pos_idx]

    def __repr__(self):
        return f"GlobalProps(next_position={self.next_position})"


def first_pos(gprops):
    x = gprops.win_width / num_components / 2
    y = gprops.win_height / 4
    self.base_positions.append(bp.BasicPoint(x,y))
