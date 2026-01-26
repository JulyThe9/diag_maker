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
        
    def fill_in_base_positions(self, num_components, width_margin_fact=0, height_margin_fact=0.25):
        #print (self.win_width)

        width_margin = self.win_width * width_margin_fact
        first_x = width_margin / 2 

        # we don't want to take margtins into acc 
        offset = (self.win_width - width_margin) / num_components

        y = self.win_height * height_margin_fact

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
